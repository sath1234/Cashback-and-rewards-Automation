import pytest
from playwright.sync_api import sync_playwright

CDP_ENDPOINT = "http://127.0.0.1:9222"

# API Endpoints
ALL_API = "https://api.santabrowser.com/quests/bff/v1/leaderboard?period=all&limit=50"
WEEKLY_API = "https://api.santabrowser.com/quests/bff/v1/leaderboard?period=weekly&limit=50"
MONTHLY_API = "https://api.santabrowser.com/quests/bff/v1/leaderboard?period=monthly&limit=50"
YEARLY_API = "https://api.santabrowser.com/quests/bff/v1/leaderboard?period=yearly&limit=50"


@pytest.fixture(scope="session")
def browser_context():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP_ENDPOINT)
        context = browser.contexts[0]
        yield context


def test_rank_all_weekly_monthly_yearly_leaderboard(browser_context):

    page = browser_context.new_page()

    all_api_data = None
    weekly_api_data = None
    monthly_api_data = None
    yearly_api_data = None

    # Capture APIs
    def handle_response(response):
        nonlocal all_api_data
        nonlocal weekly_api_data
        nonlocal monthly_api_data
        nonlocal yearly_api_data

        # ALL API
        if ALL_API in response.url:

            print("\n✅ ALL Leaderboard API Triggered")
            print("URL:", response.url)
            print("Status:", response.status)

            assert response.status == 200, \
                "❌ ALL API status code is not 200"

            try:
                all_api_data = response.json()

                if "data" in all_api_data:

                    total_users = len(all_api_data["data"])

                    print(f"✅ ALL Top Users Count: {total_users}")

                    assert total_users == 50, \
                        f"❌ Expected 50 users but got {total_users}"

            except Exception as e:
                pytest.fail(f"❌ ALL API JSON Parse Failed: {e}")

        # WEEKLY API
        if WEEKLY_API in response.url:

            print("\n✅ WEEKLY Leaderboard API Triggered")
            print("URL:", response.url)
            print("Status:", response.status)

            assert response.status == 200, \
                "❌ WEEKLY API status code is not 200"

            try:
                weekly_api_data = response.json()

                if "data" in weekly_api_data:

                    total_users = len(weekly_api_data["data"])

                    print(f"✅ WEEKLY Top Users Count: {total_users}")

                    assert total_users == 50, \
                        f"❌ Expected 50 users but got {total_users}"

            except Exception as e:
                pytest.fail(f"❌ WEEKLY API JSON Parse Failed: {e}")

        # MONTHLY API
        if MONTHLY_API in response.url:

            print("\n✅ MONTHLY Leaderboard API Triggered")
            print("URL:", response.url)
            print("Status:", response.status)

            assert response.status == 200, \
                "❌ MONTHLY API status code is not 200"

            try:
                monthly_api_data = response.json()

                if "data" in monthly_api_data:

                    total_users = len(monthly_api_data["data"])

                    print(f"✅ MONTHLY Top Users Count: {total_users}")

                    assert total_users == 50, \
                        f"❌ Expected 50 users but got {total_users}"

            except Exception as e:
                pytest.fail(f"❌ MONTHLY API JSON Parse Failed: {e}")

        # YEARLY API
        if YEARLY_API in response.url:

            print("\n✅ YEARLY Leaderboard API Triggered")
            print("URL:", response.url)
            print("Status:", response.status)

            assert response.status == 200, \
                "❌ YEARLY API status code is not 200"

            try:
                yearly_api_data = response.json()

                if "data" in yearly_api_data:

                    total_users = len(yearly_api_data["data"])

                    print(f"✅ YEARLY Top Users Count: {total_users}")

                    assert total_users == 50, \
                        f"❌ Expected 50 users but got {total_users}"

            except Exception as e:
                pytest.fail(f"❌ YEARLY API JSON Parse Failed: {e}")

    page.on("response", handle_response)

    # Open Rewards Page
    page.goto("https://rewards.santabrowser.com", wait_until="networkidle")

    page.wait_for_timeout(5000)

    # STEP 1 -> Click Rank Category
    rank_category = page.locator(
        "(//*[@class='group relative flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm transition-all duration-200 text-foreground/80 hover:bg-accent/50 hover:text-foreground'])[4]"
    )

    rank_category.wait_for(state="visible", timeout=15000)

    rank_category.click()

    print("✅ Clicked Rank Category")

    # Wait for ALL API
    page.wait_for_timeout(8000)

    # Validate ALL API
    assert all_api_data is not None, \
        "❌ ALL API not captured"

    # STEP 2 -> Click Weekly Category
    weekly_button = page.locator(
        "(//*[@class='px-3 py-1.5 text-xs font-medium rounded-full transition-colors capitalize text-muted-foreground hover:text-foreground'])[1]"
    )

    weekly_button.wait_for(state="visible", timeout=15000)

    weekly_button.click()

    print("✅ Clicked Weekly Leaderboard")

    # Wait for WEEKLY API
    page.wait_for_timeout(8000)

    # Validate WEEKLY API
    assert weekly_api_data is not None, \
        "❌ WEEKLY API not captured"

    # STEP 3 -> Click Monthly Category
    monthly_button = page.locator(
        "(//*[@class='px-3 py-1.5 text-xs font-medium rounded-full transition-colors capitalize text-muted-foreground hover:text-foreground'])[2]"
    )

    monthly_button.wait_for(state="visible", timeout=15000)

    monthly_button.click()

    print("✅ Clicked Monthly Leaderboard")

    # Wait for MONTHLY API
    page.wait_for_timeout(8000)

    # Validate MONTHLY API
    assert monthly_api_data is not None, \
        "❌ MONTHLY API not captured"

    # STEP 4 -> Click Yearly Category
    yearly_button = page.locator(
        "(//*[@class='px-3 py-1.5 text-xs font-medium rounded-full transition-colors capitalize text-muted-foreground hover:text-foreground'])[3]"
    )

    yearly_button.wait_for(state="visible", timeout=15000)

    yearly_button.click()

    print("✅ Clicked Yearly Leaderboard")

    # Wait for YEARLY API
    page.wait_for_timeout(8000)

    # Validate YEARLY API
    assert yearly_api_data is not None, \
        "❌ YEARLY API not captured"

    print("\n✅ ALL, WEEKLY, MONTHLY and YEARLY Leaderboard APIs Validated Successfully")

    page.close()