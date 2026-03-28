#!/usr/bin/env python
"""
Deep page inspection - Find exact selectors and element structure
"""
import asyncio
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import nest_asyncio
nest_asyncio.apply()

from playwright.async_api import async_playwright


async def inspect_page():
    """
    Deep inspection of the SITRAM page
    """
    print("\n" + "="*70)
    print("DEEP PAGE INSPECTION")
    print("="*70 + "\n")

    async with async_playwright() as p:
        print("[1] Launching browser...")
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        print("[2] Navigating...")
        await page.goto(
            "https://portal-sitram.sefaz.ce.gov.br/sitram-internet/#/pagamento-icms/por-nota-fiscal/fiscal",
            wait_until="domcontentloaded"
        )
        await page.wait_for_load_state('networkidle')
        print("    ✓ Page loaded\n")

        # Extract all inputs with details
        print("[3] ALL INPUT FIELDS:")
        print("-" * 70)
        inputs = await page.query_selector_all('input')
        for i, inp in enumerate(inputs):
            try:
                inp_id = await inp.get_attribute('id')
                inp_name = await inp.get_attribute('name')
                inp_type = await inp.get_attribute('type')
                placeholder = await inp.get_attribute('placeholder')
                aria_label = await inp.get_attribute('aria-label')

                print(f"\nInput [{i}]:")
                print(f"  id={inp_id}")
                print(f"  name={inp_name}")
                print(f"  type={inp_type}")
                print(f"  placeholder={placeholder}")
                print(f"  aria-label={aria_label}")

                # Selector strategy
                if inp_id:
                    print(f"  selector: #{inp_id}")
                elif inp_name:
                    print(f"  selector: input[name='{inp_name}']")
                elif placeholder:
                    print(f"  selector: input[placeholder*='{placeholder[:20]}']")
                elif aria_label:
                    print(f"  selector: input[aria-label='{aria_label}']")
            except Exception as e:
                print(f"Input [{i}] - Error: {e}")

        # Extract all buttons with details
        print("\n\n[4] ALL BUTTONS:")
        print("-" * 70)
        buttons = await page.query_selector_all('button')
        for i, btn in enumerate(buttons):
            try:
                btn_id = await btn.get_attribute('id')
                btn_class = await btn.get_attribute('class')
                text = await btn.text_content()
                aria_label = await btn.get_attribute('aria-label')

                print(f"\nButton [{i}]:")
                print(f"  text={text.strip()}")
                print(f"  id={btn_id}")
                print(f"  class={btn_class}")
                print(f"  aria-label={aria_label}")

                # Selector strategy
                if text.strip():
                    print(f"  selector: button:has-text('{text.strip()}')")
                if btn_id:
                    print(f"  selector: #{btn_id}")
            except Exception as e:
                print(f"Button [{i}] - Error: {e}")

        # Look for dropdowns - fix the selector issue
        print("\n\n[5] DROPDOWN/SELECT ELEMENTS:")
        print("-" * 70)
        try:
            # Query each selector individually
            p_dropdowns = await page.query_selector_all('p-dropdown')
            selects = await page.query_selector_all('select')
            comboboxes = await page.query_selector_all('[role="combobox"]')

            all_dropdowns = p_dropdowns + selects + comboboxes

            if all_dropdowns:
                for i, dd in enumerate(all_dropdowns):
                    try:
                        id_attr = await dd.get_attribute('id')
                        text = await dd.text_content()
                        tag = await dd.evaluate('el => el.tagName')
                        print(f"\nDropdown [{i}] ({tag}):")
                        print(f"  id={id_attr}")
                        print(f"  text={text.strip()[:80]}")
                    except Exception as e:
                        print(f"Dropdown [{i}] - Error: {e}")
            else:
                print("No standard dropdowns found (p-dropdown, select, [role=combobox])")
        except Exception as e:
            print(f"Error finding dropdowns: {e}")

        # Look for form labels
        print("\n\n[6] FORM LABELS:")
        print("-" * 70)
        labels = await page.query_selector_all('label')
        for i, label in enumerate(labels[:10]):  # First 10 labels
            try:
                text = await label.text_content()
                label_for = await label.get_attribute('for')
                print(f"  [{i}] {text.strip()} (for={label_for})")
            except:
                pass

        # Save detailed HTML analysis
        print("\n\n[7] Saving detailed analysis...")
        html = await page.content()

        analysis = {
            "url": page.url,
            "inputs_count": len(inputs),
            "buttons_count": len(buttons),
            "page_size": len(html),
            "has_angular": "ng-" in html or "angular" in html.lower(),
            "has_primeng": "p-dropdown" in html or "p-calendar" in html,
        }

        # Save JSON analysis
        with open("/tmp/sitram_analysis.json", "w") as f:
            json.dump(analysis, f, indent=2)

        # Save HTML
        with open("/tmp/sitram_detailed.html", "w") as f:
            f.write(html)

        print(f"    ✓ Analysis saved to /tmp/sitram_analysis.json")
        print(f"    ✓ HTML saved to /tmp/sitram_detailed.html")

        # Print analysis
        print("\n[8] PAGE ANALYSIS:")
        print("-" * 70)
        for key, value in analysis.items():
            print(f"  {key}: {value}")

        await browser.close()

        print("\n" + "="*70)
        print("Analysis complete!")
        print("Files generated:")
        print("  - /tmp/sitram_analysis.json  (structured data)")
        print("  - /tmp/sitram_detailed.html  (full page source)")
        print("="*70 + "\n")


if __name__ == "__main__":
    asyncio.run(inspect_page())
