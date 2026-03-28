#!/usr/bin/env python
"""
Manual testing script - Opens browser so you can see what's happening
Run with: source venv/bin/activate && python manual_test.py
"""
import asyncio
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

import nest_asyncio
nest_asyncio.apply()

from playwright.async_api import async_playwright


async def manual_test():
    """
    Opens browser in NON-headless mode so you can see everything
    """
    print("\n" + "="*60)
    print("SITRAM MANUAL TEST - Browser will stay open for you to control")
    print("="*60 + "\n")

    async with async_playwright() as p:
        # IMPORTANT: headless=False so you can SEE the browser!
        print("[1/6] Launching Chromium (browser will open in window)...")
        browser = await p.chromium.launch(headless=False, slow_mo=1000)

        page = await browser.new_page()

        print("[2/6] Navigating to SITRAM portal...")
        await page.goto(
            "https://portal-sitram.sefaz.ce.gov.br/sitram-internet/#/pagamento-icms/por-nota-fiscal/fiscal",
            wait_until="domcontentloaded"
        )

        print(f"      ✓ Current URL: {page.url}")
        await page.wait_for_load_state('networkidle')
        print("      ✓ Page fully loaded\n")

        # Find inputs and buttons for debugging
        print("[3/6] Analyzing page elements...")
        inputs = await page.query_selector_all('input')
        buttons = await page.query_selector_all('button')
        print(f"      ✓ Found {len(inputs)} input fields")
        print(f"      ✓ Found {len(buttons)} buttons\n")

        # Print input field info
        print("      Input fields:")
        for i, inp in enumerate(inputs):
            placeholder = await inp.get_attribute('placeholder')
            inp_type = await inp.get_attribute('type')
            print(f"        [{i}] type={inp_type}, placeholder={placeholder}")

        print("\n      Buttons:")
        for i, btn in enumerate(buttons):
            text = await btn.text_content()
            inner = await btn.inner_html()
            print(f"        [{i}] {text.strip()}")

        # Get page HTML
        print("\n[4/6] Generating Playwright code generator...")
        print("\n" + "="*60)
        print("NEXT STEPS - YOU HAVE OPTIONS:")
        print("="*60)
        print("\nOption A - Use Playwright Inspector (Interactive Recording):")
        print("  1. Press CTRL+SHIFT+R in the browser to open Playwright Inspector")
        print("  2. The inspector records your actions as Playwright code")
        print("  3. Do these manual steps:")
        print("     a) Fill in Start Date (data.start_date = '01/12/2025')")
        print("     b) Fill in End Date (data.end_date = '31/12/2025')")
        print("     c) Fill in CNPJ (data.cnpj = '23602073000159')")
        print("     d) Click Search button")
        print("     e) Wait for results")
        print("     f) Find and click CSV download button")
        print("  4. Copy the generated code and paste in playwright_service.py")

        print("\nOption B - Tell me to analyze the page:")
        print("  1. Keep browser open")
        print("  2. Check the page structure manually")
        print("  3. Tell me what fields you see and their IDs/names")
        print("  4. I'll update the code")

        print("\nOption C - Automated inspection (my script will try):")
        print("  1. Press Enter to continue...")
        input("  >> ")

        print(f"\n[5/6] Taking screenshot for analysis...")
        await page.screenshot(path="/tmp/sitram_manual_test.png")
        print(f"      ✓ Screenshot saved: /tmp/sitram_manual_test.png")

        # Try to get DOM structure
        print(f"\n[6/6] Saving page HTML for analysis...")
        html = await page.content()
        with open("/tmp/sitram_page.html", "w") as f:
            f.write(html)
        print(f"      ✓ HTML saved: /tmp/sitram_page.html ({len(html)} bytes)")

        print("\n" + "="*60)
        print("Browser will stay open - You can:")
        print("  1. Inspect elements (F12)")
        print("  2. Fill the form manually to see selectors")
        print("  3. Open console and check elements")
        print("  4. Copy element selectors/IDs")
        print("\nPress ENTER to close browser and exit...")
        print("="*60 + "\n")
        input(">> ")

        await browser.close()
        print("\n✓ Browser closed")


if __name__ == "__main__":
    asyncio.run(manual_test())
