#!/usr/bin/env python3
"""Verify we have all 15 expected collections"""

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

# Your 15 expected collections
expected_15 = [
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

print("🎯 VERIFYING YOUR 15 EXPECTED COLLECTIONS")
print("=" * 50)

# Get all current collections
current_collections = [c.id for c in db.collections()]

print(f"📊 Checking for all 15 expected collections:")
missing = []
found = []

for i, collection_name in enumerate(expected_15, 1):
    if collection_name in current_collections:
        print(f"   {i:2d}. ✅ {collection_name}")
        found.append(collection_name)
    else:
        print(f"   {i:2d}. ❌ {collection_name} - MISSING")
        missing.append(collection_name)

print(f"\n📈 RESULTS:")
print(f"   ✅ Found: {len(found)}/15 expected collections")
print(f"   ❌ Missing: {len(missing)} collections")

if missing:
    print(f"   Missing collections: {missing}")

if len(found) == 15:
    print(f"\n🎉 SUCCESS: All 15 expected collections are present!")
    print(f"\n🔥 Your Firebase database now contains:")
    for i, name in enumerate(sorted(found), 1):
        print(f"   {i:2d}. {name}")
else:
    print(f"\n⚠️ STATUS: {len(found)}/15 collections found")

# Check for extra collections
extra = [c for c in current_collections if c not in expected_15]
if extra:
    print(f"\n📝 Additional collections (can be ignored): {extra}")

print(f"\n📊 Total collections in database: {len(current_collections)}")
print(f"📊 Expected collections found: {len(found)}/15")

if len(found) == 15:
    print(f"\n✅ READY FOR SCHEDULED AUTOMATION!")
else:
    print(f"\n❌ Need to create {len(missing)} missing collections")
