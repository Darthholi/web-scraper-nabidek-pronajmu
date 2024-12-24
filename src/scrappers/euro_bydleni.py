from copy import deepcopy
import json
import logging
import re
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from legacy.disposition import Disposition
from scrappers.rental_offer import RentalOffer
from scrappers.base import ScrapperBase
from scrappers.rental_offer import RentalOffer
from urllib.parse import urljoin
from bs4 import BeautifulSoup


class ScraperEuroBydleni(ScrapperBase):
    """
    
    Examples:
    "Brno": {
            "sql[locality][locality][input]": "Brno, Česko",
            "sql[locality][locality][city]": "Brno, Česko",
            "sql[locality][locality][zip_code]": "",
            "sql[locality][locality][types]": "locality",
            "sql[locality][location][lat]": "49.1950602",
            "sql[locality][location][lng]": "16.6068371",
            "sql[locality][viewport][south]": "49.10965517428777",
            "sql[locality][viewport][west]": "16.42806782678905",
            "sql[locality][viewport][north]": "49.294484956308",
            "sql[locality][viewport][east]": "16.72785321479357",
        },
        "Kolin": {
            "sql[locality][locality][input]": "Kolín, Česko",
            "sql[locality][locality][city]": "Kolín, Česko",
            "sql[locality][locality][zip_code]": "",
            "sql[locality][locality][types]": "locality",
            "sql[locality][location][lat]": "50.02814",
            "sql[locality][location][lng]": "15.20057",
            "sql[locality][viewport][south]": "49.9s2814",
            "sql[locality][viewport][west]": "15.05057",
            "sql[locality][viewport][north]": "50.12814",
            "sql[locality][viewport][east]": "15.35057",
        }
    
    """

    name = "Eurobydleni"
    logo_url = "https://files.janchaloupka.cz/eurobydleni.png"
    color = 0xFA0F54
    base_url = "https://www.eurobydleni.cz/search-form"

    _base_config = {
            "sql[advert_type_eu][]": 7,
            "sql[advert_subtype_eu][]": "",
            "sql[advert_function_eu][]": 3,
            "sql[advert_price_min]": "",
            "sql[advert_price_max]": "",
            "sql[usable_area_min]": "",
            "sql[usable_area_max]": "",
            "sql[estate_area_min]": "",
            "sql[estate_area_max]": "",
            "sql[poptavka][jmeno]": "",
            "sql[poptavka][prijmeni]": "",
            "sql[poptavka][email]": "",
            "sql[poptavka][telefon]": ""
        }
    
    def __init__(self, config):
        super().__init__(config)

    cookies = {"listing-sort": "sort-added"}
    
    """
    disposition_mapping = {
        Disposition.FLAT_1: 15,
        Disposition.FLAT_1KK: 16,
        Disposition.FLAT_2: 17,
        Disposition.FLAT_2KK: 18,
        Disposition.FLAT_3: 19,
        Disposition.FLAT_3KK: 20,
        Disposition.FLAT_4: 21,
        Disposition.FLAT_4KK: 22,
        Disposition.FLAT_5_UP: (202, 256), # (5+1, 5kk)
        Disposition.FLAT_OTHERS: (14, 857), # (Garsonka, Apartman)
    }
    """


    def build_response(self) -> requests.Response:

        logging.debug("EuroBydlení request: %s", json.dumps(self._config))

        response = requests.post(self.base_url, headers=self.headers, cookies=self.cookies, data=self._config)
        response.encoding = "utf-8"
        return response
    
    def _find_content(self, metas, itemproptype) -> str:
        return " ".join([info.attrs["content"] for info in metas if info.attrs["itemprop"]==itemproptype])

    def get_latest_offers(self) -> list[RentalOffer]:
        response = self.build_response()
        soup = BeautifulSoup(response.text, 'html.parser')

        items: list[RentalOffer] = []

        offers = soup.find(id="properties-box")
        for item in offers.find_all("li", {"class": "list-items__item"}):

            image_container = item.find("ul", {"class": "list-items__item__image__wrap"})
            content = item.find("div", {"class": "list-items__content__1"})
            title = content.find("h2", {"class": "list-items__item__title"})
            details = content.find_all("li")

            metas = item.find_all("meta")
            items.append(
                RentalOffer(
                #scraper = self,
                src=self.name,
                raw=deepcopy(item),
                link = urljoin(self.base_url, title.find("a").get('href')),
                title = title.get_text().strip(),
                location = details[1].get_text().strip(),  #             self._find_content(metas, "addressLocality")+" "+self._find_content(metas, "streeetAddress")
                price = int(re.sub(r"[^\d]", "", details[0].get_text()) or self._find_content(metas, "price")),
                image_url = "https:" + image_container.find("img").get("src"),  #self._find_content(metas, "image")            
                description=self._find_content(metas, "description"),
                charges=None,
                offer_type=None,
                estate_type=None,
            ))
                

        return items