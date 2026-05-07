import requests
from datetime import datetime
from playwright.sync_api import sync_playwright, TimeoutError

CDP_ENDPOINT = "http://127.0.0.1:9222"
REWARDS_URL = "https://rewards.santabrowser.com"

CLID = "8da91acc7b09930"

# 🔹 Daily Check-in API
API_URL = f"https://api.santabrowser.com/quests/bff/v1/quests/q.daily.checkin/checkin-status?clid={CLID}"

# 🔹 Selectors
QUEST_XPATH = "(//span[@class='truncate'])[1]"

FILTER_SELECTOR = "[class='inline-flex items-center justify-center whitespace-nowrap text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 ring-offset-background border px-3 h-9 rounded-full border-foreground/10 bg-foreground/5 text-foreground hover:bg-foreground/10 hover:text-foreground']"

USAGE_XPATH = "//button[@class='whitespace-nowrap rounded-full border px-3 py-1.5 text-xs hover:bg-white/80 dark:hover:bg-white/15 border-sky-200 text-sky-700 bg-sky-50/70 dark:border-sky-400/40 dark:text-sky-200/80 dark:bg-sky-500/10']"

APPLY_SELECTOR = "[class='inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 ring-offset-background bg-primary text-primary-foreground hover:opacity-90 h-8 px-3']"

# 🔹 Daily Check-in Quest Card
DAILY_CHECKIN_CARD = "(//*[@class='tracking-tight font-display text-sm font-semibold mt-5 leading-snug text-slate-900 dark:text-white line-clamp-2'])[1]"

# 🔹 Daily Check-in Button
DAILY_CHECKIN_BUTTON = "//button[@class='inline-flex items-center justify-center whitespace-nowrap text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 ring-offset-background bg-primary text-primary-foreground hover:opacity-90 h-10 px-4 py-2 flex-1 rounded-full']"


def get_checkin_status():
    try:
        response = requests.get(API_URL, timeout=10)
        data = response.json()

        print("API RESPONSE:", data)

        # 🔹 Handle nested response
        if "data" in data:
            data = data["data"]

        last_checkin_ymd = data.get("last_checkin_ymd")

        today_date = datetime.now().strftime("%Y-%m-%d")

        # 🔹 Check status
        if last_checkin_ymd == today_date:
            return "COMPLETED"
        else:
            return "NOT_COMPLETED"

    except Exception as e:
        print("❌ API Error:", e)
        return None


def main():

    with sync_playwright() as p:

        # 🔹 Connect to existing browser
        browser = p.chromium.connect_over_cdp(CDP_ENDPOINT)

        context = (
            browser.contexts[0]
            if browser.contexts
            else browser.new_context()
        )

        page = context.new_page()

        print("Opening Rewards page...")

        page.goto(REWARDS_URL, timeout=60000)

        page.wait_for_load_state("domcontentloaded")

        page.wait_for_timeout(5000)

        try:

            # 🔹 Click Quest Category
            page.wait_for_selector(QUEST_XPATH, timeout=15000)
            page.click(QUEST_XPATH)

            print("✅ Clicked Quest Category")

            page.wait_for_timeout(2000)

            # 🔹 Click Filter
            page.wait_for_selector(FILTER_SELECTOR, timeout=15000)
            page.click(FILTER_SELECTOR)

            print("✅ Clicked Filter")

            page.wait_for_timeout(2000)

            # 🔹 Click Usage
            page.wait_for_selector(USAGE_XPATH, timeout=15000)
            page.click(USAGE_XPATH)

            print("✅ Clicked Usage")

            page.wait_for_timeout(2000)

            # 🔹 Click Apply
            page.wait_for_selector(APPLY_SELECTOR, timeout=15000)
            page.click(APPLY_SELECTOR)

            print("✅ Clicked Apply")

            page.wait_for_timeout(5000)

        except TimeoutError:
            print("❌ Navigation failed")
            page.close()
            return

        # 🔥 Get current Daily Check-in status
        status = get_checkin_status()

        print(f"\nCurrent Status : {status}")

        # 🔹 If already completed
        if status == "COMPLETED":

            print("✅ Daily Check-in already completed today")

        # 🔹 If not completed then click
        elif status == "NOT_COMPLETED":

            try:

                print("⏳ Daily Check-in not completed")

                # 🔹 Click Daily Check-in Quest Card
                page.wait_for_selector(DAILY_CHECKIN_CARD, timeout=15000)

                page.click(DAILY_CHECKIN_CARD)

                print("✅ Clicked Daily Check-in card")

                page.wait_for_timeout(3000)

                # 🔹 Click Daily Check-in Button
                page.wait_for_selector(DAILY_CHECKIN_BUTTON, timeout=15000)

                page.click(DAILY_CHECKIN_BUTTON)

                print("✅ Clicked Daily Check-in button")

                page.wait_for_timeout(10000)

                # 🔹 Verify updated status
                updated_status = get_checkin_status()

                print(f"\nUpdated Status : {updated_status}")

                if updated_status == "COMPLETED":
                    print("🎉 Daily Check-in completed successfully")

                else:
                    print("❌ Daily Check-in still pending")

            except TimeoutError:
                print("❌ Daily Check-in elements not found")

        else:
            print("❌ Unable to fetch Daily Check-in status")

        page.close()


if __name__ == "__main__":
    main()