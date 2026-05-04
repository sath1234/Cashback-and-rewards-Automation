from playwright.sync_api import sync_playwright

CDP_ENDPOINT = "http://127.0.0.1:9222"
REWARDS_URL = "https://rewards.santabrowser.com"

def main():
    with sync_playwright() as p:
        print("Connecting to browser...")
        browser = p.chromium.connect_over_cdp(CDP_ENDPOINT)

        context = browser.contexts[0] if browser.contexts else browser.new_context()
        page = context.new_page()

        # 🔹 Open Rewards
        print("Opening Rewards page...")
        page.goto(REWARDS_URL)
        page.wait_for_timeout(5000)

        # 🔹 My Rewards
        print("Clicking My Rewards...")
        page.click("//span[normalize-space()='My Rewards']")
        page.wait_for_timeout(4000)

        # 🔹 Transactions
        print("Opening Transaction History...")
        page.click("#rewards-tab-transactions")
        page.wait_for_timeout(4000)

        # 🔹 Quests
        print("Opening Quests...")
        page.click("#rewards-tab-quests")
        page.wait_for_timeout(5000)

        # 🔹 Event Awards
        print("Clicking Event Awards...")
        page.click("//button[normalize-space()='Event Awards']")
        page.wait_for_timeout(4000)

        # 🔽 Scroll down
        page.mouse.wheel(0, 1200)
        page.wait_for_timeout(2000)

        # 🔹 Filters: Clicks, Impressions, Search, Misc
        for name in ["Clicks", "Impressions", "Search", "Misc"]:
            print(f"Clicking {name}...")
            page.click(f"//button[normalize-space()='{name}']")
            page.wait_for_timeout(3000)

        # 🔹 Quest Completions
        print("Clicking Quest Completions...")
        page.click("//button[normalize-space()='Quest Completions']")
        page.wait_for_timeout(4000)

        # 🔼 Scroll to top for tabs
        page.evaluate("window.scrollTo(0, 0)")
        page.wait_for_timeout(2000)

        # 🔹 Playwall
        print("Opening Playwall...")
        page.click("#rewards-tab-playwall")
        page.wait_for_timeout(4000)

        # 🔹 Cashback
        print("Opening Cashback...")
        page.click("#rewards-tab-cashback")
        page.wait_for_timeout(4000)

        print("✅ Flow completed successfully (without Referral)")

        page.wait_for_timeout(3000)
        page.close()


if __name__ == "__main__":
    main()