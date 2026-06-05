from playwright.sync_api import sync_playwright

CDP_ENDPOINT = "http://127.0.0.1:9222"

REWARDS_URL = "https://rewards.santabrowser.com"

# ==================================================
# XPATHS
# ==================================================

MY_REWARDS_XPATH = (
    "//span[text()='My Rewards']"
)

APTOS_XPATH = (
    "//button[text()='Aptos']"
)

MIN_BALANCE_XPATH = (
    "//input[@placeholder='≥ $15']"
)

GET_QUOTE_XPATH = (
    "//button[text()='Get quote']"
)

# ==================================================
# COMMON CLICK FUNCTION
# ==================================================

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

# ==================================================
# MAIN SCRIPT
# ==================================================

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

    page.wait_for_load_state(
        "networkidle"
    )

    page.wait_for_timeout(5000)

    # ==================================================
    # Click My Rewards
    # ==================================================

    click_element(
        page,
        MY_REWARDS_XPATH,
        "My Rewards"
    )

    # ==================================================
    # Click Aptos
    # ==================================================

    click_element(
        page,
        APTOS_XPATH,
        "Aptos"
    )

    # ==================================================
    # Click Min $15
    # ==================================================

    click_element(
        page,
        MIN_BALANCE_XPATH,
        "Min $15"
    )

    # ==================================================
    # Enter Amount = 15
    # ==================================================

    amount_input = page.locator("//input").first

    amount_input.wait_for(
        state="visible",
        timeout=10000
    )

    amount_input.click()

    amount_input.fill("")

    amount_input.type("15")

    print("✅ Entered Amount : 15")

    page.wait_for_timeout(2000)

    # ==================================================
    # Click Get Quote
    # ==================================================

    click_element(
        page,
        GET_QUOTE_XPATH,
        "Get Quote"
    )

    page.wait_for_timeout(5000)

    # ==================================================
    # Screenshot
    # ==================================================

    page.screenshot(
        path="aptos_get_quote.png",
        full_page=True
    )

    print("\n✅ Aptos Get Quote flow completed successfully")

    browser.close()