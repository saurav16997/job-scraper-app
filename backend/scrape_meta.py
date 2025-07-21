from playwright.sync_api import sync_playwright
import json

def scrape_meta_jobs(keyword_filter=None):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        url = "https://www.metacareers.com/jobs/"
        page.goto(url)

        # Wait for job cards to load
        page.wait_for_selector("a.x1ypdohk")

        jobs = []
        job_elements = page.query_selector_all("a.x1ypdohk")

        for job in job_elements:
            # Title is inside a div with class "_6g3g ..."
            title_el = job.query_selector("div._6g3g")
            location_el = job.query_selector("div.x26uert")

            title = title_el.inner_text().strip() if title_el else "N/A"
            location = location_el.inner_text().strip() if location_el else ""

            href = job.get_attribute("href")
            full_url = "https://www.metacareers.com" + href if href else None

            if not full_url:
                continue

            # Filter by keyword on title only
            if keyword_filter and keyword_filter.lower() not in title.lower():
                continue

            # Optional: you can combine title and location if needed
            full_title = f"{title} ({location})" if location else title

            jobs.append({"title": full_title, "url": full_url})

        browser.close()
        return jobs

if __name__ == "__main__":
    keyword = input("Enter keyword to filter (or leave blank): ").strip()
    keyword = keyword if keyword else None

    jobs = scrape_meta_jobs(keyword_filter=keyword)

    print(f"Found {len(jobs)} jobs.")
    for job in jobs:
        print(f"- {job['title']}\n  {job['url']}\n")

    with open("meta_jobs.json", "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=2)
    print(f"Saved {len(jobs)} jobs to meta_jobs.json")
