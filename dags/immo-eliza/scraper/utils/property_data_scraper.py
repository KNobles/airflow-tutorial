import os
import json
import pandas as pd

from requests import Session
from bs4 import BeautifulSoup
from collections import defaultdict
from utils.property_data_selection import Property
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils.upload_file import upload_file

class PropertyDataWriter:

    def _get_columns():
        columns = [
        "id",
        "locality",
        "postal_code",
        "region",
        "province",
        "type_of_property",
        "subtype_of_property",
        "type_of_sale",
        "price",
        "number_of_bedrooms",
        "surface",
        "kitchen_type",
        "fully_equipped_kitchen",
        "furnished",
        "open_fire",
        "terrace",
        "terrace_surface",
        "garden",
        "garden_surface",
        "land_surface",
        "number_of_facades",
        "swimming_pool",
        "state_of_the_building"
        ]
        return columns

    def _append_to_dict(property_url: str, property_data_dictionary):
        sess = Session()
        try :
            req = sess.get(property_url, timeout=20)
            if req.status_code == 200:
                soup = BeautifulSoup(req.content, "html.parser")
                script = soup.find('script',attrs={"type" :"text/javascript"})
                property = Property(json.loads(script.contents[0][33:-10]))
                print(f"Scraping property {property.id}")
                property_data_dictionary["id"].append(property.id)
                property_data_dictionary["locality"].append(property.locality)
                property_data_dictionary["postal_code"].append(property.postal_code)
                property_data_dictionary["region"].append(property.region)
                property_data_dictionary["province"].append(property.province)
                property_data_dictionary["type_of_property"].append(property.type)
                property_data_dictionary["subtype_of_property"].append(property.sub_type)
                property_data_dictionary["type_of_sale"].append(property.sale_type)
                property_data_dictionary["price"].append(property.price)
                property_data_dictionary["number_of_bedrooms"].append(property.bedroom_count)
                property_data_dictionary["surface"].append(property.surface)
                property_data_dictionary["kitchen_type"].append(property.kitchen_type)
                property_data_dictionary["fully_equipped_kitchen"].append(property.is_kitchen_fully_equipped)
                property_data_dictionary["furnished"].append(property.is_furnished)
                property_data_dictionary["open_fire"].append(property.has_open_fire)
                property_data_dictionary["terrace"].append(property.has_terrace)
                property_data_dictionary["terrace_surface"].append(property.terrace_surface)
                property_data_dictionary["garden"].append(property.has_garden)
                property_data_dictionary["garden_surface"].append(property.garden_surface)
                property_data_dictionary["number_of_facades"].append(property.facade_count)
                property_data_dictionary["land_surface"].append(property.land_surface)
                property_data_dictionary["swimming_pool"].append(property.has_swimming_pool)
                property_data_dictionary["state_of_the_building"].append(property.building_state)
            return property_data_dictionary
        except Exception as e:
            print(e)

    def write_data_to_file():
        dic = defaultdict(list)
        new_dic = {}
        data_folder_path = os.path.join(os.getcwd(), "data")
        urls_file_path = os.path.join(data_folder_path, "realestate_urls.csv")
        data_file_path = os.path.join(data_folder_path, "properties.csv")

        with open(urls_file_path, "r") as f:
            with ThreadPoolExecutor(max_workers=12) as exec:
                res = [exec.submit(PropertyDataWriter._append_to_dict, url, dic) for url in f.readlines()]
        
        for future in as_completed(res):
            try:
                re = dict(future.result())
                new_dic.update(re)
            except TypeError as e:
                continue

        data = pd.DataFrame(new_dic, columns=PropertyDataWriter._get_columns())
        
        if os.path.exists(urls_file_path):
            data.to_csv(data_file_path, mode="a", index="False", header="False")
        else:
            data.to_csv(data_file_path, mode="a", index="False", header="False")
        print("Uploading file...")
        upload_file(data_file_path, "properties_data_akl.csv")