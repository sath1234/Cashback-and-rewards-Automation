import pytest

from playwright.sync_api import (
    sync_playwright,
    TimeoutError
)

# ==================================================
# 🔹 CONFIG
# ==================================================

CDP_ENDPOINT = "http://127.0.0.1:9222"

REWARDS_URL = "https://rewards.santabrowser.com"

# ==================================================
# 🔹 XPATHS
# ==================================================

# 🔹 Quests Category
QUESTS_XPATH = (
    "//nav[@class='flex-1 pr-1']//span[text()='Quests']"
)

# 🔹 Filter Button
FILTER_XPATH = (
    "//button[text()='Filter']"
)

# 🔹 Social Filter
SOCIAL_XPATH = (
    "//button[text()='Social']"
)

# 🔹 Apply Button
APPLY_XPATH = (
    "//button[text()='Apply']"
)

# 🔹 Connect Discord Quest
CONNECT_DISCORD_XPATH = (
    "//h3[text()='Connect Discord']"
)

# 🔹 Verify Membership Button
VERIFY_MEMBERSHIP_XPATH = (
    "//button[text()='Verify Membership']"
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

        print("\n🏆 Opening Rewards Page...")

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

def click_element(page, xpath, element_name):

    print(f"\n🔹 Clicking {element_name}...")

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

# ==================================================
# 🔹 TEST CASE 1
# ==================================================

def test_open_quests_category(page):

    click_element(
        page,
        QUESTS_XPATH,
        "Quests Category"
    )

    page.screenshot(
        path="quests_category.png",
        full_page=True
    )

# ==================================================
# 🔹 TEST CASE 2
# ==================================================

def test_apply_social_filter(page):

    # 🔹 Click Filter
    click_element(
        page,
        FILTER_XPATH,
        "Filter Button"
    )

    # 🔹 Click Social
    click_element(
        page,
        SOCIAL_XPATH,
        "Social Filter"
    )

    # 🔹 Click Apply
    click_element(
        page,
        APPLY_XPATH,
        "Apply Button"
    )

    page.screenshot(
        path="social_filter_applied.png",
        full_page=True
    )

# ==================================================
# 🔹 TEST CASE 3
# ==================================================

def test_open_connect_discord_quest(page):

    click_element(
        page,
        CONNECT_DISCORD_XPATH,
        "Connect Discord Quest"
    )

    page.screenshot(
        path="connect_discord_quest.png",
        full_page=True
    )

# ==================================================
# 🔹 TEST CASE 4
# ==================================================

def test_click_verify_membership(page):

    try:

        click_element(
            page,
            VERIFY_MEMBERSHIP_XPATH,
            "Verify Membership Button"
        )

        print(
            "🎉 Verify Membership button clicked successfully"
        )

        page.screenshot(
            path="verify_membership_clicked.png",
            full_page=True
        )

    except TimeoutError:

        pytest.fail(
            "❌ Verify Membership button not found"
        )