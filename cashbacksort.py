import random
from playwright.sync_api import sync_playwright

# ---------- CONFIG ----------
CASHBACK_HOST = "shopping.santabrowser.com"

# ---------- HELPERS ----------
def find_cashback_tab(ctx):
    for pg in ctx.pages:
        if CASHBACK_HOST in (pg.url or ""):
            return pg
    return None

def select_random_category(tab):
    categories = tab.locator("h3, button.sc-SQOaL")
    count = categories.count()
    if count == 0:
        raise RuntimeError("❌ No categories found.")

    idx = random.randint(0, count - 1)
    random_category = categories.nth(idx)
    txt = "(no text)"
    try:
        txt = random_category.inner_text(timeout=2000).strip()
    except:
        pass
    print(f"📌 Clicking category [{idx}]: {txt}")

    try:
        random_category.scroll_into_view_if_needed()
        tab.wait_for_timeout(500)
        random_category.click(timeout=3000, force=True)
    except Exception:
        print("⚠️ Normal click failed, trying JS click...")
        handle = random_category.element_handle()
        if handle:
            tab.evaluate("(el) => el.click()", handle)

    tab.wait_for_timeout(2000)

def open_sort_dropdown(tab):
    btn = tab.locator("//div[@class='relative z-10 undefined']")
    btn.scroll_into_view_if_needed()
    tab.wait_for_timeout(300)
    try:
        btn.click(timeout=2000, force=True)
    except Exception:
        handle = btn.element_handle()
        if handle:
            tab.evaluate("(el) => el.click()", handle)
    tab.wait_for_timeout(500)

def select_sort_option(tab, label: str):
    open_sort_dropdown(tab)
    option = tab.locator(f"div.a_dropdown.a_item_dropdown:has-text('{label}')").first
    if option.count() == 0:
        raise RuntimeError(f"❌ Sort option '{label}' not found in dropdown.")

    option.scroll_into_view_if_needed()
    tab.wait_for_timeout(300)
    try:
        option.click(timeout=2000, force=True)
    except Exception:
        handle = option.element_handle()
        if handle:
            tab.evaluate("(el) => el.click()", handle)
    tab.wait_for_timeout(2000)  # wait for UI update

def go_back_to_home(tab):
    print("🏠 Going back to Cashback homepage...")
    back_btn = tab.locator("//div[@class='sc-bSlUec bbdPrM']")
    if back_btn.count() == 0:
        print("❌ Back to home button not found.")
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

def print_summary_box(summary):
    GREEN = "\033[92m"
    RED = "\033[91m"
    RESET = "\033[0m"

    lines = []
    for label, status in summary.items():
        if status == "Pass":
            lines.append(f"{label} : {GREEN}✔ Pass{RESET}")
        else:
            lines.append(f"{label} : {RED}✖ Fail{RESET}")

    width = max(len(line) for line in lines) + 4
    print("\n" + "╔" + "═" * (width - 2) + "╗")
    for line in lines:
        clean_line = ''.join(c for c in line if c not in "\033[92m\033[91m\033[0m")
        print("║ " + line + " " * (width - 4 - len(clean_line)) + " ║")
    print("╚" + "═" * (width - 2) + "╝\n")

# ---------- MAIN ----------
def main():
    with sync_playwright() as p:
        print("⏳ Connecting to browser...")
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        ctx = browser.contexts[0]

        cashback = find_cashback_tab(ctx)
        if not cashback:
            print("❗ Cashback tab not found. Please open the cashback page first.")
            return

        cashback.bring_to_front()
        cashback.wait_for_load_state("domcontentloaded", timeout=10000)

        summary = {
            "Sort Filter A-Z": "Fail",
            "Sort Filter Cashback %": "Fail"
        }

        print("🚀 Starting Cashback sort flow...")

        try:
            select_random_category(cashback)

            # A-Z Sort
            print("🔤 Sorting by A-Z...")
            try:
                select_sort_option(cashback, "A-Z")
                summary["Sort Filter A-Z"] = "Pass"
            except Exception as e:
                print(f"❌ A-Z sort failed: {e}")

            # Cashback % Sort
            print("💰 Sorting by Cashback %...")
            try:
                select_sort_option(cashback, "Cashback %")
                summary["Sort Filter Cashback %"] = "Pass"
            except Exception as e:
                print(f"❌ Cashback % sort failed: {e}")

            # ✅ Go back to Cashback homepage (new XPath)
            go_back_to_home(cashback)

        except Exception as e:
            print(f"❌ Automation failed: {e}")

        print_summary_box(summary)
        input("Press Enter to exit…")

if __name__ == "__main__":
    main()
