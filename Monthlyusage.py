import requests
from playwright.sync_api import sync_playwright, TimeoutError

CDP_ENDPOINT = "http://127.0.0.1:9222"
REWARDS_URL = "https://rewards.santabrowser.com"

CLID = "40e8930bf7fdbf2"

# 🔹 Monthly API
API_URL = f"https://api.santabrowser.com/quests/bff/v1/quests/q.santa.system.usage-monthly/system-status?clid={CLID}"

# 🔹 Selectors
QUEST_XPATH = "(//span[@class='truncate'])[1]"

FILTER_SELECTOR = "[class='inline-flex items-center justify-center whitespace-nowrap text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 ring-offset-background border px-3 h-9 rounded-full border-foreground/10 bg-foreground/5 text-foreground hover:bg-foreground/10 hover:text-foreground']"

USAGE_XPATH = "//button[@class='whitespace-nowrap rounded-full border px-3 py-1.5 text-xs hover:bg-white/80 dark:hover:bg-white/15 border-sky-200 text-sky-700 bg-sky-50/70 dark:border-sky-400/40 dark:text-sky-200/80 dark:bg-sky-500/10']"

APPLY_SELECTOR = "[class='inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 ring-offset-background bg-primary text-primary-foreground hover:opacity-90 h-8 px-3']"

# 🔹 Monthly Usage XPath
MONTHLY_USAGE_XPATH = "(//*[@class='tracking-tight font-display text-sm font-semibold mt-5 leading-snug text-slate-900 dark:text-white line-clamp-2'])[4]"

def get_usage():
    try:
        response = requests.get(API_URL, timeout=10)
        data = response.json()

        progress = data.get("progress", 0)
        goal = data.get("goal", 0)

        # 🔥 CUSTOM MONTHLY LOGIC (600 threshold)
        if progress >= 600:
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
        print_usage("BEFORE MONTHLY USAGE", before)

        try:
            # 🔹 Monthly Usage
            monthly = page.wait_for_selector(MONTHLY_USAGE_XPATH, timeout=15000)
            monthly.click()

            print("\nClicked Monthly Usage, waiting 30 seconds...")
            page.wait_for_timeout(30000)

        except TimeoutError:
            print("❌ Monthly Usage element not found")

        # 🔹 AFTER
        after = get_usage()
        print_usage("AFTER MONTHLY USAGE", after)

        # 🔥 RESULT
        if before and after:
            diff = after["progress"] - before["progress"]
            print("\n--- RESULT ---")
            print(f"Usage Increased By: {diff}")
            print(f"Final Status     : {after['status']}")

        page.close()


if __name__ == "__main__":
    main()