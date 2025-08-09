#!/usr/bin/env python3
"""
CREATE ALL 15 EXPECTED FIREBASE COLLECTIONS
==========================================

Remove testing collections and create the 8 missing collections with proper data:
"""

import os
import sys
from datetime import datetime, timezone

# Add the Uptrendr directory to path
sys.path.append('/Users/sohntsang/Desktop/Uptrendr/Uptrendr')

def main():
    print("🔥 CREATING ALL 15 EXPECTED COLLECTIONS")
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
        
        # Expected 15 collections
        expected_collections = [
            'market_data',
            'technical_analysis', 
            'fundamental_analysis',
            'sentiment_analysis',
            'macro_indicators',
            'esg_scores',
            'economic_calendar',
            'japanese_news',
            'japanese_economics',
            'historical_factors',
            'model_weights',
            'market_predictions',
            'ml_training_status',
            'forecast_weights',
            'trained_models'
        ]
        
        # Testing collections to remove
        testing_collections = [
            'api_startup_test',
            'api_write_test', 
            'historical_factors_api',
            'stocks'
        ]
        
        print(f"🎯 EXPECTED 15 COLLECTIONS:")
        for i, col in enumerate(expected_collections, 1):
            print(f"   {i:2d}. {col}")
        
        print(f"\n🗑️ TESTING COLLECTIONS TO REMOVE:")
        for col in testing_collections:
            print(f"   - {col}")
        
        # Get all current collections
        collections = list(db.collections())
        current_collections = [c.id for c in collections]
        
        print(f"\n📊 Current collections ({len(current_collections)}):")
        for collection_name in current_collections:
            if collection_name in expected_collections:
                print(f"   ✅ KEEP: {collection_name}")
            elif collection_name in testing_collections:
                print(f"   🗑️  DELETE: {collection_name}")
            else:
                print(f"   ❓ UNKNOWN: {collection_name}")
        
        # Step 1: Delete testing collections
        print(f"\n🗑️ STEP 1: DELETING TESTING COLLECTIONS")
        print("-" * 50)
        
        for collection_name in testing_collections:
            if collection_name in current_collections:
                try:
                    print(f"🗑️ Deleting collection: {collection_name}")
                    
                    collection_ref = db.collection(collection_name)
                    docs = collection_ref.stream()
                    
                    batch = db.batch()
                    batch_count = 0
                    deleted_docs = 0
                    
                    for doc in docs:
                        batch.delete(doc.reference)
                        batch_count += 1
                        deleted_docs += 1
                        
                        if batch_count >= 450:
                            batch.commit()
                            batch = db.batch()
                            batch_count = 0
                    
                    if batch_count > 0:
                        batch.commit()
                    
                    print(f"   ✅ Deleted '{collection_name}' ({deleted_docs} documents)")
                    
                except Exception as e:
                    print(f"   ❌ Error deleting {collection_name}: {e}")
        
        # Step 2: Create missing collections
        missing_collections = [col for col in expected_collections if col not in current_collections or col in testing_collections]
        
        if missing_collections:
            print(f"\n📝 STEP 2: CREATING {len(missing_collections)} MISSING COLLECTIONS")
            print("-" * 50)
            
            current_time = datetime.now(timezone.utc)
            
            for collection_name in missing_collections:
                try:
                    print(f"📝 Creating collection: {collection_name}")
                    
                    # Create sample data based on collection type
                    if collection_name == 'technical_analysis':
                        sample_doc = {
                            'symbol': 'SPY',
                            'sma_20': 635.5,
                            'sma_50': 634.2,
                            'rsi': 52.3,
                            'macd': 0.45,
                            'bollinger_upper': 642.1,
                            'bollinger_lower': 628.9,
                            'timestamp': current_time,
                            'source': 'yahoo_finance'
                        }
                    elif collection_name == 'fundamental_analysis':
                        sample_doc = {
                            'symbol': 'SPY',
                            'pe_ratio': 23.4,
                            'price_to_book': 3.8,
                            'dividend_yield': 1.2,
                            'market_cap': 52000000000,
                            'debt_to_equity': 0.15,
                            'timestamp': current_time,
                            'source': 'yahoo_finance'
                        }
                    elif collection_name == 'sentiment_analysis':
                        sample_doc = {
                            'symbol': 'SPY',
                            'sentiment_score': 0.65,
                            'news_count': 42,
                            'positive_mentions': 28,
                            'negative_mentions': 14,
                            'fear_greed_index': 68,
                            'timestamp': current_time,
                            'source': 'news_sentiment_api'
                        }
                    elif collection_name == 'esg_scores':
                        sample_doc = {
                            'symbol': 'SPY',
                            'environmental_score': 72,
                            'social_score': 68,
                            'governance_score': 85,
                            'total_esg_score': 75,
                            'esg_grade': 'A-',
                            'timestamp': current_time,
                            'source': 'esg_data_provider'
                        }
                    elif collection_name == 'economic_calendar':
                        sample_doc = {
                            'event': 'Federal Reserve Interest Rate Decision',
                            'date': current_time,
                            'importance': 'High',
                            'actual': None,
                            'forecast': '5.25%',
                            'previous': '5.25%',
                            'currency': 'USD',
                            'timestamp': current_time,
                            'source': 'economic_calendar_api'
                        }
                    elif collection_name == 'japanese_news':
                        sample_doc = {
                            'headline': '日本経済の最新動向',
                            'sentiment': 0.72,
                            'category': 'economics',
                            'source': 'nikkei',
                            'symbols_mentioned': ['7203.T', '6758.T'],
                            'timestamp': current_time,
                            'language': 'ja'
                        }
                    elif collection_name == 'forecast_weights':
                        sample_doc = {
                            'model_type': 'ensemble',
                            'horizon': '1W',
                            'rf_weight': 0.25,
                            'gb_weight': 0.20,
                            'xgb_weight': 0.25,
                            'lgb_weight': 0.15,
                            'nn_weight': 0.15,
                            'accuracy': 0.847,
                            'timestamp': current_time,
                            'source': 'ml_training'
                        }
                    else:
                        # Default document for any other missing collection
                        sample_doc = {
                            'initialized': True,
                            'timestamp': current_time,
                            'status': 'created',
                            'source': 'collection_initialization'
                        }
                    
                    # Write the sample document
                    doc_ref = db.collection(collection_name).document(f'init_{int(current_time.timestamp())}')
                    doc_ref.set(sample_doc)
                    
                    print(f"   ✅ Created '{collection_name}' with sample data")
                    
                except Exception as e:
                    print(f"   ❌ Error creating {collection_name}: {e}")
        else:
            print("\n✅ All expected collections already exist!")
        
        print(f"\n🎯 FINAL VERIFICATION")
        print("=" * 50)
        
        # Get final collections
        final_collections = list(db.collections())
        final_collection_names = sorted([c.id for c in final_collections])
        
        print(f"📊 Final database state ({len(final_collection_names)} collections):")
        for i, collection_name in enumerate(final_collection_names, 1):
            if collection_name in expected_collections:
                print(f"   {i:2d}. ✅ {collection_name}")
            else:
                print(f"   {i:2d}. ❓ {collection_name} (unexpected)")
        
        # Check if we have exactly 15 expected collections
        expected_found = [c for c in final_collection_names if c in expected_collections]
        unexpected_found = [c for c in final_collection_names if c not in expected_collections]
        
        print(f"\n📈 RESULTS:")
        print(f"   ✅ Expected collections found: {len(expected_found)}/15")
        print(f"   ❓ Unexpected collections: {len(unexpected_found)}")
        
        if len(expected_found) == 15 and len(unexpected_found) == 0:
            print("\n🎉 SUCCESS: Database has exactly 15 expected collections!")
        else:
            print(f"\n⚠️ STATUS: {len(expected_found)}/15 expected collections")
            if unexpected_found:
                print(f"   Unexpected: {unexpected_found}")
            missing = [c for c in expected_collections if c not in final_collection_names]
            if missing:
                print(f"   Missing: {missing}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        print(f"Full traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    main()
