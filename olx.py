from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

def scrape_olx(query="car-cover", output_file="olx_car_cover.csv"):
    url = f"https://www.olx.in/items/q-{query}"

    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # keep visible for debugging
    driver = webdriver.Chrome(options=options)

    driver.get(url)

    # wait until some links to items appear
    WebDriverWait(driver, 15).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li a"))
    )

    items = driver.find_elements(By.CSS_SELECTOR, "li a")
    results = []

    for item in items:
        try:
            title = item.text.strip().split("\n")[0]  # first line is usually title
        except:
            title = "N/A"

        try:
            # look for ₹ in the text block
            price = next((line for line in item.text.split("\n") if "₹" in line), "N/A")
        except:
            price = "N/A"

        try:
            # often last line is location
            lines = item.text.split("\n")
            location = lines[-1] if len(lines) > 1 else "N/A"
        except:
            location = "N/A"

        try:
            link = item.get_attribute("href")
        except:
            link = "N/A"

        if title != "N/A":  # ignore empty anchors
            results.append([title, price, location, link])

    driver.quit()

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Title", "Price", "Location", "Link"])
        writer.writerows(results)

    print(f"✅ Scraping completed. {len(results)} items saved in {output_file}")

if __name__ == "__main__":
    scrape_olx()
