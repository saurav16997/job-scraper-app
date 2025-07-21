from playwright.sync_api import sync_playwright
import json

def scrape_amazon_jobs(keyword_filter=None):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        url = "https://amazon.jobs/content/en/job-categories/business-intelligence-data-engineering"
        page.goto(url)

        # Wait for job links to load
        page.wait_for_selector("a.header-module_desktop__Dnj66.header-module_title__9-W3R")

        jobs = []
        job_elements = page.query_selector_all("a.header-module_desktop__Dnj66.header-module_title__9-W3R")

        for job in job_elements:
            title = job.inner_text().strip()
            href = job.get_attribute("href")
            full_url = "https://www.amazon.jobs" + href if href else None
            
            if not full_url:
                continue

            if keyword_filter and keyword_filter.lower() not in title.lower():
                continue

            jobs.append({"title": title, "url": full_url})

        browser.close()
        return jobs

if __name__ == "__main__":
    keyword = input("Enter keyword to filter (or leave blank): ").strip()
    keyword = keyword if keyword else None

    jobs = scrape_amazon_jobs(keyword_filter=keyword)

    print(f"Found {len(jobs)} jobs.")
    for job in jobs:
        print(f"- {job['title']}\n  {job['url']}\n")

    # Save to JSON
    with open("amazon_jobs.json", "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=2)
    print(f"Saved {len(jobs)} jobs to amazon_jobs.json")
