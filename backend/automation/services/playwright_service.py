import asyncio
import tempfile
import os
from pathlib import Path
from playwright.async_api import async_playwright, Page, Browser, BrowserContext
import nest_asyncio

# Allow nested async calls for Django context
nest_asyncio.apply()


async def navigate_to_icms_page(page: Page) -> bool:
    """
    Navigate to the ICMS payment page.
    """
    try:
        print(f"[DEBUG] Starting navigation to ICMS page...")
        await page.goto(
            "https://portal-sitram.sefaz.ce.gov.br/sitram-internet/#/pagamento-icms/por-nota-fiscal/fiscal",
            wait_until="domcontentloaded",
            timeout=30000
        )
        print(f"[DEBUG] Page loaded, current URL: {page.url}")

        # Wait for page to be interactive
        await page.wait_for_load_state('networkidle', timeout=15000)
        print(f"[DEBUG] Page fully loaded")

        # Try to find form elements - multiple strategies
        try:
            # Strategy 1: Wait for any p-dropdown (PrimeNG component)
            await page.wait_for_selector("p-dropdown", timeout=10000)
            print(f"[DEBUG] Found p-dropdown elements")
            return True
        except:
            print(f"[DEBUG] p-dropdown not found, trying alternative selectors...")

        # Strategy 2: Look for form or input elements
        try:
            await page.wait_for_selector("input[type='text']", timeout=5000)
            print(f"[DEBUG] Found input elements")
            return True
        except:
            print(f"[DEBUG] input elements not found either")

        # Strategy 3: Just check if page has content
        content = await page.content()
        if len(content) > 500:
            print(f"[DEBUG] Page has content ({len(content)} bytes), assuming loaded")
            return True

        print(f"[DEBUG] Page content too small: {len(content)} bytes")
        return False

    except Exception as e:
        print(f"[ERROR] Navigation error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def fill_search_filters(page: Page, start_date: str, end_date: str, cnpj: str) -> bool:
    """
    Fill the search filters: period and CNPJ.

    Args:
        page: Playwright page object
        start_date: Start date in format DD/MM/YYYY
        end_date: End date in format DD/MM/YYYY
        cnpj: CNPJ in format XX.XXX.XXX/XXXX-XX
    """
    try:
        print(f"[DEBUG] Starting to fill search filters...")

        # Wait for page to have interactive elements
        await page.wait_for_timeout(2000)

        # Try to find and fill CNPJ field
        try:
            print(f"[DEBUG] Looking for CNPJ input field...")
            # Try multiple selectors for CNPJ
            cnpj_input = await page.query_selector('input[placeholder*="38.009"]')
            if not cnpj_input:
                cnpj_input = await page.query_selector('input[placeholder*="CNPJ"]')
            if not cnpj_input:
                cnpj_input = await page.query_selector('input[id*="cnpj"]')
            if not cnpj_input:
                # Try any input with numbers in placeholder
                cnpj_inputs = await page.query_selector_all('input[type="text"]')
                if cnpj_inputs:
                    cnpj_input = cnpj_inputs[-1]  # Try the last text input

            if cnpj_input:
                # Remove formatting from CNPJ for input
                cnpj_clean = cnpj.replace('.', '').replace('/', '').replace('-', '')
                print(f"[DEBUG] Filling CNPJ field with: {cnpj}")
                await cnpj_input.fill(cnpj, delay=50)
                await page.wait_for_timeout(500)
            else:
                print(f"[DEBUG] CNPJ input not found")

        except Exception as e:
            print(f"[ERROR] Error filling CNPJ: {str(e)}")

        # Try to find and interact with date fields
        try:
            print(f"[DEBUG] Looking for date input fields...")
            date_inputs = await page.query_selector_all('input[type="text"]')
            print(f"[DEBUG] Found {len(date_inputs)} text input fields")

            # Try to fill the first few inputs with dates
            if len(date_inputs) >= 2:
                print(f"[DEBUG] Filling date fields...")
                await date_inputs[0].fill(start_date, delay=50)
                await page.wait_for_timeout(300)

                if len(date_inputs) >= 3:
                    await date_inputs[1].fill(end_date, delay=50)
                    await page.wait_for_timeout(300)

        except Exception as e:
            print(f"[ERROR] Error filling dates: {str(e)}")

        print(f"[DEBUG] Finished filling search filters")
        return True

    except Exception as e:
        print(f"[ERROR] Filter fill error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def click_search_button(page: Page) -> bool:
    """
    Click the search button.
    """
    try:
        print(f"[DEBUG] Looking for search button...")

        # Try multiple strategies to find the search button
        search_button = None

        # Strategy 1: Look for button with "Pesquisar" text
        try:
            search_button = await page.query_selector('button:has-text("Pesquisar")')
            if search_button:
                print(f"[DEBUG] Found search button with text 'Pesquisar'")
        except:
            pass

        # Strategy 2: Look for button with magnifying glass icon
        if not search_button:
            try:
                buttons = await page.query_selector_all('button')
                for btn in buttons:
                    text = await btn.text_content()
                    if 'search' in text.lower() or 'pesquisar' in text.lower():
                        search_button = btn
                        print(f"[DEBUG] Found search button by text content: {text}")
                        break
            except:
                pass

        # Strategy 3: Look for any button (might be the search one)
        if not search_button:
            buttons = await page.query_selector_all('button')
            if buttons:
                search_button = buttons[-1]  # Try the last button
                print(f"[DEBUG] Using last button as search button")

        if search_button:
            print(f"[DEBUG] Clicking search button...")
            await search_button.click()
            await page.wait_for_timeout(2000)

            #  Wait for results
            await page.wait_for_load_state('networkidle', timeout=15000)
            print(f"[DEBUG] Results loaded after search")
            return True
        else:
            print(f"[ERROR] Search button not found")
            return False

    except Exception as e:
        print(f"[ERROR] Search button click error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def download_csv(page: Page) -> str:
    """
    Download the CSV file and return its content as a string.
    """
    try:
        print(f"[DEBUG] Looking for CSV download button...")

        # Try multiple strategies to find CSV button
        csv_button = None

        # Strategy 1: Look for button with "CSV" text
        try:
            csv_button = await page.query_selector('button:has-text("CSV")')
            if csv_button:
                print(f"[DEBUG] Found CSV button")
        except:
            pass

        # Strategy 2: Look by icon or other attributes
        if not csv_button:
            buttons = await page.query_selector_all('button')
            for btn in buttons:
                try:
                    text = await btn.text_content()
                    inner = await btn.inner_html()
                    if 'csv' in text.lower() or 'csv' in inner.lower():
                        csv_button = btn
                        print(f"[DEBUG] Found CSV button by content: {text}")
                        break
                except:
                    pass

        if csv_button:
            print(f"[DEBUG] Clicking CSV download button...")

            # Set up download listener
            async with page.expect_download(timeout=30000) as download_info:
                await csv_button.click()

            download = await download_info.value
            print(f"[DEBUG] Download started: {download.suggested_filename}")

            # Save to temporary file
            with tempfile.NamedTemporaryFile(mode='w+b', delete=False, suffix='.csv') as tmp:
                tmp.write(await download.body())
                tmp_path = tmp.name

            # Read CSV content
            with open(tmp_path, 'r', encoding='utf-8') as f:
                csv_content = f.read()

            # Clean up temp file
            os.unlink(tmp_path)

            print(f"[DEBUG] CSV downloaded successfully, {len(csv_content)} bytes")
            return csv_content
        else:
            print(f"[ERROR] CSV button not found")
            # Return page content as fallback
            content = await page.content()
            print(f"[DEBUG] Returning page content as fallback ({len(content)} bytes)")
            return ""

    except Exception as e:
        print(f"[ERROR] CSV download error: {str(e)}")
        import traceback
        traceback.print_exc()
        return ""


async def extract_sitram_data(search_params: dict) -> dict:
    """
    Main orchestration function for extracting SITRAM data.

    Args:
        search_params: Dict with 'start_date', 'end_date', 'cnpj'

    Returns:
        Dict with 'success', 'data' (CSV content), and optional 'error'
    """
    browser = None
    try:
        async with async_playwright() as p:
            print(f"[DEBUG] Launching Chromium browser...")
            browser = await p.chromium.launch(headless=True)
            print(f"[DEBUG] Browser launched successfully")

            page = await browser.new_page()

            # Navigate to ICMS page
            print(f"[DEBUG] Navigating to ICMS page...")
            if not await navigate_to_icms_page(page):
                return {
                    'success': False,
                    'error': 'Failed to navigate to ICMS page.'
                }

            # Fill filters
            start_date = search_params.get('start_date')
            end_date = search_params.get('end_date')
            cnpj = search_params.get('cnpj')

            print(f"[DEBUG] Filling search filters... Start: {start_date}, End: {end_date}, CNPJ: {cnpj}")
            if not await fill_search_filters(page, start_date, end_date, cnpj):
                return {
                    'success': False,
                    'error': 'Failed to fill search filters.'
                }

            # Click search
            print(f"[DEBUG] Clicking search button...")
            if not await click_search_button(page):
                return {
                    'success': False,
                    'error': 'Failed to perform search.'
                }

            # Download CSV
            print(f"[DEBUG] Downloading CSV...")
            csv_content = await download_csv(page)

            if not csv_content:
                return {
                    'success': False,
                    'error': 'Failed to download CSV.'
                }

            print(f"[DEBUG] CSV downloaded successfully, size: {len(csv_content)} bytes")
            return {
                'success': True,
                'data': csv_content
            }

    except Exception as e:
        print(f"[ERROR] Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            'success': False,
            'error': f'Unexpected error: {str(e)}'
        }

    finally:
        if browser:
            try:
                await browser.close()
                print(f"[DEBUG] Browser closed")
            except:
                pass


# Wrapper for sync context
def extract_sitram_data_sync(search_params: dict) -> dict:
    """
    Synchronous wrapper for extract_sitram_data.
    """
    return asyncio.run(extract_sitram_data(search_params))
