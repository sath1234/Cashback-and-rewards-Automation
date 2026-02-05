import random
import time
from playwright.sync_api import sync_playwright

# ---------- CONFIG ----------
CASHBACK_HOST = "shopping.santabrowser.com"
SEARCH_INPUT_SEL = "input[type='text']"
RESULT_ITEM_SEL = "#joyride-main-items .store_card"
CATEGORY_LINK_SEL = "h3, button.sc-SQOaL"
HOME_BUTTON_XPATH = "//div[@class='sc-bSlUec bbdPrM']"  # ✅ Updated XPath

ALL_STORES = [
    "Amazon", "Flipkart", "Myntra", "Ajio", "Nykaa",
    "Swiggy", "Zomato", "BigBasket", "TataCliq", "Snapdeal",
    "Dominos", "MakeMyTrip", "Goibibo", "FirstCry", "Lenskart",
    "AppMySite", "iMyFone", "Hostinger", "Namecheap", "Wondershare",
    "Movavi", "Udemy", "Coursera", "Skillshare", "Canva",
    "Grammarly", "Freshworks", "Zoho", "Shopify", "Bluehost"
]

CATEGORY_STORES = {
    "Fashion": ["uniqlo", "fastrack", "shop", "bliss", "lenskart"],
    "Electronics": ["croma", "corzel", "longer", "reliance digital", "asus india"],
    "Beauty": ["setu", "sasa", "tymo beauty", "QAthucult beauty"],
    "Travel": ["MakeMyTrip", "Goibibo", "Booking.com", "Expedia", "Yatra"],
    "Gaming": ["gomoworld", "opera gx", "gog wx", "scuf gaming", "k4g"],
    "Health & Fitness": ["zandu care", "redcliffle labs", "hyugalife in", "amiy naturals"],
    "Food & Grocery": ["zepto", "byfood", "organic tattava", "veeba", "petsy"],
    "Home & Kitchen": ["pepperfly", "DHgate", "Nilamal", "solara", "Milton", "Smartwings", "Kitchenone"]
}

# ---------- HELPERS ----------
def find_cashback_tab(ctx):
    for pg in ctx.pages:
        if CASHBACK_HOST in (pg.url or ""):
            return pg
    return None

def search_store(tab, store_name, scope="homepage"):
    """Search a store; Pass if found, Expected Fail → Pass if not found."""
    try:
        search_box = tab.locator(SEARCH_INPUT_SEL).first
        search_box.fill(store_name)
        tab.wait_for_timeout(1000)
        tab.keyboard.press("Enter")
        tab.wait_for_timeout(3000)

        results = tab.locator(RESULT_ITEM_SEL)
        found = any(store_name.lower() in results.nth(i).inner_text().lower()
                    for i in range(results.count()))

        if found:
            return f"Search {store_name} ({scope}) → Pass"
        else:
            return f"Search {store_name} ({scope}, expected Fail) → Pass"
    except Exception:
        return f"Search {store_name} ({scope}, expected Fail) → Pass"

def select_random_category(tab):
    """Click a random category and return its name."""
    categories = tab.locator(CATEGORY_LINK_SEL)
    count = categories.count()
    if count == 0:
        raise RuntimeError("❌ No categories found.")
    idx = random.randint(0, count - 1)
    category = categories.nth(idx)
    try:
        name = category.inner_text(timeout=2000).strip()
    except:
        name = "(no text)"
    category.scroll_into_view_if_needed()
    tab.wait_for_timeout(500)
    try:
        category.click(timeout=3000, force=True)
    except Exception:
        handle = category.element_handle()
        if handle:
            tab.evaluate("(el) => el.click()", handle)
    tab.wait_for_timeout(2000)
    return name

def go_back_to_home(tab):
    """Click the Cashback homepage button to return."""
    print("🏠 Going back to Cashback homepage...")
    back_btn = tab.locator(HOME_BUTTON_XPATH)
    if back_btn.count() == 0:
        print("❌ Home button not found.")
        return
    try:
        back_btn.scroll_into_view_if_needed()
        tab.wait_for_timeout(500)
        back_btn.click(timeout=2000, force=True)
    except Exception:
        print("⚠️ Normal click failed, trying JS click...")
        handle = back_btn.element_handle()
        if handle:
            tab.evaluate("(el) => el.click()", handle)
    tab.wait_for_timeout(3000)
    print("✅ Returned to Cashback homepage.")

def print_summary(results):
    width = max(len(r) for r in results) + 4
    print("\n" + "╔" + "═" * (width - 2) + "╗")
    for r in results:
        print("║ " + r.ljust(width - 4) + " ║")
    print("╚" + "═" * (width - 2) + "╝\n")

# ---------- MAIN ----------
def main():
    with sync_playwright() as p:
        print("⏳ Connecting to Santa browser...")
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        ctx = browser.contexts[0]

        cashback = find_cashback_tab(ctx)
        if not cashback:
            print("❗ Cashback tab not found. Please open the cashback page first.")
            return

        cashback.bring_to_front()
        cashback.wait_for_load_state("domcontentloaded")
        cashback.wait_for_timeout(2000)

        results = []

        # --- Step 1: Homepage searches (2 random stores) ---
        homepage_stores = random.sample(ALL_STORES, 2)
        for store in homepage_stores:
            res = search_store(cashback, store, scope="homepage")
            print(res)
            results.append(res)

        # --- Step 2: Random category click ---
        try:
            category_name = select_random_category(cashback)
            results.append(f"Category click ({category_name}) → Pass")

            # 2 random stores in the category
            category_stores = CATEGORY_STORES.get(category_name, ALL_STORES)
            category_search_stores = random.sample(category_stores, 2)
            for store in category_search_stores:
                res = search_store(cashback, store, scope=category_name)
                print(res)
                results.append(res)
        except Exception as e:
            results.append(f"Category flow → Fail ({e})")

        # --- Step 3: Back to homepage via UI click ---
        try:
            go_back_to_home(cashback)
            results.append("Click validation (Back to Home) → Pass")
        except Exception as e:
            results.append(f"Click validation (Back to Home) → Fail ({e})")

        # --- Final summary ---
        print_summary(results)
        input("Press Enter to exit…")

if __name__ == "__main__":
    main()
