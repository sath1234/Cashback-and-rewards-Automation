from playwright.sync_api import sync_playwright, TimeoutError

CDP_ENDPOINT = "http://127.0.0.1:9222"

# Change CLID Here
CLID = "8da91acc7b09930"

# APIs
SUMMARY_API = f"https://api.santabrowser.com/quests/bff/v1/user/{CLID}/summary-lite"
BADGES_API = f"https://api.santabrowser.com/quests/bff/v1/user/{CLID}/badges"

# Profile XPath
PROFILE_XPATH = "(//*[@d='m115.5 51.75a63.75 63.75 0 0 0-10.5 126.63v14.09a115.5 115.5 0 0 0-53.729 19.027 115.5 115.5 0 0 0 128.46 0 115.5 115.5 0 0 0-53.729-19.029v-14.084a63.75 63.75 0 0 0 53.25-62.881 63.75 63.75 0 0 0-63.65-63.75 63.75 63.75 0 0 0-0.09961 0z'])[2]"

# Badge XPath
BADGE_XPATH = "(//*[@class='relative flex h-14 w-14 items-center justify-center rounded-full bg-card border border-border shadow-sm transition-transform group-hover:scale-[1.03]'])[1]"

with sync_playwright() as p:

    try:
        # Connect Browser
        browser = p.chromium.connect_over_cdp(CDP_ENDPOINT)

        # Existing Context
        context = browser.contexts[0]

        # Create New Page
        page = context.new_page()

        # Store Summary Data
        user_summary = {}

        # Store Badge Data
        badge_data = {}

        # Capture API Responses
        def handle_response(response):

            global user_summary
            global badge_data

            # ================= SUMMARY API =================
            if SUMMARY_API in response.url:

                print("\n✅ Summary Lite API Triggered")

                if response.status == 200:

                    try:
                        data = response.json()

                        # Root Response
                        user_summary["clid"] = data.get("clid")
                        user_summary["username"] = data.get("username")

                        # Wallet Data
                        wallet = data.get("wallet", {})

                        user_summary["points_total"] = wallet.get("points_total")
                        user_summary["points_balance"] = wallet.get("points_balance")

                        user_summary["cash_total"] = wallet.get("cash_cents_total")
                        user_summary["cash_balance"] = wallet.get("cash_cents_balance")

                        user_summary["cash_pending"] = wallet.get("cash_cents_pending")

                        print("✅ User Summary Data Captured Successfully")

                    except Exception as e:
                        print("❌ Summary API Parsing Failed:", e)

            # ================= BADGES API =================
            if BADGES_API in response.url:

                print("\n✅ Badges API Triggered")

                if response.status == 200:

                    try:
                        data = response.json()

                        # Get badges list
                        badges = data.get("badges", [])

                        # Total badges count
                        total_badges = len(badges)

                        badge_data["total_badges"] = total_badges

                        print(f"\n✅ Total Badges Found : {total_badges}")

                        # Store badges
                        badge_data["badges"] = []

                        for index, badge in enumerate(badges):

                            badge_info = {
                                "id": badge.get("id"),
                                "key": badge.get("key"),
                                "name": badge.get("name"),
                                "rarity": badge.get("rarity")
                            }

                            badge_data["badges"].append(badge_info)

                            print(f"\nBadge Index : {index}")
                            print(f"ID      : {badge.get('id')}")
                            print(f"Key     : {badge.get('key')}")
                            print(f"Name    : {badge.get('name')}")
                            print(f"Rarity  : {badge.get('rarity')}")

                        print("\n✅ Badge Data Captured Successfully")

                    except Exception as e:
                        print("❌ Badges API Parsing Failed:", e)

        # Listen API Responses
        page.on("response", handle_response)

        # Open Rewards Website
        page.goto(
            "https://rewards.santabrowser.com",
            wait_until="networkidle"
        )

        print("✅ Rewards Page Opened")

        page.wait_for_timeout(5000)

        # ================= CLICK PROFILE =================
        profile_icon = page.locator(PROFILE_XPATH)

        profile_icon.wait_for(
            state="visible",
            timeout=15000
        )

        profile_icon.click()

        print("✅ Clicked My Profile")

        # Wait for Summary API
        page.wait_for_timeout(5000)

        # ================= CLICK BADGE =================
        badge_button = page.locator(BADGE_XPATH)

        badge_button.wait_for(
            state="visible",
            timeout=15000
        )

        badge_button.click()

        print("✅ Clicked Badge")

        # Wait for Badges API
        page.wait_for_timeout(8000)

        # ================= FINAL OUTPUT =================

        print("\n================ USER SUMMARY ================\n")

        print(f"CLID                 : {user_summary.get('clid')}")
        print(f"Username             : {user_summary.get('username')}")

        print(f"\nPoints Total         : {user_summary.get('points_total')}")
        print(f"Points Balance       : {user_summary.get('points_balance')}")

        print(f"\nCash Total (Cents)   : {user_summary.get('cash_total')}")
        print(f"Cash Balance(Cents)  : {user_summary.get('cash_balance')}")
        print(f"Cash Pending(Cents)  : {user_summary.get('cash_pending')}")

        print("\n================ BADGES SUMMARY ================\n")

        print(f"Total Badges : {badge_data.get('total_badges')}")

        print("\n================ BADGES LIST ================\n")

        for badge in badge_data.get("badges", []):

            print(f"ID      : {badge.get('id')}")
            print(f"Key     : {badge.get('key')}")
            print(f"Name    : {badge.get('name')}")
            print(f"Rarity  : {badge.get('rarity')}")
            print("----------------------------------------")

        print("\n================================================")

    except TimeoutError:
        print("❌ Element Not Found")

    except Exception as e:
        print("❌ Error:", e)

    finally:
        page.close()

        print("\n✅ Browser Page Closed")