from playwright.sync_api import sync_playwright, TimeoutError

CDP_ENDPOINT = "http://127.0.0.1:9222"
REWARDS_URL = "https://rewards.santabrowser.com"


# --- SWITCH TO EXISTING NTP ---
def switch_to_ntp(context):
    for page in context.pages:
        try:
            url = page.url or ""
            title = page.title() if page.url else ""

            if (
                "newtab" in url
                or url in ("about:blank", "")
                or "New Tab" in title
            ):
                page.bring_to_front()
                page.wait_for_timeout(1500)
                print("✅ Switched to NTP")
                return page
        except Exception:
            pass

    print("❌ No existing NTP tab found")
    return None


# --- OPEN REWARDS (SPA SAFE) ---
def open_rewards_page(page):
    try:
        page.goto(REWARDS_URL, timeout=20000)
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_timeout(3000)
        print("🏆 Rewards page opened")
        return True
    except Exception as e:
        print(f"❌ Failed to open Rewards: {e}")
        return False


# --- FIND REWARDS IFRAME ---
def find_rewards_frame(page):
    for frame in page.frames:
        try:
            if frame.locator("//nav").count() > 0:
                print("✅ Rewards iframe detected")
                return frame
        except Exception:
            continue

    print("❌ Rewards iframe not found")
    return None


# --- GENERIC CATEGORY CLICKER (REWARDS SAFE) ---
def click_rewards_category(frame, category_name):
    xpath = f"//a[.//span[normalize-space()='{category_name}']]"

    try:
        locator = frame.locator(xpath).first

        # 🔥 If Rewards is already active, skip
        if category_name == "Rewards":
            class_attr = locator.get_attribute("class") or ""
            if "active" in class_attr or "selected" in class_attr:
                print("ℹ️ Rewards already active, skipping click")
                return True

        locator.wait_for(state="visible", timeout=15000)
        locator.scroll_into_view_if_needed()
        frame.page.wait_for_timeout(500)
        locator.click(force=True)

        print(f"✅ Clicked '{category_name}' category")
        return True

    except TimeoutError:
        print(f"❌ '{category_name}' category not visible")
        return False

    except Exception as e:
        print(f"❌ Failed to click '{category_name}': {e}")
        return False


# --- CLICK ALL REWARDS CATEGORIES ---
def click_all_rewards_categories(page):
    categories = [
        "Rewards",   # handled safely
        "Quests",
        "Spaces",
        "Rank",
       
    ]

    frame = find_rewards_frame(page)
    if not frame:
        return

    for category in categories:
        click_rewards_category(frame, category)
        page.wait_for_timeout(1200)  # UI transition wait


# --- MAIN ---
def main():
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp(CDP_ENDPOINT)
            context = browser.contexts[0]
        except Exception as e:
            print(f"❌ CDP connection failed: {e}")
            return

        page = switch_to_ntp(context)
        if not page:
            return

        if open_rewards_page(page):
            click_all_rewards_categories(page)


if __name__ == "__main__":
    main()
