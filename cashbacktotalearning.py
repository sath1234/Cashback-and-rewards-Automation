import re
import json
import requests
from playwright.sync_api import sync_playwright
from typing import Optional

# --- Config ---
CDP_ENDPOINT = "http://127.0.0.1:9222"
CASHBACK_HOST = "shopping.santabrowser.com"
UUID = "d2e3837d66684b7"  # <-- replace with your UUID

# --- API FUNCTION ---
def get_api_total(uuid: str) -> float:
    api_url = f"https://cbapi.santabrowser.com/pull/user/earning?uuid={uuid}"
    try:
        resp = requests.get(api_url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"❌ API request failed: {e}")
        return 0.0

    total = 0.0
    if isinstance(data, dict):
        for key in ["totalEarnings", "total", "amount", "earning", "earnings"]:
            if key in data:
                try:
                    total = float(data[key])
                    break
                except ValueError:
                    pass
    return total


# --- UI FUNCTION ---
def get_ui_total(page) -> Optional[float]:
    try:
        locator = page.locator("p:has-text('$')").last
        locator.wait_for(state="visible", timeout=8000)
        txt = locator.inner_text().strip()
        matches = re.findall(r"\$([0-9,]+(?:\.[0-9]+)?)", txt)
        if matches:
            return float(matches[-1].replace(",", ""))
        if "$0" in txt:
            return 0.0
    except Exception as e:
        print(f"❌ Error extracting UI total: {e}")
        return None
    return None


# --- FIND PAGE ---
def find_cashback_tab(context):
    for page in context.pages:
        if CASHBACK_HOST in page.url:
            return page
    return None


# --- CLICK TOTAL EARNINGS BUTTON ---
def click_total_earnings_button(page):
    """
    Try multiple selectors to click the 'Total Earnings' button reliably.
    """
    selectors = [
        "svg g:has(path[fill='var(--earning-btn-bg)'])",  # Original selector
        "text='Total Earnings'",                         # Text-based fallback
        "button:has-text('Total Earnings')",              # Button fallback
        "div:has-text('Total Earnings')"                  # Div fallback
    ]

    for selector in selectors:
        try:
            btn = page.locator(selector).first
            if btn.count() > 0:
                btn.wait_for(state="visible", timeout=5000)
                btn.click(force=True)
                print(f"✅ Clicked Total Earnings button using selector: {selector}")
                page.wait_for_timeout(2000)
                return True
        except Exception:
            continue

    print("❌ Could not click any 'Total Earnings' button selector.")
    return False


# --- MAIN LOGIC ---
def main():
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp(CDP_ENDPOINT)
            context = browser.contexts[0]
        except Exception as e:
            print(f"❌ Could not connect to browser: {e}")
            return

        cashback_page = find_cashback_tab(context)
        if not cashback_page:
            print("❌ Cashback tab not found.")
            return

        cashback_page.bring_to_front()
        cashback_page.wait_for_load_state("domcontentloaded")

        # 👇 Step 1: Click Total Earnings button first
        clicked = click_total_earnings_button(cashback_page)
        if not clicked:
            print("⚠️ Proceeding without button click (UI may be stale).")

        # 👇 Step 2: Extract UI total
        ui_total = get_ui_total(cashback_page)
        if ui_total is None:
            print("❌ Could not extract UI total earnings.")
            return

        # 👇 Step 3: Fetch API total
        api_total = get_api_total(UUID)

        # 👇 Step 4: Validate
        print("\n✅ Total Earnings Validation")
        print(f"UI Total Earnings: ${ui_total:.2f}")
        print(f"API Total Earnings: ${api_total:.2f}")

        if round(ui_total, 2) == round(api_total, 2):
            print("✅ PASS: UI == API")
        else:
            print("❌ FAIL: UI != API")


if __name__ == "__main__":
    main()
