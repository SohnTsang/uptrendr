#!/usr/bin/env python3
"""Remove the stocks collection to get exactly 5 core collections"""

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

# Delete the stocks collection
collection_ref = db.collection('stocks')
docs = list(collection_ref.stream())

print(f"🗑️ Deleting 'stocks' collection ({len(docs)} documents)")

if docs:
    batch = db.batch()
    for doc in docs:
        batch.delete(doc.reference)
    batch.commit()

print("✅ Stocks collection deleted")

# Verify final state
final_collections = [c.id for c in db.collections()]
print(f"📊 Final collections ({len(final_collections)}): {sorted(final_collections)}")

if len(final_collections) == 5:
    print("🎉 SUCCESS: Exactly 5 core collections remain!")
else:
    print(f"⚠️ Expected 5, found {len(final_collections)}")
