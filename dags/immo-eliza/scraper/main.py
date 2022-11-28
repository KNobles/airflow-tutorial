import os
import pathlib
from utils.url_scraper import Scraper
from utils.property_data_scraper import PropertyDataWriter

os.chdir(pathlib.Path(os.path.dirname(__file__)))
Scraper.write_property_urls()
PropertyDataWriter.write_data_to_file()