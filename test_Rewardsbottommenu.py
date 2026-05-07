import pytest

from playwright.sync_api import (
    sync_playwright,
    TimeoutError
)

CDP_ENDPOINT = "http://127.0.0.1:9222"

REWARDS_URL = "https://rewards.santabrowser.com"


# ==================================================
# 🔹 CATEGORY XPATHS
# ==================================================

REWARDS_XPATH = "(//*[@class='truncate'])[1]"

QUESTS_XPATH = "(//*[@class='truncate'])[2]"

SPACES_XPATH = "(//*[@class='truncate'])[3]"

RANK_XPATH = "(//*[@class='truncate'])[4]"


# ==================================================
# 🔹 PYTEST FIXTURE
# ==================================================

@pytest.fixture(scope="module")

def page():

    with sync_playwright() as p:

        browser = p.chromium.connect_over_cdp(
            CDP_ENDPOINT
        )

        context = (
            browser.contexts[0]
            if browser.contexts
            else browser.new_context()
        )

        page = context.new_page()

        print("🏆 Opening Rewards page...")

        page.goto(REWARDS_URL, timeout=60000)

        page.wait_for_load_state(
            "domcontentloaded"
        )

        page.wait_for_timeout(5000)

        yield page

        browser.close()


# ==================================================
# 🔹 COMMON CLICK FUNCTION
# ==================================================

def click_category(page, xpath, category_name):

    try:

        locator = page.locator(xpath).first

        locator.wait_for(
            state="visible",
            timeout=15000
        )

        locator.scroll_into_view_if_needed()

        page.wait_for_timeout(1000)

        locator.click(force=True)

        print(f"✅ Clicked {category_name}")

        page.wait_for_timeout(3000)

    except Exception as e:

        print(f"❌ Failed to click {category_name}: {e}")

        raise


# ==================================================
# 🔹 TEST CASE 1
# ==================================================

def test_click_rewards_category(page):

    click_category(
        page,
        REWARDS_XPATH,
        "Rewards"
    )

    page.screenshot(
        path="rewards_category.png",
        full_page=True
    )


# ==================================================
# 🔹 TEST CASE 2
# ==================================================

def test_click_quests_category(page):

    click_category(
        page,
        QUESTS_XPATH,
        "Quests"
    )

    page.screenshot(
        path="quests_category.png",
        full_page=True
    )


# ==================================================
# 🔹 TEST CASE 3
# ==================================================

def test_click_spaces_category(page):

    click_category(
        page,
        SPACES_XPATH,
        "Spaces"
    )

    page.screenshot(
        path="spaces_category.png",
        full_page=True
    )


# ==================================================
# 🔹 TEST CASE 4
# ==================================================

def test_click_rank_category(page):

    click_category(
        page,
        RANK_XPATH,
        "Rank"
    )

    page.screenshot(
        path="rank_category.png",
        full_page=True
    )