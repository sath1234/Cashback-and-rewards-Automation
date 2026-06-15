from playwright.sync_api import (
    sync_playwright,
    TimeoutError
)

CDP_ENDPOINT = "http://127.0.0.1:9222"

REWARDS_URL = "https://rewards.santabrowser.com"

SEARCH_XPATH = "//input[@aria-label='Search']"

MONTHLY_USAGE_XPATH = "//mark[text()='Monthly Usage']"

CLOSE_XPATH = "//span[text()='Close']"

HOME_XPATH = (
    "//ul[@class='mt-2 space-y-1.5 px-1']//span[text()='Home']"
)


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


with sync_playwright() as p:

    try:

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

        # Search Monthly Usage
        search_box = page.locator(
            SEARCH_XPATH
        ).first

        search_box.wait_for(
            state="visible",
            timeout=15000
        )

        search_box.click()

        search_box.fill("Monthly Usage")

        print("✅ Entered Monthly Usage")

        page.wait_for_timeout(3000)

        # Click Monthly Usage
        click_element(
            page,
            MONTHLY_USAGE_XPATH,
            "Monthly Usage"
        )

        page.screenshot(
            path="monthly_usage_opened.png",
            full_page=True
        )

        # Click Close
        click_element(
            page,
            CLOSE_XPATH,
            "Close"
        )

        # Click Home
        click_element(
            page,
            HOME_XPATH,
            "Home"
        )

        page.screenshot(
            path="home_page.png",
            full_page=True
        )

        print(
            "\n🎉 Monthly Usage flow completed successfully"
        )

    except TimeoutError as e:

        print(
            f"\n❌ Monthly Usage flow failed: {e}"
        )

    finally:

        browser.close()