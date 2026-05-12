from playwright.sync_api import sync_playwright

CDP_ENDPOINT = "http://127.0.0.1:9222"

# Enter Your CLID
CLID = "8da91acc7b09930"

# API Endpoints
ALL_CLID_API = f"https://api.santabrowser.com/quests/bff/v1/leaderboard/{CLID}?period=all"
WEEKLY_CLID_API = f"https://api.santabrowser.com/quests/bff/v1/leaderboard/{CLID}?period=weekly"
MONTHLY_CLID_API = f"https://api.santabrowser.com/quests/bff/v1/leaderboard/{CLID}?period=monthly"
YEARLY_CLID_API = f"https://api.santabrowser.com/quests/bff/v1/leaderboard/{CLID}?period=yearly"

with sync_playwright() as p:

    # Connect Browser
    browser = p.chromium.connect_over_cdp(CDP_ENDPOINT)

    context = browser.contexts[0]

    page = context.new_page()

    # Store Data
    all_data = {}
    weekly_data = {}
    monthly_data = {}
    yearly_data = {}

    # Capture API Responses
    def handle_response(response):

        global all_data
        global weekly_data
        global monthly_data
        global yearly_data

        try:

            # ================= ALL API =================
            if ALL_CLID_API in response.url:

                print("\n✅ ALL Rank API Triggered")

                if response.status == 200:

                    data = response.json()

                    user_data = data.get("data", data)

                    all_data["clid"] = CLID

                    all_data["name"] = (
                        user_data.get("displayName")
                        or user_data.get("username")
                        or user_data.get("userName")
                        or user_data.get("profileName")
                        or user_data.get("name")
                    )

                    all_data["points"] = user_data.get("points")
                    all_data["rank"] = user_data.get("rank")

                    print("🏆 ALL Rank Data Captured")

            # ================= WEEKLY API =================
            if WEEKLY_CLID_API in response.url:

                print("\n✅ WEEKLY Rank API Triggered")

                if response.status == 200:

                    data = response.json()

                    user_data = data.get("data", data)

                    weekly_data["clid"] = CLID

                    weekly_data["name"] = (
                        user_data.get("displayName")
                        or user_data.get("username")
                        or user_data.get("userName")
                        or user_data.get("profileName")
                        or user_data.get("name")
                    )

                    weekly_data["points"] = user_data.get("points")
                    weekly_data["rank"] = user_data.get("rank")

                    print("🏆 WEEKLY Rank Data Captured")

            # ================= MONTHLY API =================
            if MONTHLY_CLID_API in response.url:

                print("\n✅ MONTHLY Rank API Triggered")

                if response.status == 200:

                    data = response.json()

                    user_data = data.get("data", data)

                    monthly_data["clid"] = CLID

                    monthly_data["name"] = (
                        user_data.get("displayName")
                        or user_data.get("username")
                        or user_data.get("userName")
                        or user_data.get("profileName")
                        or user_data.get("name")
                    )

                    monthly_data["points"] = user_data.get("points")
                    monthly_data["rank"] = user_data.get("rank")

                    print("🏆 MONTHLY Rank Data Captured")

            # ================= YEARLY API =================
            if YEARLY_CLID_API in response.url:

                print("\n✅ YEARLY Rank API Triggered")

                if response.status == 200:

                    data = response.json()

                    user_data = data.get("data", data)

                    yearly_data["clid"] = CLID

                    yearly_data["name"] = (
                        user_data.get("displayName")
                        or user_data.get("username")
                        or user_data.get("userName")
                        or user_data.get("profileName")
                        or user_data.get("name")
                    )

                    yearly_data["points"] = user_data.get("points")
                    yearly_data["rank"] = user_data.get("rank")

                    print("🏆 YEARLY Rank Data Captured")

        except Exception as e:
            print("❌ API Parsing Failed:", e)

    page.on("response", handle_response)

    # Open Rewards Page
    page.goto(
        "https://rewards.santabrowser.com",
        wait_until="networkidle"
    )

    page.wait_for_timeout(5000)

    # STEP 1 -> Click Rank Category
    page.locator(
        "(//*[@class='truncate'])[4]"
    ).click()

    print("\n✅ Clicked Rank Category")

    # Wait for ALL API
    page.wait_for_timeout(8000)

    # STEP 2 -> Click Weekly Leaderboard
    page.locator(
        "(//*[@class='px-3 py-1.5 text-xs font-medium rounded-full transition-colors capitalize text-muted-foreground hover:text-foreground'])[1]"
    ).click()

    print("\n✅ Clicked Weekly Leaderboard")

    # Wait for WEEKLY API
    page.wait_for_timeout(8000)

    # STEP 3 -> Click Monthly Leaderboard
    page.locator(
        "(//*[@class='px-3 py-1.5 text-xs font-medium rounded-full transition-colors capitalize text-muted-foreground hover:text-foreground'])[2]"
    ).click()

    print("\n✅ Clicked Monthly Leaderboard")

    # Wait for MONTHLY API
    page.wait_for_timeout(8000)

    # STEP 4 -> Click Yearly Leaderboard
    page.locator(
        "(//*[@class='px-3 py-1.5 text-xs font-medium rounded-full transition-colors capitalize text-muted-foreground hover:text-foreground'])[3]"
    ).click()

    print("\n✅ Clicked Yearly Leaderboard")

    # Wait for YEARLY API
    page.wait_for_timeout(8000)

    # ================= FINAL OUTPUT =================

    print("\n================ FINAL OUTPUT ================\n")

    print("🏆 ALL CATEGORY")
    print("CLID   :", all_data.get("clid"))
    print("Name   :", all_data.get("name"))
    print("Points :", all_data.get("points"))
    print("Rank   :", all_data.get("rank"))

    print("\n--------------------------------------------\n")

    print("🏆 WEEKLY CATEGORY")
    print("CLID   :", weekly_data.get("clid"))
    print("Name   :", weekly_data.get("name"))
    print("Points :", weekly_data.get("points"))
    print("Rank   :", weekly_data.get("rank"))

    print("\n--------------------------------------------\n")

    print("🏆 MONTHLY CATEGORY")
    print("CLID   :", monthly_data.get("clid"))
    print("Name   :", monthly_data.get("name"))
    print("Points :", monthly_data.get("points"))
    print("Rank   :", monthly_data.get("rank"))

    print("\n--------------------------------------------\n")

    print("🏆 YEARLY CATEGORY")
    print("CLID   :", yearly_data.get("clid"))
    print("Name   :", yearly_data.get("name"))
    print("Points :", yearly_data.get("points"))
    print("Rank   :", yearly_data.get("rank"))

    print("\n================================================")

    page.close()