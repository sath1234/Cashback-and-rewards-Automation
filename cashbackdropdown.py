import re
import time
import requests
from playwright.sync_api import sync_playwright

# ----- CONFIG -----
CDP_ENDPOINT = "http://127.0.0.1:9222"
CASHBACK_HOST = "shopping.santabrowser.com"
COUNTRY = "Afghanistan"
SCROLL_DELAY = 3.0
CLICK_DELAY = 2.0
API_URL = "https://cbapi.santabrowser.com/data/stores?page=all&Country-Code=AF"

# ----- HELPERS -----
def normalize(s: str) -> str:
    if not s:
        return ""
    s = re.sub(r"[^\w\s]", "", s)
    s = re.sub(r"\s+", " ", s).strip().lower()
    return s

def find_cashback_tab(ctx):
    for pg in ctx.pages:
        if CASHBACK_HOST in (pg.url or ""):
            return pg
    return None

def safe_click(tab, selectors, label):
    for sel in selectors:
        try:
            loc = tab.locator(sel)
            if loc.count() > 0:
                loc.first.scroll_into_view_if_needed()
                loc.first.click(timeout=5000, force=True)
                tab.wait_for_timeout(int(CLICK_DELAY * 1000))
                print(f"✅ {label} clicked")  # Show category/country selection in output
                return True
        except Exception:
            pass
    return False

def open_categories(tab):
    return safe_click(tab, ["text=All Categories", "text=Categories", "text=Brands"], "Categories")

def open_country_dropdown(tab):
    return safe_click(tab, ["button.c_dropdown.minwidthdropdown", "text=Select Country"], "Country dropdown")

def select_country(tab, country):
    opts = tab.locator("a.c_dropdown.a_item_dropdown")
    for i in range(opts.count()):
        txt = opts.nth(i).inner_text().strip()
        if normalize(country) == normalize(txt):
            opts.nth(i).scroll_into_view_if_needed()
            opts.nth(i).click(timeout=5000, force=True)
            tab.wait_for_timeout(int(CLICK_DELAY * 1000))
            print(f"✅ Country selected: {txt}")
            return True
    print(f"❌ Country {country} not found")
    return False

def fetch_api_stores():
    resp = requests.get(API_URL, timeout=20)
    resp.raise_for_status()
    data = resp.json()
    stores = set()
    all_stores = data.get("data", {}).get("data", [])
    for store in all_stores:
        if isinstance(store, dict):
            name = store.get("name")
            if name:
                stores.add(normalize(name))
    print(f"🌐 API returned {len(stores)} stores")
    return stores

def collect_ui_stores(tab):
    all_p = tab.locator("p").all_inner_texts()
    batch = []
    for txt in all_p:
        if "cashback" in txt.lower() or "$" in txt:
            continue
        n = normalize(txt)
        if n:
            batch.append(n)
    return batch

# ----- MAIN -----
def run():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP_ENDPOINT)
        ctx = browser.contexts[0]
        tab = find_cashback_tab(ctx)
        if not tab:
            raise SystemExit("❌ Cashback tab not found. Open shopping.santabrowser.com first.")

        tab.bring_to_front()
        tab.wait_for_load_state("domcontentloaded")
        time.sleep(3)

        # ------------------------------
        # Category and country selection
        # ------------------------------
        open_categories(tab)
        if open_country_dropdown(tab):
            select_country(tab, COUNTRY)

        # ------------------------------
        # Fetch API stores
        # ------------------------------
        api_stores = fetch_api_stores()
        seen = set()

        # ------------------------------
        # Scroll to collect UI stores
        # ------------------------------
        while True:
            tab.evaluate("window.scrollBy(0, document.body.scrollHeight)")
            time.sleep(SCROLL_DELAY)

            all_stores = collect_ui_stores(tab)
            new_stores = [s for s in all_stores if s not in seen]

            if not new_stores:
                # print("✅ No new stores found, stopping.")  # Commented out
                break

            seen.update(new_stores)

        # ------------------------------
        # Compare UI stores with API stores
        # ------------------------------
        mismatches = set()
        for s in api_stores:
            if s not in seen:
                mismatches.add(s)

        # ------------------------------
        # Final summary (box)
        # ------------------------------
        print("\n" + "=" * 40)
        print("              FINAL SUMMARY              ")
        print("=" * 40)
        print(f"📦 Total UI stores collected   : {len(seen)}")
        print(f"🌐 Total API stores collected  : {len(api_stores)}")
        print(f"❌ Total mismatched stores     : {len(mismatches)}")
        print("=" * 40 + "\n")

        browser.close()

if __name__ == "__main__":
    run()
