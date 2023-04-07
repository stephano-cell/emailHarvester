from bs4 import BeautifulSoup
import requests
import requests.exceptions
import urllib.parse
from collections import deque
import re

#Prompt the user to enter the target URL to scan

user_url = str(input('[+] Enter Target URL To Scan: '))
#Initialize a deque object with the entered URL as the initial value

urls = deque([user_url])

#Initialize two sets to store scraped URLs and email addresses

scraped_urls = set()
emails = set()

#Initialize a counter variable to keep track of the number of URLs processed

count = 0
try:
#Continue processing URLs until the deque object is empty or the count reaches 500 
# (can be adjusted to any value the bigger the count the longer the time)    
    while len(urls):
        count += 1
        if count == 500:
            break
# Pop the leftmost URL from the deque object and add it to the scraped URLs set
        url = urls.popleft()
        scraped_urls.add(url)
# Split the URL into its constituent parts (scheme, netloc, path, etc.)
        parts = urllib.parse.urlsplit(url)
# Construct the base URL from the scheme and netloc using string formatting
        base_url = '{0.scheme}://{0.netloc}'.format(parts)
# Extract the path from the URL and construct the full URL if it is a relative path
        path = url[:url.rfind('/')+1] if '/' in parts.path else url
# Print a message indicating that the URL is being processed
        print('[%d] Processing %s' % (count, url))
        try:
# Retrieve the URL using the requests library
            response = requests.get(url)
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError,requests.exceptions.InvalidURL):
 # If an exception is thrown during this process, continue to the next URL
            continue
# Search for email addresses in the response content using a regular expression
        new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I))
# Add any new email addresses found to the email addresses set
        emails.update(new_emails)

        soup = BeautifulSoup(response.text, features="lxml")
# Search for all anchor tags in the HTML content and construct the full URL for each anchor tag
        for anchor in soup.find_all("a"):
            link = anchor.attrs['href'] if 'href' in anchor.attrs else ''
            if link.startswith('/'):
                link = base_url + link
            elif not link.startswith('http'):
                link = path + link
# Add the URL to the deque object if it is not already in the deque object or the scraped URLs set

            if not link in urls and not link in scraped_urls:
                urls.append(link)
except KeyboardInterrupt:
    print('[-] Closing!')
#Print each email address found to the console
for mail in emails:
    print(mail)
