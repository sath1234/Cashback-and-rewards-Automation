import pytest

from playwright.sync_api import (
    sync_playwright
)

# ==================================================
# 🔹 CONFIG
# ==================================================

CDP_ENDPOINT = "http://127.0.0.1:9222"

REWARDS_URL = "https://rewards.santabrowser.com"

# ==================================================
# 🔹 XPATHS
# ==================================================

# 🔹 Referral Search Input
REFERRAL_INPUT_XPATH = (
    "//div[@class='rounded-2xl border border-border bg-card/90 p-3']//input[@class='h-9 w-full rounded-md border border-input bg-background px-3 py-1 text-sm outline-none focus-visible:ring-2 focus-visible:ring-indigo-500/30 focus-visible:border-indigo-500 dark:focus-visible:ring-indigo-300/20 dark:focus-visible:border-indigo-300']"
)

# 🔹 Apply Button
APPLY_BUTTON_XPATH = (
    "//div[@class='rounded-2xl border border-border bg-card/90 p-3']//button[text()='Apply']"
)

# 🔹 Names List
SEARCH_NAMES = [
    "Balaji",
    "Sathya",
    "Esther Shajitha",
    "Mahesh",
    "Dhanesh"
]


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

    page.wait_for_timeout(2000)


# ==================================================
# 🔹 TEST CASE
# ==================================================

def test_search_multiple_referral_names(page):

    for name in SEARCH_NAMES:

        print(f"\n🔍 Searching Name: {name}")

        # 🔹 Click Search Box
        click_element(
            page,
            REFERRAL_INPUT_XPATH,
            "Referral Search Input"
        )

        # 🔹 Clear Existing Text
        page.fill(
            REFERRAL_INPUT_XPATH,
            ""
        )

        page.wait_for_timeout(1000)

        # 🔹 Enter New Name
        page.fill(
            REFERRAL_INPUT_XPATH,
            name
        )

        print(f"✅ Typed Name: {name}")

        page.wait_for_timeout(2000)

        # 🔹 Click Apply
        click_element(
            page,
            APPLY_BUTTON_XPATH,
            "Apply Button"
        )

        print(
            f"✅ Search completed for: {name}"
        )

        page.wait_for_timeout(3000)

    # 📸 Screenshot
    page.screenshot(
        path="multiple_referral_search.png",
        full_page=True
    )