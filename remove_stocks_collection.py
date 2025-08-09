#!/usr/bin/env python3
"""Remove the stocks collection specifically"""

import sys
sys.path.append('/Users/sohntsang/Desktop/Uptrendr/Uptrendr')

from google.cloud import firestore
import firebase_admin

try:
    app = firebase_admin.get_app()
except ValueError:
    from firebase_admin import credentials
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred)

db = firestore.Client()

print("🗑️ Removing 'stocks' collection...")

try:
    # Delete all documents in the stocks collection
    collection_ref = db.collection('stocks')
    docs = list(collection_ref.stream())
    
    if docs:
        batch = db.batch()
        for doc in docs:
            batch.delete(doc.reference)
        batch.commit()
        print(f"✅ Deleted {len(docs)} documents from stocks collection")
    else:
        print("✅ Stocks collection was empty")
    
    # The collection should now be effectively deleted
    print("✅ Stocks collection removed")
    
except Exception as e:
    print(f"❌ Error: {e}")

# Verify final state
final_collections = sorted([c.id for c in db.collections()])
print(f"\n📊 Final collections ({len(final_collections)}):")
for i, name in enumerate(final_collections, 1):
    print(f"   {i:2d}. {name}")

expected_15 = [
    'economic_calendar', 'esg_scores', 'forecast_weights', 'fundamental_analysis',
    'historical_factors', 'japanese_economics', 'japanese_news', 'macro_indicators', 
    'market_data', 'market_predictions', 'ml_training_status', 'model_weights',
    'sentiment_analysis', 'technical_analysis', 'trained_models'
]

if len(final_collections) == 15 and all(c in expected_15 for c in final_collections):
    print(f"\n🎉 SUCCESS: Exactly 15 expected collections!")
else:
    print(f"\n📊 Status: {len(final_collections)} collections total")
    if 'stocks' in final_collections:
        print("⚠️ 'stocks' collection still exists")
    missing = [c for c in expected_15 if c not in final_collections]
    if missing:
        print(f"❌ Missing: {missing}")
    extra = [c for c in final_collections if c not in expected_15]
    if extra:
        print(f"❓ Extra: {extra}")
