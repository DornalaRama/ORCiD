from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Base URL for pagination
base_search_url = "https://orcid.org/orcid-search/search?searchQuery=metaphysics&pageSize=200&pageIndex="

start_page = 0       # starting page index
max_pages = 1        # number of pages to extract (46 → 51)
all_data = []

# Loop through pages
for page_index in range(start_page, start_page + max_pages):
    url = base_search_url + str(page_index)
    driver.get(url)
    time.sleep(3)  # wait to load page fully

    profile_links = driver.find_elements(By.CSS_SELECTOR, "a[href^='/000']")
    if not profile_links:
        break  # stop if no profiles on page

    profile_urls = [link.get_attribute('href') for link in profile_links]

    # Loop through profile links on this page
    for profile_url in profile_urls:
        driver.get(profile_url)
        time.sleep(2)

        try:
            name_element = driver.find_element(By.CSS_SELECTOR, "h1.orc-ui-font-heading")
            name = name_element.text.strip()
        except NoSuchElementException:
            name = "Name not found"

        try:
            email_element = driver.find_element(By.CSS_SELECTOR, "span.row.orc-font-body-small")
            email = email_element.text.strip()
        except NoSuchElementException:
            email = "Email not found"

        all_data.append({'url': profile_url, 'name': name, 'email': email})

        driver.back()
        time.sleep(1)

# Save results into a CSV file
with open('orcid_profiles_upto_5_pages.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['url', 'name', 'email']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for entry in all_data:
        writer.writerow(entry)

driver.quit()
