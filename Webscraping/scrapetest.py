import requests
from bs4 import BeautifulSoup
import csv

page = 1
url = f"https://archiveofourown.org/tags/The%20Good%20Place%20%28TV%29/works"

# Make a request to the URL
response = requests.get(url)

# Parse the HTML content using Beautiful Soup
soup = BeautifulSoup(response.content, 'html.parser')

# Find all the stories on the page
stories = soup.find_all('li', {'class': 'work'})

# Loop through each story and extract the relevant information
import csv

# Define the CSV headers
headers = ['Title', 'Author', 'Commissioned For', 'Summary', 'Hits', 'Kudos', 'Comments', 'Language', 'Fandom', 'Rating', 'Warnings','Chapters', 'Words', 'URL', 'Story Body', 'Category', 'Characters', 'Relationships','Other Tags','Bookmarks']

# Open the CSV file in write mode
with open('output.csv', 'w', encoding='utf-8', newline='') as csv_file:
    # Create a CSV writer object
    csv_writer = csv.writer(csv_file)
    
    # Write the headers to the CSV file
    csv_writer.writerow(headers)
    for story in stories:
        # Extract the title
        title_element = story.find('h4')
        title = title_element.text.strip().split('by')[0].strip()
        author_element = title_element.find("a", rel="author")
        author = author_element.text.strip()
        commissioned_for_element = title_element.find("a", href=lambda href: href and "/gifts" in href)
        if commissioned_for_element:
            commissioned_for = commissioned_for_element.text.strip()
        else:
            commissioned_for = "N/A"


        # Extract the summary
        body_element = story.find('blockquote', {'class': 'userstuff summary'})
        if body_element is not None:
            summary = body_element.text.strip()
        else:
            summary = 'N/A'

        #Extract the fandom
        fandom_list = story.find_all("h5", {"class": "fandoms heading"})
        fandom = ', '.join([f.text.strip() for f in fandom_list])

        # Extract the views
        views = story.find('dd', {'class': 'hits'}).text.strip()

        # Extract the likes (kudos)
        likes_element = story.find('dd', {'class': 'kudos'})
        if likes_element is not None:
            likes = likes_element.text.strip()
        else:
            likes = 'N/A'

        #Extract the bookmarks
        bookmarks_element = story.find('dd', {'class': 'bookmarks'})
        if bookmarks_element is not None:
            bookmarks = bookmarks_element.text.strip()
        else:
            bookmarks = 0

        # Extract the tags
        tags_list = story.find('ul', {'class': 'tags'})
        tags = [tag.text.strip() for tag in tags_list.find_all('a')]

        #Extract the Language
        language_element = story.find('dd', {'class': 'language'})
        if language_element is not None:
            language = language_element.text.strip()
        else:
            language = 'N/A'


        ratings = []
        warnings = []
        requiredTags = story.find("ul", {"class": "required-tags"}).find_all("li")
        ratings.append(requiredTags[0].find("span", {"class": "text"}).string)
        warnings.append(requiredTags[1].find("span", {"class": "text"}).string)

        # Extract the number of comments
        comments_element = story.find('dd', {'class': 'comments'})
        if comments_element is not None:
            comments = comments_element.text.strip()
        else:
            comments = 'N/A'

        #Extract the number of chapters
        chapters_element = story.find('dd', {'class': 'chapters'})
        if chapters_element is not None:
            chapters = chapters_element.text.strip()
        else:
            chapters = 'N/A'

    
        #Extract the number of words
        words_element = story.find('dd', {'class': 'words'})


        #Extract story link
        link_element = story.find('h4', {'class': 'heading'})
        link = link_element.find('a')['href']

        #Use the URL to get the story page
        story_url = 'https://archiveofourown.org' + link
        story_response = requests.get(story_url)
        story_soup = BeautifulSoup(story_response.content, 'html.parser')
        #Extract the body of the story
        story_body_element = story_soup.find('div', {'class': 'userstuff'})
        if story_body_element is not None:
            story_body = story_body_element.text.strip()
        else:
            story_body = 'N/A'
        
        #Extract category tags
        category_list = story_soup.find_all("dd", {"class": "category tags"})
        category = ', '.join([c.text.strip() for c in category_list])

        #Extract the character tags
        characters_list = story_soup.find('dd', {'class': 'character tags'})
        if characters_list is not None:
            characters = [c.text.strip() for c in characters_list.find_all('a')]
        else:
            characters = 'N/A'
    
    #Extract the relationships
        relationships_list = story_soup.find('dd', {'class': 'relationship tags'})
        if relationships_list is not None:
            relationships = [r.text.strip() for r in relationships_list.find_all('a')]
        else:
            relationships = 'N/A'
    #Extract freeform tags
        freeform_list = story_soup.find('dd', {'class': 'freeform tags'})
        if freeform_list is not None:
            freeform = [f.text.strip() for f in freeform_list.find_all('a')]
        else:
            freeform = 'N/A'

    #GO to the next page
        next_page = soup.find('li', {'class': 'next'})
        if next_page is not None:
            next_url = next_page.find('a')['href']
            next_url = 'https://archiveofourown.org' + next_url
            next_response = requests.get(next_url)
            soup = BeautifulSoup(next_response.content, 'html.parser')
            stories = soup.find_all('li', {'class': 'work blurb group'})
               

        # Print out the extracted information for each story
        print('Title:', title)
        print('Author:', author)
        print('Summary:', summary)
        print('Hits:', views)
        print('Kudos:', likes)
        print('Comments:', comments)
        print('Language:', language)
        print('Chapters:', chapters)
        print('Fandom(s):', fandom)
        print('Rating:', ratings)
        print('Warnings:', warnings)
        print('Link', link)
        print('Category:', category)
        print('Characters:', characters)
        print('Relationships:', relationships)
        print('Other tags:', freeform)
        print('Bookmarks:', bookmarks)
        print('Comissioned for:', commissioned_for)
        print()

        #output to CSV

        csv_writer.writerow([title, author, commissioned_for, summary, views, likes, comments, language, fandom, ratings, warnings, chapters, words_element, link, story_body, category, characters, relationships, freeform, bookmarks])