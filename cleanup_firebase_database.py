#!/usr/bin/env python3
"""
CLEANUP FIREBASE DATABASE
=========================

Remove all testing collections and keep only the 5 core ML collections:
1. historical_factors
2. model_weights  
3. market_predictions
4. ml_training_status
5. trained_models
"""

import os
import sys
from datetime import datetime, timezone

# Add the Uptrendr directory to path
sys.path.append('/Users/sohntsang/Desktop/Uptrendr/Uptrendr')

def main():
    print("🧹 CLEANING UP FIREBASE DATABASE")
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
        
        # Core collections to KEEP
        keep_collections = {
            'historical_factors',
            'model_weights', 
            'market_predictions',
            'ml_training_status',
            'trained_models'
        }
        
        print(f"\n🎯 CORE COLLECTIONS TO KEEP: {list(keep_collections)}")
        print("-" * 50)
        
        # Get all current collections
        collections = list(db.collections())
        current_collections = [c.id for c in collections]
        
        print(f"📊 Current collections ({len(current_collections)}):")
        for collection_name in current_collections:
            if collection_name in keep_collections:
                print(f"   ✅ KEEP: {collection_name}")
            else:
                print(f"   🗑️  DELETE: {collection_name}")
        
        # Collections to delete
        collections_to_delete = [c for c in current_collections if c not in keep_collections]
        
        if not collections_to_delete:
            print("\n✅ Database is already clean! No collections to delete.")
            return
        
        print(f"\n🗑️  DELETING {len(collections_to_delete)} COLLECTIONS")
        print("-" * 50)
        
        for collection_name in collections_to_delete:
            try:
                print(f"🗑️  Deleting collection: {collection_name}")
                
                # Get all documents in the collection
                collection_ref = db.collection(collection_name)
                docs = collection_ref.stream()
                
                # Delete all documents in batches
                batch = db.batch()
                batch_count = 0
                deleted_docs = 0
                
                for doc in docs:
                    batch.delete(doc.reference)
                    batch_count += 1
                    deleted_docs += 1
                    
                    # Commit batch when it reaches 450 (Firebase limit is 500)
                    if batch_count >= 450:
                        batch.commit()
                        print(f"   📄 Deleted {batch_count} documents...")
                        batch = db.batch()
                        batch_count = 0
                
                # Commit remaining documents
                if batch_count > 0:
                    batch.commit()
                    print(f"   📄 Deleted {batch_count} documents...")
                
                print(f"   ✅ Deleted collection '{collection_name}' ({deleted_docs} documents)")
                
            except Exception as e:
                print(f"   ❌ Error deleting {collection_name}: {e}")
        
        print(f"\n🧹 CLEANUP COMPLETE")
        print("=" * 50)
        
        # Verify final state
        final_collections = list(db.collections())
        final_collection_names = [c.id for c in final_collections]
        
        print(f"📊 Final database state ({len(final_collection_names)} collections):")
        for collection_name in final_collection_names:
            docs = list(collection_name for collection_name in final_collection_names if collection_name in keep_collections)
            print(f"   ✅ {collection_name}")
        
        if len(final_collection_names) == 5 and all(c in keep_collections for c in final_collection_names):
            print("\n🎉 SUCCESS: Database cleaned to exactly 5 core collections!")
        else:
            print(f"\n⚠️  WARNING: Expected 5 collections, found {len(final_collection_names)}")
            unexpected = [c for c in final_collection_names if c not in keep_collections]
            if unexpected:
                print(f"   Unexpected collections: {unexpected}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        print(f"Full traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    main()
