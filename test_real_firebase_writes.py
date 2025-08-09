#!/usr/bin/env python3
"""
TEST REAL FIREBASE WRITES
=========================

This script tests if the API endpoints are actually writing to Firebase
by checking before/after document counts and timestamps.
"""

import requests
import json
from datetime import datetime
import time

def get_firebase_status():
    """Get current Firebase status"""
    try:
        response = requests.get("https://uptrendr-api-626448778297.asia-northeast1.run.app/test-firebase")
        if response.status_code == 200:
            data = response.json()
            collections = {c['name']: c for c in data.get('collections', [])}
            return collections
        else:
            print(f"❌ Failed to get Firebase status: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error getting Firebase status: {e}")
        return None

def main():
    print("🔍 TESTING REAL FIREBASE WRITES")
    print("=" * 50)
    print(f"📅 Started at: {datetime.now()}")
    print()
    
    # Step 1: Get initial state
    print("📊 STEP 1: Getting initial Firebase state")
    initial_state = get_firebase_status()
    if not initial_state:
        print("❌ Could not get initial state")
        return
    
    print(f"✅ Found {len(initial_state)} collections initially")
    for name, info in initial_state.items():
        if 'historical' in name:
            print(f"   📁 {name}: {info['document_count']} documents")
    
    # Step 2: Call the API endpoint
    print("\n🚀 STEP 2: Calling /populate-data endpoint")
    try:
        response = requests.post("https://uptrendr-api-626448778297.asia-northeast1.run.app/populate-data")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Response: {data.get('message', 'No message')}")
            print(f"   📄 Records claimed: {data.get('records_created', 'Unknown')}")
            print(f"   ⏰ Timestamp: {data.get('timestamp', 'Unknown')}")
        else:
            print(f"❌ API call failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return
    except Exception as e:
        print(f"❌ Error calling API: {e}")
        return
    
    # Step 3: Wait a moment for writes to propagate
    print("\n⏳ STEP 3: Waiting 3 seconds for writes to propagate...")
    time.sleep(3)
    
    # Step 4: Get final state
    print("\n📊 STEP 4: Getting final Firebase state")
    final_state = get_firebase_status()
    if not final_state:
        print("❌ Could not get final state")
        return
    
    print(f"✅ Found {len(final_state)} collections after API call")
    
    # Step 5: Compare states
    print("\n🔍 STEP 5: Comparing before/after states")
    print("-" * 40)
    
    changes_detected = False
    
    # Check for new collections
    new_collections = set(final_state.keys()) - set(initial_state.keys())
    if new_collections:
        changes_detected = True
        print(f"✅ NEW COLLECTIONS: {list(new_collections)}")
    
    # Check for changed document counts
    for name in initial_state:
        if name in final_state:
            initial_count = initial_state[name]['document_count']
            final_count = final_state[name]['document_count']
            
            if initial_count != final_count:
                changes_detected = True
                print(f"✅ COLLECTION UPDATED: {name}")
                print(f"   📊 Before: {initial_count} documents")
                print(f"   📊 After: {final_count} documents")
            elif 'historical' in name:
                print(f"❌ NO CHANGE: {name} still has {initial_count} documents")
    
    # Step 6: Final verdict
    print("\n" + "=" * 50)
    print("🎯 FINAL VERDICT")
    print("=" * 50)
    
    if changes_detected:
        print("✅ SUCCESS: Firebase was actually updated!")
        print("   The API endpoints are working correctly.")
    else:
        print("❌ FAILURE: No changes detected in Firebase!")
        print("   The API endpoints are still giving fake responses.")
        print("   Despite claiming to write 900 records, nothing changed.")
    
    print(f"\n📅 Test completed at: {datetime.now()}")

if __name__ == "__main__":
    main()
