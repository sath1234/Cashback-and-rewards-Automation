from playwright.sync_api import sync_playwright, TimeoutError

CDP_ENDPOINT = "http://127.0.0.1:9222"

REWARDS_URL = "https://rewards.santabrowser.com"

# 🔹 Category XPaths
SOCIAL_XPATH = "(//*[@class='text-[13px] font-semibold leading-tight tracking-tight text-foreground cat-label'])[1]"

VIDEO_XPATH = "(//*[@class='text-[13px] font-semibold leading-tight tracking-tight text-foreground cat-label'])[2]"

SPACES_XPATH = "(//*[@class='text-[13px] font-semibold leading-tight tracking-tight text-foreground cat-label'])[3]"

USAGE_XPATH = "(//*[@class='text-[13px] font-semibold leading-tight tracking-tight text-foreground cat-label'])[4]"

SURVEYS_XPATH = "(//*[@class='text-[13px] font-semibold leading-tight tracking-tight text-foreground cat-label'])[5]"


# ==================================================
# 🔹 Common Function
# ==================================================

def click_category(page, xpath, category_name):

    try:

        # 🔹 Wait for element
        page.wait_for_selector(xpath, timeout=15000)

        # 🔹 Scroll into view
        element = page.locator(xpath)

        element.scroll_into_view_if_needed()

        page.wait_for_timeout(2000)

        # 🔹 Click element
        element.click(force=True)

        print(f"✅ Clicked {category_name}")

        page.wait_for_timeout(5000)

        # 🔹 Go back to Home
        page.go_back()

        print(f"✅ Navigated back from {category_name}")

        page.wait_for_timeout(5000)

    except Exception as e:

        print(f"❌ Failed to click {category_name}: {e}")

        raise


# ==================================================
# 🔹 Setup Browser
# ==================================================

def setup_page():

    p = sync_playwright().start()

    browser = p.chromium.connect_over_cdp(CDP_ENDPOINT)

    context = (
        browser.contexts[0]
        if browser.contexts
        else browser.new_context()
    )

    page = context.new_page()

    page.goto(REWARDS_URL, timeout=60000)

    page.wait_for_load_state("domcontentloaded")

    page.wait_for_timeout(5000)

    return page, browser, p


# ==================================================
# 🔹 Test Social Category
# ==================================================

def test_social_category():

    page, browser, p = setup_page()

    click_category(page, SOCIAL_XPATH, "Social")

    page.close()

    browser.close()

    p.stop()


# ==================================================
# 🔹 Test Video Quest Category
# ==================================================

def test_video_category():

    page, browser, p = setup_page()

    click_category(page, VIDEO_XPATH, "Video Quest")

    page.close()

    browser.close()

    p.stop()


# ==================================================
# 🔹 Test Spaces Category
# ==================================================

def test_spaces_category():

    page, browser, p = setup_page()

    click_category(page, SPACES_XPATH, "Spaces")

    page.close()

    browser.close()

    p.stop()


# ==================================================
# 🔹 Test Usage Category
# ==================================================

def test_usage_category():

    page, browser, p = setup_page()

    click_category(page, USAGE_XPATH, "Usage")

    page.close()

    browser.close()

    p.stop()


# ==================================================
# 🔹 Test Surveys Category
# ==================================================

def test_surveys_category():

    page, browser, p = setup_page()

    click_category(page, SURVEYS_XPATH, "Surveys")

    page.close()

    browser.close()

    p.stop()