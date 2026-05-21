from playwright.sync_api import (
    sync_playwright,
    TimeoutError
)

import pytest

# ==================================================
# 🔹 CONFIG
# ==================================================

CDP_ENDPOINT = "http://127.0.0.1:9222"

REWARDS_URL = (
    "https://rewards.santabrowser.com/home?clid=8da91acc7b09930"
)

# ==================================================
# 🔹 XPATHS
# ==================================================

# 🔹 Spaces Category
SPACES_XPATH = (
    "//nav[@class='flex-1 pr-1']//span[text()='Spaces']"
)

# 🔹 Santa Quest
SANTA_QUEST_XPATH = (
    "//h3[text()='Santa']"
)

# 🔹 Home Category
HOME_XPATH = (
    "//nav[@class='flex-1 pr-1']//span[text()='Home']"
)

# ==================================================
# 🔹 SETUP
# ==================================================

def setup_page():

    p = sync_playwright().start()

    browser = p.chromium.connect_over_cdp(
        CDP_ENDPOINT
    )

    context = (
        browser.contexts[0]
        if browser.contexts
        else browser.new_context()
    )

    page = context.new_page()

    print("🏆 Opening Rewards Home...")

    page.goto(
        REWARDS_URL,
        timeout=60000
    )

    page.wait_for_load_state(
        "domcontentloaded"
    )

    page.wait_for_timeout(5000)

    return page, browser, p

# ==================================================
# 🔹 COMMON CLICK FUNCTION
# ==================================================

def click_element(page, xpath, element_name):

    try:

        print(f"🔹 Clicking {element_name}...")

        locator = page.locator(xpath).first

        locator.wait_for(
            state="visible",
            timeout=15000
        )

        locator.scroll_into_view_if_needed()

        page.wait_for_timeout(1000)

        locator.click(force=True)

        print(f"✅ Clicked {element_name}")

        page.wait_for_timeout(3000)

    except TimeoutError:

        print(f"❌ {element_name} not found")

        raise

# ==================================================
# 🔹 TEST CASE 1
# ==================================================

def test_click_spaces():

    page, browser, p = setup_page()

    click_element(
        page,
        SPACES_XPATH,
        "Spaces Category"
    )

    page.screenshot(
        path="spaces_click.png",
        full_page=True
    )

    page.close()

    browser.close()

    p.stop()

# ==================================================
# 🔹 TEST CASE 2
# ==================================================

def test_click_santa_quest():

    page, browser, p = setup_page()

    # 🔹 Click Spaces
    click_element(
        page,
        SPACES_XPATH,
        "Spaces Category"
    )

    # 🔹 Click Santa Quest
    click_element(
        page,
        SANTA_QUEST_XPATH,
        "Santa Quest"
    )

    page.screenshot(
        path="santa_quest_click.png",
        full_page=True
    )

    page.close()

    browser.close()

    p.stop()

# ==================================================
# 🔹 TEST CASE 3
# ==================================================

def test_click_home_category():

    page, browser, p = setup_page()

    # 🔹 Click Spaces
    click_element(
        page,
        SPACES_XPATH,
        "Spaces Category"
    )

    # 🔹 Click Santa Quest
    click_element(
        page,
        SANTA_QUEST_XPATH,
        "Santa Quest"
    )

    # 🔹 Click Home
    click_element(
        page,
        HOME_XPATH,
        "Home Category"
    )

    page.screenshot(
        path="home_category_click.png",
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

    # 🔹 Click Spaces
    click_element(
        page,
        SPACES_XPATH,
        "Spaces Category"
    )

    # 🔹 Click Santa Quest
    click_element(
        page,
        SANTA_QUEST_XPATH,
        "Santa Quest"
    )

    # 🔹 Click Home
    click_element(
        page,
        HOME_XPATH,
        "Home Category"
    )

    print("✅ Complete Spaces Flow Passed")

    page.screenshot(
        path="complete_spaces_flow.png",
        full_page=True
    )

    page.close()

    browser.close()

    p.stop()