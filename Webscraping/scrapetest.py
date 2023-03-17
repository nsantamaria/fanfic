import requests
from bs4 import BeautifulSoup
import csv
import time

# Define the CSV headers
headers = [
    "Title",
    "Author",
    "Date Published",
    "Commissioned For",
    "Summary",
    "Hits",
    "Kudos",
    "Comments",
    "Language",
    "Fandom",
    "Rating",
    "Warnings",
    "Chapters",
    "Words",
    "URL",
    "Story Body",
    "Category",
    "Characters",
    "Relationships",
    "Other Tags",
    "Bookmarks",
    "Collections"
]
page = 1
skipped = 0
# Open the CSV file in write mode
with open("brooklyn99-2.csv", "w", encoding="utf-8", newline="") as csv_file:
    # Create a CSV writer object
    csv_writer = csv.writer(csv_file)

    # Write the headers to the CSV file
    csv_writer.writerow(headers)

    done = False
    # Loop through all pages of search results until we reach the end
    while not done:
        url = f"https://archiveofourown.org/tags/Brooklyn%20Nine-Nine%20(TV)/works?page={page}"
        # Make a request to the URL
        try:
            response = requests.get(url, timeout=None)
        except:
            print("Error: Request timed out")
            time.sleep(5)
            continue

        response.headers[
            "User-Agent"
        ] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36"

        # Parse the HTML content using Beautiful Soup
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all the stories on the page
        stories = soup.find_all("li", {"class": "work"})

        # Loop through each story and extract the relevant information
        for story in stories:
            # Extract the title
            title_element = story.find("h4")
            title = title_element.text.strip().split("by")[0].strip()
            author_element = title_element.find("a", rel="author")

            if author_element is not None:
                author = author_element.text.strip()
            else:
                author = "Anonymous"

            commissioned_for_element = title_element.find(
                "a", href=lambda href: href and "/gifts" in href
            )
            if commissioned_for_element:
                commissioned_for = commissioned_for_element.text.strip()
            else:
                commissioned_for = "N/A"

            # Extract the summary
            body_element = story.find("blockquote", {"class": "userstuff summary"})
            if body_element is not None:
                summary = body_element.text.strip()
            else:
                summary = "N/A"

            # Extract the views
            views = story.find("dd", {"class": "hits"}).text.strip()

            # Extract the likes (kudos)
            likes_element = story.find("dd", {"class": "kudos"})
            if likes_element is not None:
                likes = likes_element.text.strip()
            else:
                likes = 0

            # Extract the date
            date_element = story.find("p", {"class": "datetime"})
            if date_element is not None:
                date = date_element.text.strip()
            else:
                date = "N/A"

            collections_element = story.find("dd", {"class": "collections"})
            if collections_element is not None:
                collections = collections_element.text.strip()
            else:
                collections = 0

            # Extract the bookmarks
            bookmarks_element = story.find("dd", {"class": "bookmarks"})
            if bookmarks_element is not None:
                bookmarks = bookmarks_element.text.strip()
            else:
                bookmarks = 0

            # Extract the tags
            tags_list = story.find("ul", {"class": "tags"})
            tags = [tag.text.strip() for tag in tags_list.find_all("a")]

            # Extract the Language
            language_element = story.find("dd", {"class": "language"})
            if language_element is not None:
                language = language_element.text.strip()
            else:
                language = "N/A"

            # Extract ratings and warnings
            warnings = []
            requiredTags = story.find("ul", {"class": "required-tags"}).find_all("li")
            ratings = requiredTags[0].find("span", {"class": "text"}).string
            warnings.append(requiredTags[1].find("span", {"class": "text"}).string)

            # Extract the number of comments
            comments_element = story.find("dd", {"class": "comments"})
            if comments_element is not None:
                comments = comments_element.text.strip()
            else:
                comments = 0

            # Extract the number of chapters
            chapters_element = story.find("dd", {"class": "chapters"})
            if chapters_element is not None:
                chapters = chapters_element.text.strip()
            else:
                chapters = "N/A"

            # Extract the number of words
            words_element = story.find("dd", {"class": "words"})
            words = words_element.text.strip()

            # Extract story link
            link_element = story.find("h4", {"class": "heading"})
            link = link_element.find("a")["href"]

            # Use the URL to get the story page
            # Try statement to skip stories with dead links
            try:
                story_url = "https://archiveofourown.org" + link + "style=disable"
                story_response = requests.get(story_url, timeout=None)
                story_soup = BeautifulSoup(story_response.content, "html.parser")

                # Check if there's a button to get the full text
                full_text_button = story_soup.find("li", {"class": "chapter entire"})
                if full_text_button is not None:
                    # Click the button to get the full text
                    print("Full text button found")
                    full_text_url = (
                        "https://archiveofourown.org"
                        + full_text_button.find("a")["href"]
                        + "style=disable"
                    )
                    full_text_response = requests.get(full_text_url, timeout=None)
                    full_text_soup = BeautifulSoup(
                        full_text_response.content, "html.parser"
                    )
                    story_body_element = full_text_soup.find(
                        "div", {"id": "chapters", "role": "article"}
                    )
                else:
                    story_body_element = story_soup.find("div", {"class": "userstuff"})
                
        

                # Extract the body of the story
                if story_body_element is not None:
                    story_body = story_body_element.text.strip()
                else:
                    story_body = "N/A"

                characters_list = story_soup.find("dd", {"class": "character tags"})
                if characters_list is not None:
                    characters = [c.text.strip() for c in characters_list.find_all("a")]
                else:
                    characters = "N/A"
                # Extract the character tags
                try:        
                    category_list = story_soup.find_all("dd", {"class": "category tags"})   

                    if category_list is not None:
                        category_soup = BeautifulSoup(str(category_list), "html.parser")
                    # Find all the <a> tags within the <ul> tag
                    tag_links = category_soup.find_all("ul", {"class": "commas"})[0].find_all("a")
                    if tag_links is not None:
                        category = [link.text for link in tag_links]
                except:
                    category = "N/A"

                # Extract the fandoms
                fandom_list = story_soup.find("dd", {"class": "fandom tags"})
                if fandom_list is not None:
                    fandom = [f.text.strip() for f in fandom_list.find_all("a")]
                else:
                    fandom = "N/A"

                # Extract the relationships
                relationships_list = story_soup.find(
                    "dd", {"class": "relationship tags"}
                )
                if relationships_list is not None:
                    relationships = [
                        r.text.strip() for r in relationships_list.find_all("a")
                    ]
                else:
                    relationships = "N/A"
                # Extract freeform tags
                freeform_list = story_soup.find("dd", {"class": "freeform tags"})
                if freeform_list is not None:
                    freeform = [f.text.strip() for f in freeform_list.find_all("a")]
                else:
                    freeform = "N/A"

            except Exception as e:
                print(f"(◡︵◡) Exception caught for link: {link}. Error message: {e}. Skipping story...")
                skipped += 1
                print (f"We have skipped {skipped} stories thus far")
                continue

            # output to CSV
            csv_writer.writerow(
                [
                    title,
                    author,
                    date,
                    commissioned_for,
                    summary,
                    views,
                    likes,
                    comments,
                    language,
                    fandom,
                    ratings,
                    warnings,
                    chapters,
                    words,
                    link,
                    story_body,
                    category,
                    characters,
                    relationships,
                    freeform,
                    bookmarks,
                    collections,
                ]
            )
            time.sleep(2)

            # Print out story title and date published once its written to CSV
            print(date, title)
            print()

            # Find the next page URL
            next_page = soup.find("li", {"class": "next"})

            # Go to that url
            try:
                next_page_url = next_page.find("a")["href"]
                page = next_page_url.split("=")[1]
            except:
                # If there's no next page, change our variable to stop the loop after the last story the page is scraped
                done = True
    else:
        print("Finished scraping, skipped ", skipped, "stories with dead links")

#To do:
#1. Figure out why some stories are skipped even though they have good links (FIXED)
#2. Can I decrease the sleep timer? Just use it in try/except statements? 
#3. Collections? Series? 
