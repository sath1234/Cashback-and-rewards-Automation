from playwright.sync_api import sync_playwright

CDP_ENDPOINT = "http://127.0.0.1:9222"

CLID = "8da91acc7b09930"

REWARDS_URL = "https://rewards.santabrowser.com"

# Quest API
DEFAULT_BROWSER_API = f"https://api.santabrowser.com/quests/bff/v1/quests/q.santa.browser.default?clid={CLID}"

# XPaths
SET_DEFAULT_QUEST = "//div[@class='hidden hero3:grid hero3:grid-cols-4 gap-3 items-stretch']//div[contains(@class,'justify-between')]//h3[contains(text(),'Set Default Browser')]"

KEEP_SANTA_DEFAULT = "//div[@class='flex items-center gap-3']//button[text()='Keep Santa as Default']"

CLOSE_POPUP = "//*[@class='sr-only']"

with sync_playwright() as p:

    browser = p.chromium.connect_over_cdp(CDP_ENDPOINT)

    context = browser.contexts[0]

    page = context.new_page()

    # Default Status
    final_status = {"value": "Keep Santa as Default"}

    # Capture API Response
    def handle_response(response):

        try:

            if DEFAULT_BROWSER_API in response.url:

                print("\n✅ Default Browser Quest API Triggered")

                if response.status == 200:

                    final_status["value"] = "Santa is Default"

        except Exception as e:
            print("❌ API Parsing Failed:", e)

    page.on("response", handle_response)

    # Open Rewards Page
    page.goto(REWARDS_URL, wait_until="networkidle")

    page.wait_for_timeout(5000)

    # Click Set Default Browser Quest
    page.locator(SET_DEFAULT_QUEST).click()

    print("✅ Clicked Set Default Browser Quest")

    page.wait_for_timeout(3000)

    # Click Keep Santa As Default
    page.locator(KEEP_SANTA_DEFAULT).click()

    print("✅ Clicked Keep Santa As Default")

    # Wait For API Trigger
    page.wait_for_timeout(8000)

    # Close Popup
    page.locator(CLOSE_POPUP).click()

    print("✅ Popup Closed")

    page.wait_for_timeout(3000)

    # Final Output
    print("\n============= FINAL OUTPUT =============\n")

    print("STATUS :", final_status["value"])

    print("\n========================================")

    page.wait_for_timeout(5000)

    page.close()