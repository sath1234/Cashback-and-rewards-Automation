from playwright.sync_api import (
    sync_playwright,
    TimeoutError
)

CDP_ENDPOINT = "http://127.0.0.1:9222"

REWARDS_URL = "https://rewards.santabrowser.com"

# ==================================================
# 🔹 XPATHS
# ==================================================

# 🔹 Quests Category
QUESTS_XPATH = (
    "//div[@class='mb-5']//span[text()='Quests']"
)

# 🔹 Filter Button
FILTER_XPATH = (
    "//button[text()='Filter']"
)

# 🔹 Social Filter
SOCIAL_XPATH = (
    "//button[text()='Social']"
)

# 🔹 Not Started Filter
NOT_STARTED_XPATH = (
    "//button[text()='Not started']"
)

# 🔹 Completed Filter
COMPLETED_XPATH = (
    "//button[text()='Completed']"
)

# 🔹 Apply Button
APPLY_XPATH = (
    "//button[text()='Apply']"
)

# ==================================================
# 🔹 COMMON CLICK FUNCTION
# ==================================================

def click_element(page, xpath, element_name):

    try:

        print(f"\n🔹 Clicking {element_name}...")

        page.wait_for_selector(
            xpath,
            timeout=15000
        )

        element = page.locator(xpath).first

        element.scroll_into_view_if_needed()

        page.wait_for_timeout(2000)

        element.click(force=True)

        print(f"✅ Clicked {element_name}")

        page.wait_for_timeout(4000)

    except Exception as e:

        print(f"❌ Failed to click {element_name}: {e}")

        raise

# ==================================================
# 🔹 SETUP BROWSER
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

    print("\n🏆 Opening Rewards Page...")

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
# 🔹 TEST SOCIAL FILTER FLOW
# ==================================================

def test_social_filter_flow():

    page, browser, p = setup_page()

    try:

        # 🔹 Click Quests Category
        click_element(
            page,
            QUESTS_XPATH,
            "Quests Category"
        )

        # ==================================================
        # 🔹 SOCIAL + NOT STARTED FILTER
        # ==================================================

        click_element(
            page,
            FILTER_XPATH,
            "Filter Button"
        )

        click_element(
            page,
            SOCIAL_XPATH,
            "Social Filter"
        )

        click_element(
            page,
            NOT_STARTED_XPATH,
            "Not Started Filter"
        )

        click_element(
            page,
            APPLY_XPATH,
            "Apply Button"
        )

        # ==================================================
        # 🔹 SOCIAL + COMPLETED FILTER
        # ==================================================

        click_element(
            page,
            FILTER_XPATH,
            "Filter Button"
        )

        click_element(
            page,
            SOCIAL_XPATH,
            "Social Filter"
        )

        click_element(
            page,
            COMPLETED_XPATH,
            "Completed Filter"
        )

        click_element(
            page,
            APPLY_XPATH,
            "Apply Button"
        )

        # 🔹 Screenshot
        page.screenshot(
            path="social_filter_flow.png",
            full_page=True
        )

        print(
            "\n🎉 Social filter flow completed successfully"
        )

    except TimeoutError:

        print(
            "❌ Element not found during social filter flow"
        )

        raise

    finally:

        page.close()

        browser.close()

        p.stop()