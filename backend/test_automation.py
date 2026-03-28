#!/usr/bin/env python
"""
Debug script to test SITRAM automation
"""
import asyncio
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

import nest_asyncio
nest_asyncio.apply()

from automation.services.playwright_service import (
    navigate_to_icms_page,
    fill_search_filters,
    click_search_button,
    extract_sitram_data_sync
)
from playwright.async_api import async_playwright


async def test_navigation():
    """Test if we can navigate to the ICMS page"""
    print("[TEST] Starting navigation test...")

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            success = await navigate_to_icms_page(page)

            if success:
                print("[✓] Navigation successful!")
                print(f"[INFO] Current URL: {page.url}")

                # Take screenshot for debugging
                await page.screenshot(path="/tmp/sitram_page.png")
                print("[INFO] Screenshot saved to /tmp/sitram_page.png")

                # Get page content
                content = await page.content()
                print(f"[INFO] Page content size: {len(content)} bytes")

                # Try to find inputs
                inputs = await page.query_selector_all('input')
                print(f"[INFO] Found {len(inputs)} input fields")

                buttons = await page.query_selector_all('button')
                print(f"[INFO] Found {len(buttons)} buttons")

            else:
                print("[✗] Navigation failed")

            await browser.close()

    except Exception as e:
        print(f"[ERROR] Test failed: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_navigation())
