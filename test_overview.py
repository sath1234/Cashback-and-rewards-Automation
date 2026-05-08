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

OVERVIEW_XPATH = (
    "(//button[@class='inline-flex items-center "
    "justify-center whitespace-nowrap text-sm "
    "focus-visible:outline-none focus-visible:ring-2 "
    "focus-visible:ring-ring focus-visible:ring-offset-2 "
    "disabled:pointer-events-none disabled:opacity-50 "
    "ring-offset-background border h-9 rounded-full "
    "px-4 font-semibold border-border bg-transparent "
    "hover:bg-primary/10 hover:border-primary "
    "hover:text-primary transition-colors'])[2]"
)

REFERRAL_XPATH = (
    "(//button[@class='h-8 px-3 text-xs rounded-full "
    "transition-colors whitespace-nowrap shrink-0 "
    "hover:bg-muted'])[3]"
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

        page.wait_for_timeout(4000)

    except Exception as e:

        print(
            f"❌ Failed to click "
            f"{element_name}: {e}"
        )

        raise


# ==================================================
# 🔹 TEST CASE 1
# ==================================================

def test_click_overview(page):

    click_element(
        page,
        OVERVIEW_XPATH,
        "Overview"
    )

    page.screenshot(
        path="overview.png",
        full_page=True
    )


# ==================================================
# 🔹 TEST CASE 2
# ==================================================

def test_click_referral(page):

    click_element(
        page,
        OVERVIEW_XPATH,
        "Overview"
    )

    click_element(
        page,
        REFERRAL_XPATH,
        "Referral"
    )

    page.screenshot(
        path="referral.png",
        full_page=True
    )


# ==================================================
# 🔹 TEST CASE 3
# ==================================================

def test_complete_overview_referral_flow(page):

    click_element(
        page,
        OVERVIEW_XPATH,
        "Overview"
    )

    click_element(
        page,
        REFERRAL_XPATH,
        "Referral"
    )

    print(
        "✅ Overview → Referral flow passed"
    )

    page.screenshot(
        path="overview_referral_flow.png",
        full_page=True
    )