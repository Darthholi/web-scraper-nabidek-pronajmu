from copy import deepcopy
import logging
import re

import requests
from bs4 import BeautifulSoup

from legacy.disposition import Disposition
from scrappers.rental_offer import RentalOffer
from scrappers.base import ScrapperBase
from scrappers.rental_offer import RentalOffer
import requests
from bs4 import BeautifulSoup


class ScraperRealcity(ScrapperBase):

    name = "REALCITY"
    logo_url = "https://files.janchaloupka.cz/realcity.png"
    color = 0xB60D1C
    base_url = "https://www.realcity.cz/nemovitosti"
    _base_config = {"url": base_url}


    """
    disposition_mapping = {
        Disposition.FLAT_1KK: "%221%2Bkk%22",
        Disposition.FLAT_1: "%221%2B1%22",
        Disposition.FLAT_2KK: "%222%2Bkk%22",
        Disposition.FLAT_2: "%222%2B1%22",
        Disposition.FLAT_3KK: "%223%2Bkk%22",
        Disposition.FLAT_3: "%223%2B1%22",
        Disposition.FLAT_4KK: "%224%2Bkk%22",
        Disposition.FLAT_4: ("%224%2B1%22", "%224%2B2%22"), # 4+1, 4+2
        Disposition.FLAT_5_UP: ("%225%2Bkk%22", "%225%2B1%22", "%225%2B2%22", "%226%2Bkk%22", "%226%2B1%22", "%22disp_more%22"), # 5kk, 5+1, 5+2, 6kk, 6+1, ++
        Disposition.FLAT_OTHERS: ("%22atyp%22", "%22disp_nospec%22"), # atyp, unknown
    }
    """
    def __init__(self, config):
        super().__init__(config)

    def build_response(self) -> requests.Response:
        #url = "https://www.realcity.cz/pronajem-bytu/brno-mesto-68/?sp=%7B%22locality%22%3A%5B68%5D%2C%22transactionTypes%22%3A%5B%22rent%22%5D%2C%22propertyTypes%22%3A%5B%7B%22propertyType%22%3A%22flat%22%2C%22options%22%3A%7B%22disposition%22%3A%5B"
        #url += "%2C".join(self.get_dispositions_data())
        #url += "%5D%7D%7D%5D%7D"
        url = self._config["url"]

        logging.debug("REALCITY request: %s", url)

        return requests.get(url, headers=self.headers)

    def get_latest_offers(self) -> list[RentalOffer]:
        response = self.build_response()
        soup = BeautifulSoup(response.text, 'html.parser')

        items: list[RentalOffer] = []

        for item in soup.select("#rc-advertise-result .media.advertise.item"):
            image = item.find("div", "pull-left image")
            body = item.find("div", "media-body")
            # TODO this is one of the sites that do not provide more information
            items.append(
                RentalOffer(
                #scraper=self,
                src=self.name,
                raw=deepcopy(item),
                link="https://www.realcity.cz" + body.find("div", "title").a.get("href"),
                title=body.find("div", "title").a.get_text() or "Chybí titulek",
                location=body.find("div", "address").get_text().strip() or "Chybí adresa",
                price=re.sub(r'\D+', '', body.find("div", "price").get_text() or "0"),
                image_url="https:" + image.img.get("src"),
                description=body.find("div", "description").get_text().strip() or None,
                charges=None,
                offer_type=None,
                estate_type=None,
            ))
            

        return items