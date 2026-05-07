from playwright.sync_api import sync_playwright, TimeoutError
import pytest


# ==================================================
# 🔹 CONFIG
# ==================================================

CDP_ENDPOINT = "http://127.0.0.1:9222"

REWARDS_URL = (
    "https://rewards.santabrowser.com/home?clid=8da91acc7b09930"
)

# 🔹 XPaths
SPACES_XPATH = "(//*[@class='truncate'])[2]"

TEXT_ITEM_XPATH = (
    "(//*[contains(@class,'tracking-tight') "
    "and contains(@class,'text-xs')])[1]"
)

SIDEBAR_ACTIVE_XPATH = (
    "(//*[contains(@class,'sidebar-active-glow')])[1]"
)


# ==================================================
# 🔹 SETUP
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

    print("Opening Rewards Home...")

    page.goto(REWARDS_URL, timeout=60000)

    page.wait_for_load_state("domcontentloaded")

    page.wait_for_timeout(5000)

    return page, browser, p


# ==================================================
# 🔹 COMMON CLICK FUNCTION
# ==================================================

def click_element(page, xpath, element_name):

    try:

        print(f"Clicking {element_name}...")

        page.wait_for_selector(xpath, timeout=15000)

        element = page.locator(xpath)

        element.scroll_into_view_if_needed()

        page.wait_for_timeout(1000)

        element.click(force=True)

        print(f"✅ Clicked {element_name}")

        page.wait_for_timeout(3000)

    except Exception as e:

        print(f"❌ Failed to click {element_name}: {e}")

        raise


# ==================================================
# 🔹 TEST CASE 1
# ==================================================

def test_click_spaces():

    page, browser, p = setup_page()

    click_element(page, SPACES_XPATH, "Spaces")

    page.screenshot(path="spaces.png", full_page=True)

    page.close()

    browser.close()

    p.stop()


# ==================================================
# 🔹 TEST CASE 2
# ==================================================

def test_click_text_item():

    page, browser, p = setup_page()

    click_element(page, SPACES_XPATH, "Spaces")

    click_element(page, TEXT_ITEM_XPATH, "Text Item")

    page.screenshot(path="text_item.png", full_page=True)

    page.close()

    browser.close()

    p.stop()


# ==================================================
# 🔹 TEST CASE 3
# ==================================================

def test_click_sidebar_active():

    page, browser, p = setup_page()

    click_element(page, SPACES_XPATH, "Spaces")

    click_element(page, TEXT_ITEM_XPATH, "Text Item")

    click_element(
        page,
        SIDEBAR_ACTIVE_XPATH,
        "Sidebar Active Item"
    )

    page.screenshot(
        path="sidebar_active.png",
        full_page=True
    )

    page.close()

    browser.close()

    p.stop()


# ==================================================
# 🔹 TEST CASE 4
# ==================================================

def test_complete_spaces_flow():

    page, browser, p = setup_page()

    click_element(page, SPACES_XPATH, "Spaces")

    click_element(page, TEXT_ITEM_XPATH, "Text Item")

    click_element(
        page,
        SIDEBAR_ACTIVE_XPATH,
        "Sidebar Active Item"
    )

    print("✅ Complete Spaces flow passed")

    page.screenshot(
        path="complete_flow.png",
        full_page=True
    )

    page.close()

    browser.close()

    p.stop()