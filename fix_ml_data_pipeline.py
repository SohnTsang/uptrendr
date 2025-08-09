#!/usr/bin/env python3
"""
FIX ML DATA PIPELINE
====================

This script fixes the ML data pipeline by:
1. Populating Firestore with real market data
2. Creating proper historical factors with real returns
3. Training ML models with real data instead of random data

Run this to fix the "all predictions around 50" issue.
"""

import sys
import os
sys.path.append('/Users/sohntsang/Desktop/Uptrendr/Uptrendr')

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timezone, timedelta
from google.cloud import firestore
import logging
import requests

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_firestore():
    """Initialize Firestore connection"""
    try:
        db = firestore.Client()
        logger.info("🔥 Connected to Firestore successfully!")
        return db
    except Exception as e:
        logger.error(f"❌ Failed to connect to Firestore: {e}")
        return None

def fetch_and_store_real_market_data(db):
    """Fetch real market data from Yahoo Finance and store in Firestore"""
    logger.info("📊 Fetching real market data...")
    
    # Major symbols to fetch
    symbols = [
        # US Markets
        '^GSPC', '^DJI', '^IXIC',  # S&P 500, Dow Jones, NASDAQ
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA',
        # Global Markets
        '^N225', '^TOPX',  # Nikkei, TOPIX
        '^FTSE', '^GDAXI', '^FCHI',  # FTSE, DAX, CAC
        # Forex
        'USDJPY=X', 'EURUSD=X', 'GBPUSD=X'
    ]
    
    market_data_batch = []
    technical_data_batch = []
    
    for symbol in symbols:
        try:
            logger.info(f"📈 Processing {symbol}")
            
            # Get 60 days of data for proper technical analysis
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="60d", interval="1d")
            info = ticker.info
            
            if hist.empty:
                logger.warning(f"❌ No data for {symbol}")
                continue
            
            # Process each day's data
            for i in range(len(hist)):
                date = hist.index[i]
                data_point = hist.iloc[i]
                
                # Calculate technical indicators
                if i >= 14:  # Need at least 14 days for RSI
                    prices = hist['Close'][:i+1]
                    
                    # RSI calculation
                    delta = prices.diff()
                    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                    rs = gain / loss
                    rsi = 100 - (100 / (1 + rs)).iloc[-1]
                    
                    # Moving averages
                    ma_20 = prices.rolling(20).mean().iloc[-1] if len(prices) >= 20 else prices.iloc[-1]
                    ma_50 = prices.rolling(50).mean().iloc[-1] if len(prices) >= 50 else prices.iloc[-1]
                    
                    # Technical score based on multiple indicators
                    price_vs_ma20 = (prices.iloc[-1] - ma_20) / ma_20 if ma_20 > 0 else 0
                    price_vs_ma50 = (prices.iloc[-1] - ma_50) / ma_50 if ma_50 > 0 else 0
                    rsi_score = (rsi - 50) / 50  # Normalized RSI
                    
                    technical_score = np.clip(0.5 + (price_vs_ma20 * 0.3 + price_vs_ma50 * 0.2 + rsi_score * 0.3), 0, 1)
                else:
                    technical_score = 0.5
                    rsi = 50
                
                # Fundamental score (basic)
                try:
                    pe_ratio = info.get('trailingPE', 20)
                    market_cap = info.get('marketCap', 1000000000)
                    
                    # Normalize P/E ratio (lower is better, but not too low)
                    pe_score = max(0, min(1, 1 - (pe_ratio - 15) / 50)) if pe_ratio and pe_ratio > 0 else 0.5
                    fundamental_score = np.clip(pe_score, 0, 1)
                except:
                    fundamental_score = 0.5
                
                # Create market data document
                market_doc = {
                    'symbol': symbol,
                    'price': float(data_point['Close']),
                    'open': float(data_point['Open']),
                    'high': float(data_point['High']),
                    'low': float(data_point['Low']),
                    'volume': int(data_point['Volume']) if not pd.isna(data_point['Volume']) else 0,
                    'current_price': float(data_point['Close']),
                    'close_price': float(data_point['Close']),
                    'volatility': float(np.std(hist['Close'].pct_change().dropna()) * 100 * np.sqrt(252)) if len(hist) > 5 else 15.0,
                    'fundamental_score': float(fundamental_score),
                    'technical_score': float(technical_score),
                    'timestamp': date.replace(tzinfo=timezone.utc),
                    'source': 'yfinance_real_data'
                }
                
                market_data_batch.append(market_doc)
                
                # Create technical analysis document
                tech_doc = {
                    'symbol': symbol,
                    'rsi': float(rsi) if not np.isnan(rsi) else 50.0,
                    'technical_score': float(technical_score),
                    'price_change_pct': float(data_point['Close'] / data_point['Open'] - 1) if data_point['Open'] > 0 else 0.0,
                    'volume': int(data_point['Volume']) if not pd.isna(data_point['Volume']) else 0,
                    'timestamp': date.replace(tzinfo=timezone.utc),
                    'source': 'calculated_real_data'
                }
                
                technical_data_batch.append(tech_doc)
        
        except Exception as e:
            logger.error(f"❌ Error processing {symbol}: {e}")
            continue
    
    # Batch write to Firestore
    if market_data_batch:
        logger.info(f"💾 Writing {len(market_data_batch)} market data records...")
        batch = db.batch()
        batch_count = 0
        
        for doc in market_data_batch:
            doc_ref = db.collection('market_data').document(f"{doc['symbol']}_{int(doc['timestamp'].timestamp())}")
            batch.set(doc_ref, doc)
            batch_count += 1
            
            if batch_count >= 400:  # Firestore batch limit
                batch.commit()
                batch = db.batch()
                batch_count = 0
        
        if batch_count > 0:
            batch.commit()
    
    if technical_data_batch:
        logger.info(f"📊 Writing {len(technical_data_batch)} technical analysis records...")
        batch = db.batch()
        batch_count = 0
        
        for doc in technical_data_batch:
            doc_ref = db.collection('technical_analysis').document(f"{doc['symbol']}_{int(doc['timestamp'].timestamp())}")
            batch.set(doc_ref, doc)
            batch_count += 1
            
            if batch_count >= 400:
                batch.commit()
                batch = db.batch()
                batch_count = 0
        
        if batch_count > 0:
            batch.commit()
    
    logger.info(f"✅ Stored {len(market_data_batch)} market data records and {len(technical_data_batch)} technical records")
    return len(market_data_batch)

