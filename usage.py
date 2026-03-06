from playwright.sync_api import sync_playwright, TimeoutError

CDP_ENDPOINT = "http://127.0.0.1:9222"
REWARDS_URL = "https://rewards.santabrowser.com"


def open_and_close_quest(page, quest_name):
    quest_xpath = f"//h3[text()='{quest_name}']"
    close_xpath = "//button[@aria-label='Close']"

    # Open quest
    page.wait_for_selector(f"xpath={quest_xpath}", timeout=30000)
    page.click(f"xpath={quest_xpath}")
    print(f"✅ {quest_name} opened")

    page.wait_for_timeout(4000)

    # Close popup
    page.wait_for_selector(f"xpath={close_xpath}", timeout=30000)
    page.click(f"xpath={close_xpath}")
    print("✅ Popup closed")

    page.wait_for_timeout(2000)


def main():
    with sync_playwright() as p:

        print("Connecting to browser...")
        browser = p.chromium.connect_over_cdp(CDP_ENDPOINT)

        context = browser.contexts[0] if browser.contexts else browser.new_context()
        page = context.new_page()

        print("Opening Rewards page...")
        page.goto(REWARDS_URL, timeout=60000)

        try:
            page.wait_for_load_state("domcontentloaded")
            page.wait_for_timeout(5000)

            # Click Quests category
            page.click("xpath=//span[text()='Quests']/ancestor::a")
            print("✅ Quests category clicked")

            page.wait_for_timeout(3000)

            # Click Usage filter
            page.click("xpath=//button[@role='tab' and text()='Usage']")
            print("✅ Usage filter selected")

            page.wait_for_timeout(3000)

            # Open and close quests
            open_and_close_quest(page, "Daily Usage")
            open_and_close_quest(page, "Weekly Usage")
            open_and_close_quest(page, "Monthly Usage")

        except TimeoutError:
            print("❌ Element not found")

        page.close()
        print("✅ Page closed")


if __name__ == "__main__":
    main()