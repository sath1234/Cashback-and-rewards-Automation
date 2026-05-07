from playwright.sync_api import sync_playwright, TimeoutError

CDP_ENDPOINT = "http://127.0.0.1:9222"
REWARDS_URL = "https://rewards.santabrowser.com/home?clid=8da91acc7b09930"

# 🔹 XPaths
SPACES_XPATH = "(//*[@class='truncate'])[2]"

TEXT_ITEM_XPATH = "(//*[contains(@class,'tracking-tight') and contains(@class,'text-xs')])[1]"

SIDEBAR_ACTIVE_XPATH = "(//*[contains(@class,'sidebar-active-glow')])[1]"


def main():
    with sync_playwright() as p:
        print("Connecting to browser...")
        browser = p.chromium.connect_over_cdp(CDP_ENDPOINT)

        context = browser.contexts[0] if browser.contexts else browser.new_context()
        page = context.new_page()

        # 🔹 Open Rewards Home with CLID
        print("Opening Rewards Home...")
        page.goto(REWARDS_URL, timeout=60000)
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_timeout(5000)

        try:
            # 🔹 Click Spaces
            print("Clicking Spaces...")
            page.wait_for_selector(SPACES_XPATH, timeout=15000)
            page.click(SPACES_XPATH)
            page.wait_for_timeout(3000)

            # 🔹 Click Text Item (index 1)
            print("Clicking Text Item...")
            page.wait_for_selector(TEXT_ITEM_XPATH, timeout=15000)
            page.click(TEXT_ITEM_XPATH)
            page.wait_for_timeout(3000)

            # 🔹 Click Sidebar Active Item
            print("Clicking Sidebar Active Item...")
            page.wait_for_selector(SIDEBAR_ACTIVE_XPATH, timeout=15000)
            page.click(SIDEBAR_ACTIVE_XPATH)
            page.wait_for_timeout(3000)

            print("✅ Flow completed successfully")

        except TimeoutError:
            print("❌ One of the elements not found")

        # 📸 Screenshot
        page.screenshot(path="final_flow.png", full_page=True)

        page.close()
        print("Done")


if __name__ == "__main__":
    main()