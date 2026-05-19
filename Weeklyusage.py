import requests
from playwright.sync_api import sync_playwright, TimeoutError

CDP_ENDPOINT = "http://127.0.0.1:9222"
REWARDS_URL = "https://rewards.santabrowser.com"

CLID = "8da91acc7b09930"

# 🔹 Weekly API
API_URL = f"https://api.santabrowser.com/quests/bff/v1/quests/q.santa.system.usage/system-status?clid={CLID}"

# 🔹 Selectors
QUEST_XPATH = "//nav[@class='flex-1 pr-1']//span[text()='Quests']"

FILTER_SELECTOR = "//div[@class='hidden md:flex items-center justify-between gap-3']//button[text()='Filter']"

USAGE_XPATH = "//div[@class='space-y-3']//button[text()='Usage']"

APPLY_SELECTOR = "//div[@class='mb-3 flex items-center justify-between']//button[text()='Apply']"

WEEKLY_USAGE_XPATH = "//div[@class='grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 hero3:grid-cols-4 wide:grid-cols-5 gap-2 md:gap-3']//h3[text()='Weekly Usage']"


def get_usage():
    try:
        response = requests.get(API_URL, timeout=10)
        data = response.json()

        progress = data.get("progress", 0)
        goal = data.get("goal", 0)

        # 🔥 CUSTOM WEEKLY LOGIC (420 threshold)
        if progress >= 420:
            status = "✅ COMPLETED"
        else:
            status = "⏳ IN PROGRESS"

        return {
            "progress": progress,
            "goal": goal,
            "status": status
        }

    except Exception as e:
        print("❌ API Error:", e)
        return None


def print_usage(label, usage):
    if usage:
        print(f"\n--- {label} ---")
        print(f"Usage   : {usage['progress']} / {usage['goal']}")
        print(f"Status  : {usage['status']}")


def main():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP_ENDPOINT)
        context = browser.contexts[0] if browser.contexts else browser.new_context()
        page = context.new_page()

        print("Opening Rewards page...")
        page.goto(REWARDS_URL, timeout=60000)
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_timeout(5000)

        try:
            # 🔹 Quest Category
            page.wait_for_selector(QUEST_XPATH, timeout=15000)
            page.click(QUEST_XPATH)
            page.wait_for_timeout(2000)

            # 🔹 Filter
            page.wait_for_selector(FILTER_SELECTOR, timeout=15000)
            page.click(FILTER_SELECTOR)
            page.wait_for_timeout(2000)

            # 🔹 Usage
            page.wait_for_selector(USAGE_XPATH, timeout=15000)
            page.click(USAGE_XPATH)
            page.wait_for_timeout(2000)

            # 🔹 Apply
            page.wait_for_selector(APPLY_SELECTOR, timeout=15000)
            page.click(APPLY_SELECTOR)
            page.wait_for_timeout(3000)

        except TimeoutError:
            print("❌ Navigation failed")

        # 🔹 BEFORE
        before = get_usage()
        print_usage("BEFORE WEEKLY USAGE", before)

        try:
            # 🔹 Weekly Usage
            weekly = page.wait_for_selector(WEEKLY_USAGE_XPATH, timeout=15000)
            weekly.click()

            print("\nClicked Weekly Usage, waiting 30 seconds...")
            page.wait_for_timeout(30000)

        except TimeoutError:
            print("❌ Weekly Usage element not found")

        # 🔹 AFTER
        after = get_usage()
        print_usage("AFTER WEEKLY USAGE", after)

        # 🔥 RESULT
        if before and after:
            diff = after["progress"] - before["progress"]
            print("\n--- RESULT ---")
            print(f"Usage Increased By: {diff}")
            print(f"Final Status     : {after['status']}")

        page.close()


if __name__ == "__main__":
    main()