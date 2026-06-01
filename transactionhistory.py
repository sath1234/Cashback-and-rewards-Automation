from playwright.sync_api import sync_playwright

CDP_ENDPOINT = "http://127.0.0.1:9222"

REWARDS_URL = "https://rewards.santabrowser.com"

MY_REWARDS_XPATH = (
    "//nav[@class='flex-1 pr-1']//span[text()='My Rewards']"
)

TRANSACTION_HISTORY_XPATH = (
    "//button[text()='Transaction history']"
)

API_PATTERN = (
    "/quests/bff/v1/claims/token-claims/8da91acc7b09930"
)


def click_element(page, xpath, element_name):

    print(f"\n🔹 Clicking {element_name}")

    locator = page.locator(xpath).first

    locator.wait_for(
        state="visible",
        timeout=15000
    )

    locator.scroll_into_view_if_needed()

    locator.click(force=True)

    page.wait_for_timeout(2000)

    print(f"✅ Clicked {element_name}")


with sync_playwright() as p:

    browser = p.chromium.connect_over_cdp(
        CDP_ENDPOINT
    )

    context = (
        browser.contexts[0]
        if browser.contexts
        else browser.new_context()
    )

    page = context.new_page()

    print("\n🏆 Opening Rewards Page...")

    page.goto(
        REWARDS_URL,
        timeout=60000
    )

    page.wait_for_load_state("networkidle")

    # Click My Rewards
    click_element(
        page,
        MY_REWARDS_XPATH,
        "My Rewards"
    )

    # Capture API after clicking Transaction History
    with page.expect_response(
        lambda response:
        API_PATTERN in response.url
    ) as api_response:

        click_element(
            page,
            TRANSACTION_HISTORY_XPATH,
            "Transaction History"
        )

    response = api_response.value

    print("\n" + "=" * 70)
    print("API URL :", response.url)
    print("STATUS  :", response.status)

    clid = response.url.split("/")[-1]

    print("CLID    :", clid)
    print("=" * 70)

    # Get API response
    transactions = response.json()

    # Total transaction count
    total_transactions = len(transactions)

    # Total reward amount
    total_reward_amount = sum(
        txn.get("source_amount", 0)
        for txn in transactions
    )

    print(f"\n📊 TOTAL TRANSACTIONS : {total_transactions}")
    print(f"💰 TOTAL REWARD AMOUNT : {total_reward_amount}")

    print("\n" + "=" * 70)
    print("TRANSACTION DETAILS")
    print("=" * 70)

    for index, txn in enumerate(
        transactions,
        start=1
    ):

        print(f"\nTransaction #{index}")

        print(
            f"ID          : {txn.get('id')}"
        )

        print(
            f"CLID        : {txn.get('clid')}"
        )

        print(
            f"STATUS      : {txn.get('status')}"
        )

        print(
            f"AMOUNT      : {txn.get('source_amount')}"
        )

        print(
            f"TOKEN MICRO : {txn.get('token_amount_micro')}"
        )

        print(
            f"TX HASH     : {txn.get('tx_hash')}"
        )

        print(
            f"CREATED AT  : {txn.get('created_at')}"
        )

    # Validation
    if response.status == 200:
        print("\n✅ API STATUS CODE VERIFIED")
    else:
        print(
            f"\n❌ API FAILED WITH STATUS {response.status}"
        )

    page.screenshot(
        path="transaction_history.png",
        full_page=True
    )

    print("\n✅ Transaction History Validation Completed")

    browser.close()