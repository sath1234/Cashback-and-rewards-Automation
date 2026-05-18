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

MY_REWARDS_CATEGORY = (
    "(//*[@class='group relative flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm transition-all duration-200 text-foreground/80 hover:bg-accent/50 hover:text-foreground'])[3]"
)

TRANSACTION_HISTORY = (
    "(//*[@class='inline-flex items-center justify-center font-medium transition-colors disabled:pointer-events-none disabled:opacity-50 ring-offset-background hover:bg-accent hover:text-accent-foreground px-3 h-7 rounded-full text-xs whitespace-nowrap shrink-0 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-primary focus-visible:ring-offset-background opacity-80'])[1]"
)

QUEST_CATEGORY = (
    "(//*[@class='inline-flex items-center justify-center font-medium transition-colors disabled:pointer-events-none disabled:opacity-50 ring-offset-background hover:bg-accent hover:text-accent-foreground px-3 h-7 rounded-full text-xs whitespace-nowrap shrink-0 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-primary focus-visible:ring-offset-background opacity-80'])[2]"
)

EVENT_AWARDS = (
    "//div[@class='inline-flex w-max gap-2 whitespace-nowrap md:gap-0 md:rounded-full md:border md:p-1 md:bg-white/70 md:dark:bg-white/10']/button[text()='Event Awards']"
)

CLICKS = (
    "//div[@class='flex items-center gap-2 overflow-x-auto pb-1 flex-nowrap [-ms-overflow-style:none] [scrollbar-width:none] [&::-webkit-scrollbar]:hidden md:flex-wrap md:overflow-visible min-w-0 flex-1']/button[text()='Clicks']"
)

IMPRESSIONS = (
    "//div[@class='flex items-center gap-2 overflow-x-auto pb-1 flex-nowrap [-ms-overflow-style:none] [scrollbar-width:none] [&::-webkit-scrollbar]:hidden md:flex-wrap md:overflow-visible min-w-0 flex-1']/button[text()='Impressions']"
)

MISC = (
    "//div[@class='flex items-center gap-2 overflow-x-auto pb-1 flex-nowrap [-ms-overflow-style:none] [scrollbar-width:none] [&::-webkit-scrollbar]:hidden md:flex-wrap md:overflow-visible min-w-0 flex-1']/button[text()='Misc']"
)

QUEST_COMPLETIONS = (
    "//div[@class='inline-flex w-max gap-2 whitespace-nowrap md:gap-0 md:rounded-full md:border md:p-1 md:bg-white/70 md:dark:bg-white/10']/button[text()='Quest Completions']"
)

REFERRAL_REWARDS = (
    "//div[@class='inline-flex w-max gap-2 whitespace-nowrap md:gap-0 md:rounded-full md:border md:p-1 md:bg-white/70 md:dark:bg-white/10']/button[text()='Referral Rewards']"
)

PLAYWALL_HISTORY = (
    "//div[@class='inline-flex w-max gap-2 whitespace-nowrap md:gap-0 md:rounded-full md:border']/button[text()='Playwall history']"
)

CASHBACK_HISTORY = (
    "//div[@class='inline-flex w-max gap-2 whitespace-nowrap md:gap-0 md:rounded-full md:border']/button[text()='Cashback history']"
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
# 🔹 TEST CASE
# ==================================================

def test_rewards_categories(page):

    try:

        # 🔹 My Rewards Category
        click_element(
            page,
            MY_REWARDS_CATEGORY,
            "My Rewards Category"
        )

        # 🔹 Transaction History
        click_element(
            page,
            TRANSACTION_HISTORY,
            "Transaction History"
        )

        # 🔹 Quest Category
        click_element(
            page,
            QUEST_CATEGORY,
            "Quest Category"
        )

        # 🔹 Event Awards
        click_element(
            page,
            EVENT_AWARDS,
            "Event Awards"
        )

        # 🔹 Clicks
        click_element(
            page,
            CLICKS,
            "Clicks"
        )

        # 🔹 Impressions
        click_element(
            page,
            IMPRESSIONS,
            "Impressions"
        )

        # 🔹 Misc
        click_element(
            page,
            MISC,
            "Misc"
        )

        # 🔹 Quest Completions
        click_element(
            page,
            QUEST_COMPLETIONS,
            "Quest Completions"
        )

        # 🔹 Referral Rewards
        click_element(
            page,
            REFERRAL_REWARDS,
            "Referral Rewards"
        )

        # 🔹 Playwall History
        click_element(
            page,
            PLAYWALL_HISTORY,
            "Playwall History"
        )

        # 🔹 Cashback History
        click_element(
            page,
            CASHBACK_HISTORY,
            "Cashback History"
        )

        print("\n🎉 All Rewards Categories Clicked Successfully")

        # 📸 Screenshot
        page.screenshot(
            path="rewards_categories.png",
            full_page=True
        )

    except TimeoutError:

        pytest.fail(
            "❌ One or more elements not found"
        )