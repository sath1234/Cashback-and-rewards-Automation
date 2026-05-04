from playwright.sync_api import sync_playwright, TimeoutError

CDP_ENDPOINT = "http://127.0.0.1:9222"
REWARDS_URL = "https://rewards.santabrowser.com"

OVERVIEW_XPATH = "(//button[@class='inline-flex items-center justify-center whitespace-nowrap text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 ring-offset-background border h-9 rounded-full px-4 font-semibold border-border bg-transparent hover:bg-primary/10 hover:border-primary hover:text-primary transition-colors'])[2]"

REFERRAL_XPATH = "(//button[@class='h-8 px-3 text-xs rounded-full transition-colors whitespace-nowrap shrink-0 hover:bg-muted'])[3]"

def main():
    with sync_playwright() as p:
        print("Connecting to browser...")
        browser = p.chromium.connect_over_cdp(CDP_ENDPOINT)

        context = browser.contexts[0] if browser.contexts else browser.new_context()
        page = context.new_page()

        # 🔹 Open Rewards
        print("Opening Rewards page...")
        page.goto(REWARDS_URL, timeout=60000)
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_timeout(5000)

        # 🔹 Click Overview
        try:
            print("Clicking Overview...")
            page.wait_for_selector(OVERVIEW_XPATH, timeout=15000)
            page.click(OVERVIEW_XPATH)
            page.wait_for_timeout(4000)
        except TimeoutError:
            print("❌ Overview not found")

        # 🔹 Click Referral
        try:
            print("Clicking Referral...")
            page.wait_for_selector(REFERRAL_XPATH, timeout=15000)
            page.click(REFERRAL_XPATH)
            page.wait_for_timeout(4000)
            print("✅ Referral clicked successfully")
        except TimeoutError:
            print("❌ Referral not found")

        # 📸 Screenshot
        page.screenshot(path="overview_referral.png", full_page=True)

        page.close()
        print("Done")


if __name__ == "__main__":
    main()