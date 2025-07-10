#!/usr/bin/env python3
"""
Test script for Google Sheets integration
Run this after setting up new credentials
"""

import asyncio
import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
from services import GoogleSheetsService

# Load environment variables
load_dotenv()

async def test_google_sheets():
    """Test Google Sheets integration"""
    print("🧪 Testing Google Sheets Integration...")
    
    # Initialize service
    sheets_service = GoogleSheetsService()
    
    try:
        # Test 1: Setup headers
        print("\n1. Testing headers setup...")
        success = await sheets_service.create_headers_if_needed()
        if success:
            print("✅ Headers setup successful")
        else:
            print("❌ Headers setup failed")
            return
        
        # Test 2: Add test complaint
        print("\n2. Testing complaint addition...")
        test_complaint = {
            "id": 999,
            "text": "Test complaint for integration verification",
            "category": "Test",
            "sentiment": "neutral",
            "status": "open",
            "created_at": "2025-07-09 23:45:00",
            "ip_address": "127.0.0.1",
            "is_spam": False
        }
        
        success = await sheets_service.add_complaint_to_sheet(test_complaint)
        if success:
            print("✅ Test complaint added successfully")
        else:
            print("❌ Failed to add test complaint")
            return
        
        # Test 3: Get summary
        print("\n3. Testing summary retrieval...")
        summary = await sheets_service.get_complaints_summary()
        if summary:
            print("✅ Summary retrieved successfully")
            print(f"   Total rows: {summary.get('total_rows', 'N/A')}")
            print(f"   Last updated: {summary.get('last_updated', 'N/A')}")
        else:
            print("❌ Failed to get summary")
        
        print("\n🎉 All Google Sheets tests completed!")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        print("\n🔧 Troubleshooting tips:")
        print("1. Check if google-credentials.json exists in project root")
        print("2. Verify GOOGLE_SPREADSHEET_ID in .env file")
        print("3. Ensure service account has Editor access to the sheet")
        print("4. Check if Google Sheets API is enabled in Google Cloud Console")

if __name__ == "__main__":
    asyncio.run(test_google_sheets()) 