#!/usr/bin/env python
"""
Test changing the filter dropdown from "Chave de Acesso" to "Período"
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import nest_asyncio
nest_asyncio.apply()

from playwright.async_api import async_playwright


async def test_filter_change():
    """
    Change the filter dropdown and see what elements appear
    """
    print("\n" + "="*70)
    print("CHANGING FILTER DROPDOWN")
    print("="*70 + "\n")

    async with async_playwright() as p:
        print("[1] Launching browser...")
        browser = await p.chromium.launch(headless=False, slow_mo=500)
        page = await browser.new_page()

        print("[2] Navigating...")
        await page.goto(
            "https://portal-sitram.sefaz.ce.gov.br/sitram-internet/#/pagamento-icms/por-nota-fiscal/fiscal",
            wait_until="domcontentloaded"
        )
        await page.wait_for_load_state('networkidle')
        print("    ✓ Page loaded\n")

        print("[3] Finding 'Filtrar por' dropdown (first p-dropdown)...")
        dropdowns = await page.query_selector_all('p-dropdown')
        print(f"    Found {len(dropdowns)} dropdowns")

        if dropdowns:
            first_dropdown = dropdowns[0]
            print("\n[4] Clicking first dropdown to open options...")
            await first_dropdown.click()
            await page.wait_for_timeout(1000)

            print("[5] Looking for 'Período' option...")
            # Find all options in the dropdown menu
            options = await page.query_selector_all('.p-dropdown-items-wrapper li')
            print(f"    Found {len(options)} options in dropdown\n")

            if options:
                print("    Available options:")
                for i, opt in enumerate(options):
                    try:
                        text = await opt.text_content()
                        print(f"      [{i}] {text.strip()}")
                    except:
                        pass

                print("\n[6] Looking for and clicking 'Período' option...")
                periodo_option = None
                for opt in options:
                    text = await opt.text_content()
                    if 'período' in text.lower() or 'periodo' in text.lower():
                        periodo_option = opt
                        break

                if periodo_option:
                    await periodo_option.click()
                    print("    ✓ Clicked 'Período'")
                    await page.wait_for_timeout(2000)  # Wait for new fields to appear

                    print("\n[7] Page updated! Analyzing new elements...")
                    inputs = await page.query_selector_all('input')
                    print(f"    Now have {len(inputs)} input fields\n")

                    print("    Input fields:")
                    for i, inp in enumerate(inputs):
                        try:
                            placeholder = await inp.get_attribute('placeholder')
                            print(f"      [{i}] placeholder={placeholder}")
                        except:
                            pass

                    # Get updated HTML
                    html = await page.content()
                    with open("/tmp/sitram_after_filter_change.html", "w") as f:
                        f.write(html)
                    print("\n    ✓ New HTML saved: /tmp/sitram_after_filter_change.html")

                else:
                    print("    ✗ 'Período' option not found!")
                    print("    Let me show you ALL available options in the dropdown...")

        print("\n[8] Browser will stay open - Inspect the page!")
        print("    Press ENTER to close...")
        input(">> ")

        await browser.close()


if __name__ == "__main__":
    asyncio.run(test_filter_change())
