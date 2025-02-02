
# Call this method to get the news in string format stored in a list.
# News is from NRK's topp saker feed

import requests
import feedparser
from bs4 import BeautifulSoup
import re

def getNews(num):
    newsList = []
    # Get the urls from the RSS feed
    #rssFeed = feedparser.parse("https://www.nrk.no/toppsaker.rss")
    rssFeed = feedparser.parse("http://feeds.bbci.co.uk/news/rss.xml")
    count = 0
    # Parse each of rss feed entries
    for entry in rssFeed.entries:
        if (count >= num):
            break
        
        # Get the link to the story
        pageUrl = entry.link
        
        # Get the news document from the link
        response = requests.get(pageUrl)

        # Parse the document using soup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Get all text with the CSS element text-body (damn you NRK!)
        #cssBodyElement = soup.select('.text-body')
        cssBodyElement = soup.select('.ssrcss-1q0x1qg-Paragraph')

        # Loop through the elements and put the processed text content in the list
        finalText = ""
        for element in cssBodyElement:
            text = re.sub(r'\s+', ' ', element.get_text().strip())
            if (text == "" or text == " " or text == "\n"):
                pass
            else:
                finalText += text

        # Remove BBC quotes 
        for substring in ["2023 BBC", "The BBC is not responsible for the content of external sites.", "Read about our approach to external linking.", 
                          "Sign up for our morning newsletter and get BBC News in your inbox.", "This video can not be played", "Â©"]:
            if(substring in finalText):
                finalText = finalText.replace(substring, "")

        if (len(finalText) < 150):
            #Skip if the article is empty/too short
            continue
        newsList.append({"article":finalText, "URL":pageUrl})

        count += 1
    
    return newsList

#return newsList

#print(pageUrl)
#print("")
#print(str(data.keys()))

#print(body_content)

if __name__ == "__main__":
    print(str(getNews(20)))