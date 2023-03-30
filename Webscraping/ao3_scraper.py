import re
import requests
from bs4 import BeautifulSoup
import csv
import time

work_name = input("Please enter the work's name like it occurs in the search URL (eg 'South%20Park', 'The Good Place (TV)': ")
cleaned_work_name = re.sub(r'\W+', '_', work_name).strip('_')


print("It's scrapin' time!")

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36"
})

start_time = time.time()

def format_time(seconds):
    if seconds < 60:
        return f"{seconds:.0f} seconds"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        remaining_seconds = int(seconds % 60)
        return f"{minutes} minutes {remaining_seconds} seconds"
    else:
        hours = int(seconds // 3600)
        remaining_minutes = int((seconds % 3600) // 60)
        return f"{hours} hours {remaining_minutes} minutes"



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
    "Collections",
    "Series"
]
page = 1
skipped = 0
count = 1
total_stories = 0

# Open the CSV file in write mode
with open(f"{cleaned_work_name}.csv", "w", encoding="utf-8", newline="") as csv_file:
    # Create a CSV writer object
    csv_writer = csv.writer(csv_file)

    # Write the headers to the CSV file
    csv_writer.writerow(headers)

    done = False
    # Loop through all pages of search results until we reach the end

    skipped_stories = []

    while not done:

        # Create the URL for the page
        url = f"https://archiveofourown.org/tags/{work_name}/works?page={page}"

        
        # Make a request to the URL
        # Make a request to the URL
        try:
            response = requests.get(url, timeout=None)
            if response.status_code != 200:
                raise Exception(f"Error: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)
            continue

        response.headers[
            "User-Agent"
        ] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36"

        # Parse the HTML content using Beautiful Soup
        soup = BeautifulSoup(response.content, "html.parser")

        heading = soup.find("h2", {"class": "heading"})
        if heading:
            total_stories_text = heading.text.strip()
            total_stories_match = re.search(r"\d[\d,]*(?= Works)", total_stories_text)
            if total_stories_match:
                total_stories = int(total_stories_match.group(0).replace(",", ""))
        else:
            total_stories = 0

        if total_stories == 0:
            print("No search results found. Exiting loop.")
            break

        # Find all the stories on the page
        stories = soup.find_all("li", {"class": "work"})

        if not stories:
            print("No stories found. Exiting loop.")
            break

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

            # Part of a series?
            series_element = story.find("ul", {"class": "series"})
            if series_element is not None:
                series = series_element.text.strip()
            else:
                series = "N/A"

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
                retries = 0
                story_url = "https://archiveofourown.org" + link + "style=disable"
                story_response = session.get(story_url, timeout=None)
                story_soup = BeautifulSoup(story_response.content, "html.parser")

                retry_later_message = story_soup.find("pre")
                if retry_later_message and "Retry later" in retry_later_message.text:
                    print("Rate limited. Retrying...")
                    retries += 1
                    time.sleep(3)  # Increase the delay if rate limited
                    continue
                else:
                    current_time = time.time()
                    elapsed_time = current_time - start_time
                    stories_processed = count - 1
                    time_per_story = elapsed_time / stories_processed if stories_processed > 0 else 0
                    stories_remaining = total_stories - count
                    time_remaining = stories_remaining * time_per_story

                    remaining_time_str = (
                        "calculating time"
                        if stories_processed == 0
                        else format_time(time_remaining)
                    )

                    print(
                        f"Downloading story {count}/{total_stories}. "
                        f"{round(count/total_stories*100, 3)}% done. "
                        f"{total_stories - count} stories remaining. "
                        f"{remaining_time_str} remaining."
                    )
                    count += 1

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
                    full_text_response = session.get(full_text_url, timeout=None)
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
                print(f"Oh no! (ᗒᗣᗕ)! Exception caught for link: {link}. Error message: {e}. Skipping story...")
                skipped_stories.append({'title': title, 'date': date, 'url': link, 'error': e})
                skipped += 1
                print(f"We have skipped {skipped} stories thus far")
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
                    series
                    
                ]
            )
            time.sleep(5)

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
        print("☆彡(ノ^ ^)ノ Congratulations! Finished scraping! ヘ(^ ^ヘ)☆彡 \n skipped ", skipped, "stories with dead links")
        end_time = time.time()
        elapsed_time = end_time - start_time
        formatted_elapsed_time = format_time(elapsed_time)
        print(f"Total time taken: {formatted_elapsed_time}")

        with open("ao3_scrape_summary.txt", "w", encoding="utf-8") as summary_file:
            summary_file.write("Summary of Scraping Process\n")
            summary_file.write("===========================\n\n")
            
            # Total number of stories written
            summary_file.write(f"Total number of stories written: {count-1}\n")

            # Total time taken
            summary_file.write(f"Total time taken: {formatted_elapsed_time}\n")
            
            # Number of stories skipped and their details
            summary_file.write(f"Number of stories skipped: {skipped}\n\n")
            summary_file.write("Skipped Stories Details:\n")
            for skipped_story in skipped_stories:
                summary_file.write(f"Title: {skipped_story['title']}\n")
                summary_file.write(f"Date Published: {skipped_story['date']}\n")
                summary_file.write(f"URL: {skipped_story['url']}\n\n")
            
            # Total number of stories written
            summary_file.write(f"Total number of stories written: {count-1}\n")