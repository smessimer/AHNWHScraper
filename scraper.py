# scraper.py
import sys, os
sys.path.append(os.path.dirname(__file__))

import requests
from pyquery import PyQuery as pq
import re

def ScrapeJobs():
    
    startUrl = "https://www.google.com/search?site=&source=hp&q=site%3Anews.ycombinator.com+hacker+news+who+is+hiring"
    response = requests.get(startUrl)
    doc = pq(response.content)

    regex = ".*item\?id=(\d+)"

    results = [pq(result).html() for result in doc('cite')]

    storyNums = [re.findall(regex, result) for result in results]

    print(storyNums)
    links = []
    for storyNum in storyNums:
        if storyNum:
            links.append(storyNum[0])

    print(links)

    links = ["https://news.ycombinator.com/item?id={}".format(link) for link in links]
    
    print(links)

    jobs = []

    for link in links:
        response = requests.get(link)
        doc = pq(response.content)
        for job in doc('div.comment'):
            jobs.append(pq(job).html())

    print(jobs)
    
    # Okay, we got the goods.  Now output to file that we'll open up on the site.
    try:
        if not os.path.exists("results"):
            os.makedirs("results")
    except OSError:
        pass
    filename = "results/results.html"
    try:
        os.remove(filename)
    except OSError:
        pass
    f = open(filename, 'w')
    html = "<html><head><link rel=\"stylesheet\" type=\"text/css\" href=\"news.css\">"
    html += "</head><body>"
    f.write(html)
    for j in jobs:
        f.write(j)
        f.write("<hr>")
    f.write("</body></html>")
    f.close()

    # Get the HN stylesheet
    cssUrl = "https://news.ycombinator.com/news.css"
    response = requests.get(cssUrl)
    filename = "results/news.css"
    try:
        os.remove(filename)
    except OSError:
        pass
    f = open(filename, 'w')
    f.write(response.text)
    f.close()


if __name__ == "__main__":
    ScrapeJobs()
