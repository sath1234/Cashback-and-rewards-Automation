import requests
from playwright.sync_api import sync_playwright, TimeoutError

CDP_ENDPOINT = "http://127.0.0.1:9222"
REWARDS_URL = "https://rewards.santabrowser.com"

CLID = "8da91acc7b09930"
API_URL = f"https://api.santabrowser.com/quests/bff/v1/quests/q.santa.system.usage-daily/system-status?clid={CLID}"


def get_usage():
    try:
        response = requests.get(API_URL, timeout=10)
        data = response.json()

        progress = data.get("progress", 0)
        target = data.get("target", 0)

        # 🔥 CUSTOM DAILY LOGIC (121 threshold)
        if progress >= 121:
            status = "✅ COMPLETED"
        else:
            status = "⏳ IN PROGRESS"

        return {
            "progress": progress,
            "target": target,
            "status": status
        }

    except Exception as e:
        print("❌ API Error:", e)
        return None


def print_usage(label, usage):
    if usage:
        print(f"\n--- {label} ---")
        print(f"Usage   : {usage['progress']} / {usage['target']}")
        print(f"Status  : {usage['status']}")


def main():
    with sync_playwright() as p:
        print("Connecting to browser...")
        browser = p.chromium.connect_over_cdp(CDP_ENDPOINT)

        context = browser.contexts[0] if browser.contexts else browser.new_context()
        page = context.new_page()

        print("Opening Rewards page...")
        page.goto(REWARDS_URL, timeout=60000)
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_timeout(8000)

        # 🔹 BEFORE
        before = get_usage()
        print_usage("BEFORE USAGE", before)

        try:
            daily_usage = page.wait_for_selector(
                "(//div[contains(@class,'flex') and contains(@class,'flex-col') and contains(@class,'justify-between')])[6]",
                timeout=15000
            )

            daily_usage.click()
            print("\nClicked Daily Usage, waiting 30 seconds...")
            page.wait_for_timeout(30000)

        except TimeoutError:
            print("❌ Daily Usage element not found")

        # 🔹 AFTER
        after = get_usage()
        print_usage("AFTER USAGE", after)

        # 🔥 DIFFERENCE
        if before and after:
            diff = after["progress"] - before["progress"]
            print("\n--- RESULT ---")
            print(f"Usage Increased By: {diff}")
            print(f"Final Status     : {after['status']}")

        page.close()


if __name__ == "__main__":
    main()