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


# --- OPEN REWARDS PAGE ---
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


# --- CLICK RANK CATEGORY ---
def click_rank_category(frame):
    rank_xpath = "//a[normalize-space()='Rank']"

    try:
        locator = frame.locator(rank_xpath).first
        locator.wait_for(state="visible", timeout=15000)
        locator.scroll_into_view_if_needed()
        frame.page.wait_for_timeout(500)
        locator.click(force=True)

        print("✅ Rank category clicked")
        return True

    except TimeoutError:
        print("❌ Rank category not visible")
        return False

    except Exception as e:
        print(f"❌ Failed to click Rank: {e}")
        return False


# --- CLICK WEEKLY / MONTHLY / YEARLY ---
def click_weekly_monthly_yearly(frame):
    tabs = ["weekly", "monthly", "yearly"]

    for tab in tabs:
        xpath = f"//button[@type='button' and normalize-space()='{tab}']"

        try:
            locator = frame.locator(xpath).first
            locator.wait_for(state="visible", timeout=10000)
            locator.scroll_into_view_if_needed()
            frame.page.wait_for_timeout(500)
            locator.click(force=True)

            print(f"✅ Clicked {tab}")
            frame.page.wait_for_timeout(2000)

        except TimeoutError:
            print(f"❌ {tab} tab not visible")

        except Exception as e:
            print(f"❌ Failed to click {tab}: {e}")


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
            frame = find_rewards_frame(page)
            if frame and click_rank_category(frame):
                frame.page.wait_for_timeout(2000)
                click_weekly_monthly_yearly(frame)


if __name__ == "__main__":
    main()
