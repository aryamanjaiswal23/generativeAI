import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chromedriver_path = "/usr/bin/chromedriver"
service = Service(executable_path=chromedriver_path)
driver = webdriver.Chrome()
driver.get("https://autocatalogarchive.com/lancia/")
download_folder = "2020"
os.makedirs(download_folder, exist_ok=True)
try:
    elements = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located(
            (
                By.XPATH,
                '//div[contains(@onclick, "location.href")]',
            )
        )
    )

    for element in elements:
        onclick_attribute = element.get_attribute("onclick")
        url = onclick_attribute.split("'")[1] if onclick_attribute else None
        if url and url.endswith(f"{download_folder}-AU.pdf"):
            file_name = url.split("/")[-1]
            download_path = os.path.join(download_folder, file_name)
            response = requests.get(url)
            if response.status_code == 200:
                with open(download_path, "wb") as f:
                    f.write(response.content)
                print(f"Downloaded: {file_name}")
            else:
                print(f"Failed to download: {file_name}")

finally:
    driver.quit()
