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

# 🔹 Rank Category
RANK_XPATH = "//a[normalize-space()='Rank']"

# 🔹 Rank Filters
RANK_WEEKLY_XPATH = (
    "//button[@type='button' and normalize-space()='weekly']"
)

RANK_MONTHLY_XPATH = (
    "//button[@type='button' and normalize-space()='monthly']"
)

RANK_YEARLY_XPATH = (
    "//button[@type='button' and normalize-space()='yearly']"
)

# 🔹 Crew Category
CREW_XPATH = (
    "(//*[@class='px-3 py-1.5 text-xs font-medium "
    "rounded-full transition-colors "
    "text-muted-foreground hover:text-foreground'])[1]"
)

# 🔹 Crew Filters
CREW_WEEKLY_XPATH = (
    "(//*[@class='px-3 py-1.5 text-xs font-medium "
    "rounded-full transition-colors capitalize "
    "text-muted-foreground hover:text-foreground'])[1]"
)

CREW_MONTHLY_XPATH = (
    "(//*[@class='px-3 py-1.5 text-xs font-medium "
    "rounded-full transition-colors capitalize "
    "text-muted-foreground hover:text-foreground'])[2]"
)

CREW_YEARLY_XPATH = (
    "(//*[@class='px-3 py-1.5 text-xs font-medium "
    "rounded-full transition-colors capitalize "
    "text-muted-foreground hover:text-foreground'])[3]"
)


# ==================================================
# 🔹 PYTEST FIXTURE
# ==================================================

@pytest.fixture(scope="module")

def frame():

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

        rewards_frame = None

        for frm in page.frames:

            try:

                if frm.locator("//nav").count() > 0:

                    rewards_frame = frm

                    print(
                        "✅ Rewards iframe detected"
                    )

                    break

            except Exception:

                continue

        if not rewards_frame:

            raise Exception(
                "❌ Rewards iframe not found"
            )

        yield rewards_frame

        browser.close()


# ==================================================
# 🔹 COMMON CLICK FUNCTION
# ==================================================

def click_element(frame, xpath, element_name):

    print(f"🔹 Clicking {element_name}...")

    locator = frame.locator(xpath).first

    locator.wait_for(
        state="visible",
        timeout=15000
    )

    locator.scroll_into_view_if_needed()

    frame.page.wait_for_timeout(1000)

    locator.click(force=True)

    print(f"✅ Clicked {element_name}")

    frame.page.wait_for_timeout(3000)


# ==================================================
# 🔹 TEST CASE 1
# ==================================================

def test_click_rank(frame):

    click_element(
        frame,
        RANK_XPATH,
        "Rank"
    )

    frame.page.screenshot(
        path="rank.png",
        full_page=True
    )


# ==================================================
# 🔹 TEST CASE 2
# ==================================================

def test_click_rank_weekly(frame):

    click_element(
        frame,
        RANK_XPATH,
        "Rank"
    )

    click_element(
        frame,
        RANK_WEEKLY_XPATH,
        "Rank Weekly"
    )

    frame.page.screenshot(
        path="rank_weekly.png",
        full_page=True
    )


# ==================================================
# 🔹 TEST CASE 3
# ==================================================

def test_click_rank_monthly(frame):

    click_element(
        frame,
        RANK_XPATH,
        "Rank"
    )

    click_element(
        frame,
        RANK_MONTHLY_XPATH,
        "Rank Monthly"
    )

    frame.page.screenshot(
        path="rank_monthly.png",
        full_page=True
    )


# ==================================================
# 🔹 TEST CASE 4
# ==================================================

def test_click_rank_yearly(frame):

    click_element(
        frame,
        RANK_XPATH,
        "Rank"
    )

    click_element(
        frame,
        RANK_YEARLY_XPATH,
        "Rank Yearly"
    )

    frame.page.screenshot(
        path="rank_yearly.png",
        full_page=True
    )


# ==================================================
# 🔹 TEST CASE 5
# ==================================================

def test_click_crew(frame):

    click_element(
        frame,
        RANK_XPATH,
        "Rank"
    )

    click_element(
        frame,
        CREW_XPATH,
        "Crew Category"
    )

    frame.page.screenshot(
        path="crew.png",
        full_page=True
    )


# ==================================================
# 🔹 TEST CASE 6
# ==================================================

def test_click_crew_weekly(frame):

    click_element(
        frame,
        RANK_XPATH,
        "Rank"
    )

    click_element(
        frame,
        CREW_XPATH,
        "Crew Category"
    )

    click_element(
        frame,
        CREW_WEEKLY_XPATH,
        "Crew Weekly"
    )

    frame.page.screenshot(
        path="crew_weekly.png",
        full_page=True
    )


# ==================================================
# 🔹 TEST CASE 7
# ==================================================

def test_click_crew_monthly(frame):

    click_element(
        frame,
        RANK_XPATH,
        "Rank"
    )

    click_element(
        frame,
        CREW_XPATH,
        "Crew Category"
    )

    click_element(
        frame,
        CREW_MONTHLY_XPATH,
        "Crew Monthly"
    )

    frame.page.screenshot(
        path="crew_monthly.png",
        full_page=True
    )


# ==================================================
# 🔹 TEST CASE 8
# ==================================================

def test_click_crew_yearly(frame):

    click_element(
        frame,
        RANK_XPATH,
        "Rank"
    )

    click_element(
        frame,
        CREW_XPATH,
        "Crew Category"
    )

    click_element(
        frame,
        CREW_YEARLY_XPATH,
        "Crew Yearly"
    )

    frame.page.screenshot(
        path="crew_yearly.png",
        full_page=True
    )