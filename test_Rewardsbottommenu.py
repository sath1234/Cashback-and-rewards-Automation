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

QUESTS_XPATH = (
    "//nav[@class='flex-1 pr-1']//span[text()='Quests']"
)

SPACES_XPATH = (
    "//nav[@class='flex-1 pr-1']//span[text()='Spaces']"
)

REWARDS_XPATH = (
    "//nav[@class='flex-1 pr-1']//span[text()='My Rewards']"
)

RANK_XPATH = (
    "//nav[@class='flex-1 pr-1']//span[text()='Rank']"
)

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

        print("🏆 Opening Rewards Page...")

        page.goto(
            REWARDS_URL,
            timeout=60000
        )

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

        print(f"\n🔹 Clicking {category_name}...")

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

def test_click_all_categories(page):

    # 🔹 Quests
    click_category(
        page,
        QUESTS_XPATH,
        "Quests"
    )

    # 🔹 Spaces
    click_category(
        page,
        SPACES_XPATH,
        "Spaces"
    )

    # 🔹 My Rewards
    click_category(
        page,
        REWARDS_XPATH,
        "My Rewards"
    )

    # 🔹 Rank
    click_category(
        page,
        RANK_XPATH,
        "Rank"
    )

    print(
        "\n🎉 Successfully clicked all categories"
    )

    # 📸 Screenshot
    page.screenshot(
        path="all_categories.png",
        full_page=True
    )