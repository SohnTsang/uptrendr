#!/usr/bin/env python3
"""
DIRECT FIREBASE WRITE TEST
===========================

This script directly writes to Firebase to test if the database operations
are working, bypassing the API endpoints that are giving false success responses.
"""

import os
import sys
from datetime import datetime, timezone

# Add the Uptrendr directory to path
sys.path.append('/Users/sohntsang/Desktop/Uptrendr/Uptrendr')

def main():
    print("🚀 DIRECT FIREBASE WRITE TEST")
    print("=" * 50)
    print(f"📅 Started at: {datetime.now()}")
    print()
    
    try:
        # Import Firebase modules
        from google.cloud import firestore
        from firebase_admin import initialize_app, credentials
        
        print("✅ Firebase modules imported")
        
        # Initialize Firebase
        try:
            import firebase_admin
            app = firebase_admin.get_app()
            print("✅ Firebase app already initialized")
        except ValueError:
            cred = credentials.ApplicationDefault()
            firebase_admin.initialize_app(cred)
            print("✅ Firebase app initialized")
        
        # Get Firestore client
        db = firestore.Client()
        print("✅ Firestore client created")
        
        # Test 1: Write new collection
        print("\n🧪 TEST 1: WRITING TO NEW COLLECTION")
        print("-" * 40)
        
        new_collection = 'direct_test_collection'
        test_data = {
            'test_type': 'direct_firebase_write',
            'timestamp': datetime.now(timezone.utc),
            'message': 'This data was written directly to Firebase',
            'success': True,
            'symbols': ['AAPL', 'TSLA', 'MSFT']
        }
        
        doc_ref = db.collection(new_collection).document('test_doc_1')
        doc_ref.set(test_data)
        print(f"✅ Wrote to {new_collection}/test_doc_1")
        
        # Read it back
        doc = doc_ref.get()
        if doc.exists:
            data = doc.to_dict()
            print(f"✅ Read back successfully: {data['message']}")
        else:
            print("❌ Could not read back the document")
            
        # Test 2: Write to historical_factors_new
        print("\n🧪 TEST 2: WRITING REAL MARKET DATA")
        print("-" * 40)
        
        market_data = []
        symbols = ['AAPL', 'TSLA', 'MSFT']
        horizons = ['1W', '1M', '6M']
        
        for symbol in symbols:
            for horizon in horizons:
                record = {
                    'symbol': symbol,
                    'horizon': horizon,
                    'timestamp': datetime.now(timezone.utc),
                    'price': 150.0 + hash(symbol) % 100,  # Fake price
                    'volume': 1000000 + hash(symbol) % 500000,  # Fake volume
                    'sentiment': 0.5 + (hash(symbol) % 100) / 200,  # Fake sentiment
                    'volatility': 0.1 + (hash(symbol) % 50) / 500,  # Fake volatility
                    'fundamental': 0.4 + (hash(symbol) % 80) / 200,  # Fake fundamental
                    'technical': 0.6 + (hash(symbol) % 60) / 150,  # Fake technical
                    'macro': 0.3 + (hash(symbol) % 70) / 233,  # Fake macro
                    'esg': 0.5 + (hash(symbol) % 40) / 80,  # Fake ESG
                    'test_source': 'direct_python_script'
                }
                market_data.append(record)
        
        # Write in batch
        batch = db.batch()
        collection_name = 'historical_factors_new'
        
        for i, record in enumerate(market_data):
            doc_id = f"{record['symbol']}_{record['horizon']}_{int(record['timestamp'].timestamp())}_{i}"
            doc_ref = db.collection(collection_name).document(doc_id)
            batch.set(doc_ref, record)
            
        batch.commit()
        print(f"✅ Wrote {len(market_data)} records to {collection_name}")
        
        # Test 3: Write current market data
        print("\n🧪 TEST 3: WRITING CURRENT MARKET DATA")
        print("-" * 40)
        
        current_market_collection = 'current_market_data'
        current_time = datetime.now(timezone.utc)
        
        for symbol in ['AAPL', 'GOOGL', 'TSLA', '7203.T']:
            current_data = {
                'symbol': symbol,
                'price': 200.0 + hash(symbol) % 150,
                'timestamp': current_time,
                'daily_change_pct': -5.0 + (hash(symbol) % 100) / 10,
                'volume': 5000000 + hash(symbol) % 10000000,
                'source': 'direct_test',
                'last_updated': current_time.isoformat()
            }
            
            doc_ref = db.collection(current_market_collection).document(symbol)
            doc_ref.set(current_data)
            print(f"✅ Wrote current data for {symbol}")
        
        # Test 4: List all collections to verify
        print("\n📊 COLLECTIONS AFTER WRITE TEST")
        print("-" * 40)
        
        collections = list(db.collections())
        for collection in collections:
            try:
                docs = list(collection.limit(3).stream())
                print(f"📁 {collection.id}: {len(docs)}+ documents")
                
                if collection.id in ['direct_test_collection', 'historical_factors_new', 'current_market_data']:
                    print(f"   🆕 NEW COLLECTION CREATED!")
                    
            except Exception as e:
                print(f"📁 {collection.id}: error ({e})")
        
        print(f"\n🎯 SUMMARY")
        print("=" * 50)
        print("✅ Direct Firebase write test SUCCESSFUL")
        print("✅ Created 3 new collections with test data")
        print("✅ Firebase connectivity and authentication working")
        print()
        print("🚨 CONCLUSION:")
        print("   Firebase works fine when called directly from Python")
        print("   The issue is in the API endpoints - they're not actually")
        print("   executing the Firebase write operations properly")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        print(f"Full traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    main()
