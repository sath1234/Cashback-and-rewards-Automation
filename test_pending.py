from playwright.sync_api import sync_playwright, TimeoutError

CDP_ENDPOINT = "http://127.0.0.1:9222"

REWARDS_URL = "https://rewards.santabrowser.com"

# ==================================================
# 🔹 XPaths
# ==================================================

PENDING_BALANCE_XPATH = "//aside[@class='hidden lg:flex lg:flex-col lg:gap-4']//button[text()='Overview']"

HOME_XPATH = "//nav[@class='flex-1 pr-1']//span[text()='Home']"


# ==================================================
# 🔹 Common Function
# ==================================================

def click_pending_balance(page):

    try:

        # 🔹 Wait for Pending Balance element
        page.wait_for_selector(PENDING_BALANCE_XPATH, timeout=15000)

        # 🔹 Scroll into view
        pending_element = page.locator(PENDING_BALANCE_XPATH)

        pending_element.scroll_into_view_if_needed()

        page.wait_for_timeout(2000)

        # 🔹 Click Pending Balance
        pending_element.click(force=True)

        print("✅ Clicked Pending Balance")

        page.wait_for_timeout(5000)

        # 🔹 Wait for Home element
        page.wait_for_selector(HOME_XPATH, timeout=15000)

        # 🔹 Click Home
        home_element = page.locator(HOME_XPATH)

        home_element.scroll_into_view_if_needed()

        page.wait_for_timeout(2000)

        home_element.click(force=True)

        print("✅ Clicked Home")

        page.wait_for_timeout(5000)

    except Exception as e:

        print(f"❌ Failed in Pending Balance flow: {e}")

        raise


# ==================================================
# 🔹 Setup Browser
# ==================================================

def setup_page():

    p = sync_playwright().start()

    browser = p.chromium.connect_over_cdp(CDP_ENDPOINT)

    context = (
        browser.contexts[0]
        if browser.contexts
        else browser.new_context()
    )

    page = context.new_page()

    page.goto(REWARDS_URL, timeout=60000)

    page.wait_for_load_state("domcontentloaded")

    page.wait_for_timeout(5000)

    return page, browser, p


# ==================================================
# 🔹 Test Pending Balance Flow
# ==================================================

def test_pending_balance_flow():

    page, browser, p = setup_page()

    click_pending_balance(page)

    page.close()

    browser.close()

    p.stop()