from copy import deepcopy
import datetime
import logging
from time import time
from urllib.parse import urljoin
from scrappers.rental_offer import RentalOffer
from scrappers.base import ScrapperBase
from scrappers.rental_offer import RentalOffer
from time import time
import requests
from urllib.parse import urljoin
import re


class ScraperSreality(ScrapperBase):
    """
    https://dspace.cvut.cz/bitstream/handle/10467/103384/F8-BP-2021-Malach-Ondrej-thesis.pdf?sequence=-1&isAllowed=y

    Workflow:
    go to the GUI of sreality.cz, click what you want, you get the url:
    https://www.sreality.cz/hledani/prodej/byty,domy?region=Kol%C3%ADn&region-id=3412&region-typ=municipality
    


    """

    name = "Sreality"
    logo_url = "https://www.sreality.cz/img/icons/android-chrome-192x192.png"
    color = 0xCC0000
    base_url = "https://www.sreality.cz/api/cs/v2/estates?"

    _base_config = {"url": None,  # use this to override the logic
                    "API_INSIDE_URL_SELECTIONS": ""
                    }


    """
    disposition_mapping = {
        Disposition.FLAT_1KK: "2",
        Disposition.FLAT_1: "3",
        Disposition.FLAT_2KK: "4",
        Disposition.FLAT_2: "5",
        Disposition.FLAT_3KK: "6",
        Disposition.FLAT_3: "7",
        Disposition.FLAT_4KK: "8",
        Disposition.FLAT_4: "9",
        Disposition.FLAT_5_UP: ("10", "11", "12"),
        Disposition.FLAT_OTHERS: "16",
    }
    """

    _category_type_to_url = {
        0: "vse",
        1: "prodej",
        2: "pronajem",
        3: "drazby"
    }

    _category_main_to_url = {
        0: "vse",
        1: "byt",
        2: "dum",
        3: "pozemek",
        4: "komercni",
        5: "ostatni"
    }

    _category_sub_to_url = {
            2: "1+kk",
            3: "1+1",
            4: "2+kk",
            5: "2+1",
            6: "3+kk",
            7: "3+1",
            8: "4+kk",
            9: "4+1",
            10: "5+kk",
            11: "5+1",
            12: "6-a-vice",
            16: "atypicky",
            47: "pokoj",
            37: "rodinny",
            39: "vila",
            43: "chalupa",
            33: "chata",
            35: "pamatka",
            40: "na-klic",
            44: "zemedelska-usedlost",
            19: "bydleni",
            18: "komercni",
            20: "pole",
            22: "louka",
            21: "les",
            46: "rybnik",
            48: "sady-vinice",
            23: "zahrada",
            24: "ostatni-pozemky",
            25: "kancelare",
            26: "sklad",
            27: "vyrobni-prostor",
            28: "obchodni-prostor",
            29: "ubytovani",
            30: "restaurace",
            31: "zemedelsky",
            38: "cinzovni-dum",
            49: "virtualni-kancelar",
            32: "ostatni-komercni-prostory",
            34: "garaz",
            52: "garazove-stani",
            50: "vinny-sklep",
            51: "pudni-prostor",
            53: "mobilni-domek",
            36: "jine-nemovitosti",
            57: "Unknown",
        }
    
    def __init__(self, config):
        super().__init__(config)


    def _create_link_to_offer(self, offer) -> str:
        return urljoin(self.base_url, "/detail" +
            "/" + self._category_type_to_url[offer["seo"]["category_type_cb"]] +
            "/" + self._category_main_to_url[offer["seo"]["category_main_cb"]] +
            "/" + self._category_sub_to_url[offer["seo"]["category_sub_cb"]] +
            "/" + offer["seo"]["locality"] +
            "/" + str(offer["hash_id"]))

    def build_response(self) -> requests.Response:
        #url = self.base_url + "/api/cs/v2/estates?category_main_cb=1&category_sub_cb="
        #url += "|".join(self.get_dispositions_data())
        #url += "&category_type_cb=2&locality_district_id=72&locality_region_id=14&per_page=20"
        #url += "&tms=" + str(int(time()))
        url = "https://www.sreality.cz/hledani/prodej/byty?region=Kol%C3%ADn&region-id=3412&region-typ=municipality"

        url = self._config["url"]
        if url is None:  # not overriden:
            url = self.base_url + self._config["API_INSIDE_URL_SELECTIONS"] + "&tms=" + str(int(time()))

        logging.debug("Sreality request: %s", url)

        return requests.get(url, headers=self.headers)

    def get_latest_offers(self) -> list[RentalOffer]:
        response = self.build_response().json()

        items: list[RentalOffer] = []

        for item in response["_embedded"]["estates"]:
            # Ignorovat "tip" nabídky, které úplně neodpovídají filtrům a mění se s každým vyhledáváním
            if item["region_tip"] > 0:
                continue

            title = item["name"].replace(u'\xa0', u' ')
            
            items.append(
                RentalOffer(
                src=self.name,
                raw=deepcopy(item),
                link = self._create_link_to_offer(item),
                title = title,
                location = item["locality"],
                price = item["price_czk"]["value_raw"],
                image_url = item["_links"]["image_middle2"][0]["href"],      
                estate_type=self._category_main_to_url[item["category"]],  
                disposition=self._category_sub_to_url[item["seo"]["category_sub_cb"]],
                offer_type=self._category_type_to_url[item["seo"]["category_type_cb"]],
                charges=None,
                # todo category check jestli je category energeticka?
                ))

        return items
