import json
import time
from scholarly import scholarly

# Google Scholar Author ID
SCHOLAR_ID = "8G1qo1gAAAAJ"

# Output file
JSON_FILE = "publications.json"

def fetch_scholar_publications():
    """Fetches publications from Google Scholar and formats them in APA style with links."""
    print("📢 Fetching publications from Google Scholar...")

    try:
        author = scholarly.search_author_id(SCHOLAR_ID)
        scholarly.fill(author, sections=["publications"])

        publications = []
        for pub in author["publications"]:
            scholarly.fill(pub)  # Get full publication details

            # ✅ Ensure bib_data is always a dictionary
            bib_data = pub.get("bib") or {}

            # Extract details
            authors = bib_data.get("author", "Unknown")
            year = str(bib_data.get("pub_year", "")).strip()
            title = bib_data.get("title", "")
            journal = bib_data.get("journal", "")
            volume = bib_data.get("volume", "")  # Extract Volume
            issue = bib_data.get("number", "")   # Extract Issue
            pages = bib_data.get("pages", "")    # Extract Pages
            link = pub.get("pub_url", "#")  # Default to "#" if no link

            # Format volume, issue, and pages
            vol_issue = f"{volume}({issue})" if volume and issue else volume or issue
            page_text = f", {pages}" if pages else ""

            # APA citation as a clickable link
            apa_format = f'<a href="{link}" target="_blank" style="text-decoration: none; color: inherit;">' \
                         f'{authors} {"(" + year + ")" if year else ""}. <b>{title}</b>. <i>{journal}</i>' \
                         f'{", " + vol_issue if vol_issue else ""}{page_text}.</a>'

            publications.append({
                "authors": authors,
                "year": year if year else None,  # Exclude empty years
                "title": title,
                "journal": journal,
                "volume_issue": vol_issue,
                "pages": pages,
                "apa_citation": apa_format
            })

            time.sleep(1)  # Prevent getting blocked

        # ✅ Fix: Sort by year only if it's available
        publications = sorted(publications, key=lambda x: int(x["year"]) if x["year"] and x["year"].isdigit() else -1, reverse=True)

        # Save to JSON
        with open(JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(publications, f, indent=4)

        print("✅ Publications updated successfully!")

    except Exception as e:
        print("🚨 Error fetching publications:", e)

# Fetch publications when the script runs
fetch_scholar_publications()