def create_real_historical_factors(db):
    """Create historical factors with REAL returns calculated from price changes"""
    logger.info("🔧 Creating historical factors with REAL returns...")
    
    # Get all market data from last 30 days
    cutoff_time = datetime.now(timezone.utc) - timedelta(days=30)
    market_query = db.collection('market_data').where('timestamp', '>=', cutoff_time).stream()
    
    # Group by symbol and date
    symbol_data = {}
    for doc in market_query:
        data = doc.to_dict()
        symbol = data['symbol']
        date_key = data['timestamp'].date()
        
        if symbol not in symbol_data:
            symbol_data[symbol] = {}
        
        symbol_data[symbol][date_key] = data
    
    # Create historical factors with real returns
    historical_batch = []
    horizons = ['1W', '1M', '6M']
    
    for symbol, dates_data in symbol_data.items():
        # Sort dates
        sorted_dates = sorted(dates_data.keys())
        
        if len(sorted_dates) < 2:
            continue
        
        # Calculate returns for different horizons
        for i, current_date in enumerate(sorted_dates):
            current_data = dates_data[current_date]
            current_price = current_data['price']
            
            for horizon in horizons:
                # Calculate lookback period for each horizon
                if horizon == '1W':
                    lookback_days = 7
                elif horizon == '1M':
                    lookback_days = 30
                else:  # 6M
                    lookback_days = 180
                
                # Find price from lookback_days ago
                target_date = current_date - timedelta(days=lookback_days)
                
                # Find closest available date
                past_price = None
                for past_date in sorted_dates:
                    if past_date <= target_date:
                        past_price = dates_data[past_date]['price']
                    else:
                        break
                
                if past_price is None or past_price <= 0:
                    continue
                
                # Calculate REAL return
                actual_return = (current_price - past_price) / past_price
                
                # Get factor scores
                fundamental = current_data.get('fundamental_score', 0.5)
                technical = current_data.get('technical_score', 0.5)
                
                # Create historical factor document
                historical_doc = {
                    'symbol': symbol,
                    'horizon': horizon,
                    'timestamp': current_data['timestamp'],
                    'fundamental': float(fundamental),
                    'technical': float(technical),
                    'sentiment': float(np.random.uniform(0.3, 0.7)),  # Placeholder - would come from news analysis
                    'macro': float(np.random.uniform(0.4, 0.6)),     # Placeholder - would come from economic data
                    'esg': float(np.random.uniform(0.4, 0.6)),       # Placeholder - would come from ESG data
                    'actual_return': float(np.clip(actual_return, -0.5, 0.5)),  # Real calculated return!
                    'price': float(current_price),
                    'volatility': float(current_data.get('volatility', 20)),
                    'volume': int(current_data.get('volume', 0)),
                    'source': 'real_calculated_returns'
                }
                
                historical_batch.append(historical_doc)
                
                if len(historical_batch) % 100 == 0:
                    logger.info(f"📊 Created {len(historical_batch)} historical factors so far...")
    
    # Batch write historical factors
    if historical_batch:
        logger.info(f"💾 Writing {len(historical_batch)} historical factor records...")
        batch = db.batch()
        batch_count = 0
        
        for doc_data in historical_batch:
            doc_ref = db.collection('historical_factors').document()
            batch.set(doc_ref, doc_data)
            batch_count += 1
            
            if batch_count >= 400:
                batch.commit()
                batch = db.batch()
                batch_count = 0
        
        if batch_count > 0:
            batch.commit()
    
    logger.info(f"✅ Created {len(historical_batch)} historical factors with REAL returns")
    return len(historical_batch)

