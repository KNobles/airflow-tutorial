import os
from selenium import webdriver
from multiprocessing import get_context
from multiprocessing import cpu_count
from selenium.webdriver.common.by import By
class Scraper:
    root_url = "https://www.immoweb.be/en"
    search_apartment_url = root_url + "/search/apartment/for-sale" 
    search_house_url = root_url + "/search/house/for-sale"
    search_property_type_url = [search_apartment_url, search_house_url]

    def _get_properties_url(page_num):
        path = os.path.join(os.getcwd(), "driver/geckodriver")
        options = webdriver.FirefoxOptions()
        options.headless = True
        driver = webdriver.Firefox(executable_path=path,options=options)
        items = []
        for property_type in Scraper.search_property_type_url:
            # print(f"PAGE N°{page_num} of {property_type}")
            driver.get(property_type + f"?countries=BE&isAPublicSale=false&page={page_num}&orderBy=newest")
            elements = driver.find_elements(By.XPATH, '//h2[@class="card__title card--result__title"]')
            for item in elements:
                items.append(item.find_element(By.CLASS_NAME, "card__title-link").get_attribute("href"))
        driver.close()
        print(items)
        return items

    def write_property_urls():
        os.makedirs(name="data", exist_ok=True)
        # Merge /app with /data => /app/data
        data_folder_path = os.path.join(os.getcwd(), "data")
        data_file_location = os.path.join(data_folder_path, "realestate_urls.csv")
        with open(data_file_location, "a+", encoding="utf-8") as cache:
            existing = [l.rstrip("\n") for l in cache.readlines()]
        with get_context("fork").Pool(int(cpu_count() / 2)) as pool:
            urls_generator = list(tuple(pool.map(Scraper._get_properties_url, range(1, 6))))
        with open(data_file_location, "a+", encoding="utf-8") as realestate_file:
            for property_url in urls_generator:
                for url in property_url:
                    if url not in existing:
                        realestate_file.write(url + "\n")
        print("Done writing!")