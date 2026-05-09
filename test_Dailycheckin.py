import pytest
import requests

from datetime import datetime

from playwright.sync_api import (
    sync_playwright,
    TimeoutError
)

# ==================================================
# 🔹 CONFIG
# ==================================================

CDP_ENDPOINT = "http://127.0.0.1:9222"

REWARDS_URL = "https://rewards.santabrowser.com"

CLID = "8da91acc7b09930"

API_URL = (
    "https://api.santabrowser.com/quests/bff/v1/"
    f"quests/q.daily.checkin/checkin-status?clid={CLID}"
)

# ==================================================
# 🔹 XPATHS / SELECTORS
# ==================================================

QUEST_XPATH = "(//span[@class='truncate'])[1]"

FILTER_SELECTOR = (
    "[class='inline-flex items-center justify-center "
    "whitespace-nowrap text-sm font-medium "
    "transition-colors focus-visible:outline-none "
    "focus-visible:ring-2 focus-visible:ring-ring "
    "focus-visible:ring-offset-2 "
    "disabled:pointer-events-none "
    "disabled:opacity-50 ring-offset-background "
    "border px-3 h-9 rounded-full "
    "border-foreground/10 bg-foreground/5 "
    "text-foreground hover:bg-foreground/10 "
    "hover:text-foreground']"
)

USAGE_XPATH = (
    "//button[@class='whitespace-nowrap rounded-full "
    "border px-3 py-1.5 text-xs hover:bg-white/80 "
    "dark:hover:bg-white/15 border-sky-200 "
    "text-sky-700 bg-sky-50/70 "
    "dark:border-sky-400/40 "
    "dark:text-sky-200/80 dark:bg-sky-500/10']"
)

APPLY_SELECTOR = (
    "[class='inline-flex items-center justify-center "
    "whitespace-nowrap rounded-md text-sm "
    "font-medium transition-colors "
    "focus-visible:outline-none "
    "focus-visible:ring-2 focus-visible:ring-ring "
    "focus-visible:ring-offset-2 "
    "disabled:pointer-events-none "
    "disabled:opacity-50 ring-offset-background "
    "bg-primary text-primary-foreground "
    "hover:opacity-90 h-8 px-3']"
)

# 🔹 Updated Daily Check-in Card Index [4]
DAILY_CHECKIN_CARD = (
    "(//*[@class='tracking-tight font-display "
    "text-sm font-semibold mt-5 leading-snug "
    "text-slate-900 dark:text-white "
    "line-clamp-2'])[4]"
)

DAILY_CHECKIN_BUTTON = (
    "//button[@class='inline-flex items-center "
    "justify-center whitespace-nowrap text-sm "
    "font-medium transition-colors "
    "focus-visible:outline-none "
    "focus-visible:ring-2 focus-visible:ring-ring "
    "focus-visible:ring-offset-2 "
    "disabled:pointer-events-none "
    "disabled:opacity-50 ring-offset-background "
    "bg-primary text-primary-foreground "
    "hover:opacity-90 h-10 px-4 py-2 "
    "flex-1 rounded-full']"
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

        print("\n🏆 Opening Rewards page...")

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
# 🔹 API FUNCTION
# ==================================================

def get_checkin_status():

    try:

        response = requests.get(
            API_URL,
            timeout=10
        )

        data = response.json()

        print("\n📡 API RESPONSE:", data)

        if "data" in data:

            data = data["data"]

        last_checkin_ymd = data.get(
            "last_checkin_ymd"
        )

        today_date = datetime.now().strftime(
            "%Y-%m-%d"
        )

        if last_checkin_ymd == today_date:

            return "COMPLETED"

        return "NOT_COMPLETED"

    except Exception as e:

        print("❌ API Error:", e)

        return None


# ==================================================
# 🔹 TEST CASE 1
# ==================================================

def test_open_quest_category(page):

    click_element(
        page,
        QUEST_XPATH,
        "Quest Category"
    )

    page.screenshot(
        path="quest_category.png",
        full_page=True
    )


# ==================================================
# 🔹 TEST CASE 2
# ==================================================

def test_apply_usage_filter(page):

    click_element(
        page,
        FILTER_SELECTOR,
        "Filter"
    )

    click_element(
        page,
        USAGE_XPATH,
        "Usage"
    )

    click_element(
        page,
        APPLY_SELECTOR,
        "Apply"
    )

    page.screenshot(
        path="usage_filter.png",
        full_page=True
    )


# ==================================================
# 🔹 TEST CASE 3
# ==================================================

def test_verify_daily_checkin_status():

    status = get_checkin_status()

    print(
        f"\n✅ Current Daily Check-in Status : {status}"
    )

    assert status in [
        "COMPLETED",
        "NOT_COMPLETED"
    ]


# ==================================================
# 🔹 TEST CASE 4
# ==================================================

def test_complete_daily_checkin(page):

    status = get_checkin_status()

    print(f"\n📌 Current Status : {status}")

    # 🔹 Already Completed
    if status == "COMPLETED":

        print(
            "✅ Daily Check-in already completed"
        )

        assert True

    # 🔹 Not Completed → Complete it
    elif status == "NOT_COMPLETED":

        print(
            "⏳ Daily Check-in not completed"
        )

        try:

            # 🔹 Click Daily Check-in Card
            click_element(
                page,
                DAILY_CHECKIN_CARD,
                "Daily Check-in Card"
            )

            # 🔹 Click Daily Check-in Button
            click_element(
                page,
                DAILY_CHECKIN_BUTTON,
                "Daily Check-in Button"
            )

            print(
                "\n⏳ Waiting for status update..."
            )

            page.wait_for_timeout(10000)

            # 🔹 Verify Updated Status
            updated_status = get_checkin_status()

            print(
                f"\n✅ Updated Status : "
                f"{updated_status}"
            )

            # 🔥 PASS TEST CASE
            assert (
                updated_status == "COMPLETED"
            )

            print(
                "🎉 Daily Check-in completed "
                "successfully"
            )

            # 📸 Screenshot
            page.screenshot(
                path="daily_checkin_completed.png",
                full_page=True
            )

        except TimeoutError:

            pytest.fail(
                "❌ Daily Check-in elements not found"
            )

    else:

        pytest.fail(
            "❌ Unable to fetch Daily Check-in status"
        )