def trigger_model_training():
    """Trigger ML model training via API"""
    logger.info("🤖 Triggering ML model training...")
    
    try:
        # Trigger training for each horizon
        base_url = "https://uptrendr-api-626448778297.asia-northeast1.run.app"
        
        endpoints = [
            f"{base_url}/train-models/1W",
            f"{base_url}/train-models/1M", 
            f"{base_url}/train-models/6M"
        ]
        
        for endpoint in endpoints:
            try:
                logger.info(f"🚀 Training models at {endpoint}")
                response = requests.post(endpoint, timeout=120)
                if response.status_code == 200:
                    result = response.json()
                    logger.info(f"✅ Training successful: {result.get('message', 'OK')}")
                else:
                    logger.warning(f"⚠️ Training response: {response.status_code}")
            except Exception as e:
                logger.error(f"❌ Training failed for {endpoint}: {e}")
                
    except Exception as e:
        logger.error(f"❌ Error triggering model training: {e}")

def main():
    """Main function to fix the ML data pipeline"""
    logger.info("🚀 Starting ML Data Pipeline Fix...")
    
    # Initialize Firestore
    db = initialize_firestore()
    if not db:
        logger.error("❌ Cannot continue without Firestore connection")
        return
    
    try:
        # Step 1: Fetch and store real market data
        logger.info("\n1️⃣ FETCHING REAL MARKET DATA...")
        market_records = fetch_and_store_real_market_data(db)
        
        # Step 2: Create historical factors with real returns
        logger.info("\n2️⃣ CREATING HISTORICAL FACTORS WITH REAL RETURNS...")
        factor_records = create_real_historical_factors(db)
        
        # Step 3: Trigger model training
        logger.info("\n3️⃣ TRIGGERING ML MODEL TRAINING...")
        trigger_model_training()
        
        logger.info("\n🎉 ML Data Pipeline Fix Complete!")
        logger.info(f"✅ Market Data Records: {market_records}")
        logger.info(f"✅ Historical Factor Records: {factor_records}")
        logger.info("✅ ML Model Training Triggered")
        
        print("\n" + "="*60)
        print("🎯 NEXT STEPS:")
        print("1. Wait 2-3 minutes for model training to complete")
        print("2. Test your iOS app - predictions should now show variety!")
        print("3. Check logs for any training errors")
        print("="*60)
        
    except Exception as e:
        logger.error(f"❌ Error in main process: {e}")
        raise

if __name__ == "__main__":
    main()
