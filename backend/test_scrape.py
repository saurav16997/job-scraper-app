from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://amazon.jobs/content/en/job-categories/business-intelligence-data-engineering")
        page.wait_for_timeout(5000)  # wait 5 seconds
        browser.close()

if __name__ == "__main__":
    run()
