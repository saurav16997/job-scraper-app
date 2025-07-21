from playwright.sync_api import sync_playwright
import json

def scrape_google_jobs(keyword_filter=None):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        url = "https://www.google.com/about/careers/applications/jobs/results/"
        page.goto(url)

        # Wait for job cards
        page.wait_for_selector("a[jsname='hSRGPd']")

        jobs = []
        job_elements = page.query_selector_all("a[jsname='hSRGPd']")

        for job in job_elements:
            title = job.get_attribute("aria-label") or job.inner_text()
            href = job.get_attribute("href")
            full_url = "https://www.google.com" + href if href else None

            if not full_url:
                continue

            if keyword_filter and keyword_filter.lower() not in title.lower():
                continue

            jobs.append({"title": title.strip(), "url": full_url})

        browser.close()
        return jobs

if __name__ == "__main__":
    keyword = input("Enter keyword to filter (or leave blank): ").strip()
    keyword = keyword if keyword else None

    jobs = scrape_google_jobs(keyword_filter=keyword)

    print(f"Found {len(jobs)} jobs.")
    for job in jobs:
        print(f"- {job['title']}\n  {job['url']}\n")

    with open("google_jobs.json", "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=2)
    print(f"Saved {len(jobs)} jobs to google_jobs.json")
