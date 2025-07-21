from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import json
import os

app = FastAPI()

if not os.path.exists("static"):
    os.mkdir("static")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load jobs at startup
def load_jobs():
    jobs = []
    for company, file in {
        "Amazon": "amazon_jobs.json",
        "Google": "google_jobs.json",
        "Meta": "meta_jobs.json"
    }.items():
        if os.path.exists(file):
            with open(file, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    for job in data:
                        job["company"] = company
                    jobs.extend(data)
                except Exception as e:
                    print(f"Error loading {file}: {e}")
    return jobs

all_jobs = load_jobs()

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/jobs")
async def get_jobs(
    keyword: str = Query(None),
    location: str = Query(None),
    company: str = Query(None)
):
    filtered = all_jobs
    if company and company.lower() != "all":
        filtered = [job for job in filtered if job["company"].lower() == company.lower()]
    if keyword:
        filtered = [job for job in filtered if keyword.lower() in job.get("title", "").lower()]
    if location:
        filtered = [job for job in filtered if location.lower() in job.get("location", "").lower()]
    return filtered
