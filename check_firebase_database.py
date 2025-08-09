#!/usr/bin/env python3
"""
CHECK FIREBASE DATABASE STATUS
==============================

This script directly checks what's in the Firebase database to see
what collections exist and their data.
"""

import os
import sys
from datetime import datetime, timezone

# Add the Uptrendr directory to path to import modules
sys.path.append('/Users/sohntsang/Desktop/Uptrendr/Uptrendr')

def main():
    print("🔍 CHECKING FIREBASE DATABASE STATUS")
    print("=" * 50)
    print(f"📅 Checked at: {datetime.now()}")
    print(f"🎯 Project: uptrendr-jp")
    print()
    
    try:
        # Import Firebase modules
        from google.cloud import firestore
        from firebase_admin import initialize_app, credentials
        
        print("✅ Firebase modules imported successfully")
        
        # Initialize Firebase
        try:
            # Try to get existing app
            import firebase_admin
            app = firebase_admin.get_app()
            print("✅ Firebase app already initialized")
        except ValueError:
            # Initialize new app
            cred = credentials.ApplicationDefault()
            firebase_admin.initialize_app(cred)
            print("✅ Firebase app initialized with Application Default Credentials")
        
        # Get Firestore client
        db = firestore.Client()
        print("✅ Firestore client created")
        
        # List all collections
        print("\n📊 CHECKING FIRESTORE COLLECTIONS")
        print("-" * 40)
        
        collections = db.collections()
        collection_list = []
        
        for collection in collections:
            collection_name = collection.id
            collection_list.append(collection_name)
            
            # Count documents in each collection
            try:
                docs = list(collection.limit(10).stream())
                doc_count = len(docs)
                
                if doc_count > 0:
                    # Get first document to show sample data
                    first_doc = docs[0]
                    sample_data = first_doc.to_dict()
                    
                    print(f"📁 {collection_name}")
                    print(f"   📄 Documents: {doc_count}+ (showing first 10)")
                    print(f"   🔑 Sample keys: {list(sample_data.keys())[:5]}")
                    
                    # Show timestamp if available
                    if 'timestamp' in sample_data:
                        print(f"   ⏰ Latest: {sample_data['timestamp']}")
                    elif 'updated' in sample_data:
                        print(f"   ⏰ Latest: {sample_data['updated']}")
                    
                    print()
                else:
                    print(f"📁 {collection_name} (EMPTY)")
                    
            except Exception as e:
                print(f"📁 {collection_name} (ERROR: {e})")
        
        # Summary
        print("=" * 50)
        print("📋 SUMMARY")
        print("=" * 50)
        print(f"📊 Total Collections: {len(collection_list)}")
        
        if collection_list:
            print("📁 Collections found:")
            for i, collection in enumerate(collection_list, 1):
                print(f"   {i}. {collection}")
        else:
            print("❌ NO COLLECTIONS FOUND!")
            print("   This means the database is completely empty.")
            
        # Test write operation
        print("\n🧪 TESTING WRITE OPERATION")
        print("-" * 40)
        
        try:
            test_ref = db.collection('test_collection').document('test_doc')
            test_data = {
                'test': True,
                'timestamp': datetime.now(timezone.utc),
                'message': 'Firebase write test'
            }
            
            test_ref.set(test_data)
            print("✅ Write test successful")
            
            # Read it back
            doc = test_ref.get()
            if doc.exists:
                print("✅ Read test successful")
                print(f"   📄 Data: {doc.to_dict()}")
                
                # Clean up
                test_ref.delete()
                print("✅ Cleanup successful")
            else:
                print("❌ Read test failed")
                
        except Exception as e:
            print(f"❌ Write test failed: {e}")
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure Firebase Admin SDK is installed:")
        print("   pip install firebase-admin google-cloud-firestore")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Check your authentication:")
        print("   gcloud auth application-default login")

if __name__ == "__main__":
    main()
