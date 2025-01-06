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
from tqdm import tqdm


class ScraperIdnesReality(ScrapperBase):

    name = "iDNESReality"
    logo_url = "https://sta-reality2.1gr.cz/ui/image/favicons/favicon-32x32.png"
    color = 0x1D80D7
    base_url = "https://reality.idnes.cz/s/"

    _base_config = {"url": base_url}


    """
    disposition_mapping = {
        Disposition.FLAT_1KK: "s-qc%5BsubtypeFlat%5D%5B%5D=1k",
        Disposition.FLAT_1: "s-qc%5BsubtypeFlat%5D%5B%5D=11",
        Disposition.FLAT_2KK: "s-qc%5BsubtypeFlat%5D%5B%5D=2k",
        Disposition.FLAT_2: "s-qc%5BsubtypeFlat%5D%5B%5D=21",
        Disposition.FLAT_3KK: "s-qc%5BsubtypeFlat%5D%5B%5D=3k",
        Disposition.FLAT_3: "s-qc%5BsubtypeFlat%5D%5B%5D=31",
        Disposition.FLAT_4KK: "s-qc%5BsubtypeFlat%5D%5B%5D=4k",
        Disposition.FLAT_4: "s-qc%5BsubtypeFlat%5D%5B%5D=41",
        Disposition.FLAT_5_UP: (
            "s-qc%5BsubtypeFlat%5D%5B%5D=5k",
            "s-qc%5BsubtypeFlat%5D%5B%5D=51",
            "s-qc%5BsubtypeFlat%5D%5B%5D=6k", # 6 a víc
        ),
        Disposition.FLAT_OTHERS: "s-qc%5BsubtypeFlat%5D%5B%5D=atypical", # atyp
    }
    """
    def __init__(self, config):
        super().__init__(config)

    def build_response(self) -> requests.Response:
        url = self._config["url"]

        logging.debug("iDNES reality request: %s", url)
        
        results = []
        for page in range(0, 100):
            result = requests.get(url+f"?page={page}", headers=self.headers)
            if result.url.endswith(f"page={page-1}"): # if the page is the same as the previous one, we are out of range
                break
            results.append(result)
        return results

    def find_get_content(self, soup, *args, **kwargs):
        search = soup.find(*args, **kwargs)
        if search:
            return search.get('content')
        return None
    
    def find_get_text(self, soup, *args, **kwargs):
        search = soup.find(*args, **kwargs)
        if search:
            return search.get_text(strip=True)
        return None
    
    def find_get_textorcontent(self, soup, *args, **kwargs):
        search = soup.find(*args, **kwargs)
        if search:
            txt = search.get_text(strip=True)
            if not txt:
                txt = search.get('content')
            return txt
        return None

    def get_latest_offers(self) -> list[RentalOffer]:
        responses = self.build_response()
        # TODO Idnes does not provide more information, it would need to read the link for more details

        items: list[RentalOffer] = []
        for response in tqdm(responses, desc="iDNESReality", leave=False):
            soup = BeautifulSoup(response.text, 'html.parser')

            offers = soup.find(id="snippet-s-result-articles")
            for item in offers.find_all("div", {"class": "c-products__item"}):

                if "c-products__item-advertisment" in item.get("class"):
                    continue


                link = item.find("a", {"class": "c-products__link"}).get('href')
                

                area_land = None
                area = None
                yearly_energy = None
                energy_eff = None
                typedisp = None
                sdetail = None

                if self.details_allowed:
                    detail = requests.get(link)
                    if detail.status_code == 200:
                        sdetail = BeautifulSoup(detail.content, 'html.parser')

                        #title=sdetail.find('h1', {'class': 'b-detail__title'}).get_text(strip=True) if soup.find('h1', {'class': 'b-detail__title'}) else 'No title found',  # Extract title
                        #location=sdetail.find('span', {'class': 'b-detail__info-item'}).get_text(strip=True) if soup.find('span', {'class': 'b-detail__info-item'}) else 'No location found',  # Extract location
                        #price=int(sdetail.find('strong', {'class': 'b-detail__price-value'}).get_text(strip=True).replace(' ', '').replace('Kč', '')) if soup.find('strong', {'class': 'b-detail__price-value'}) else 0,  # Extract price
                        #image_url=sdetail.find('img', {'class': 'main-image'})['src'] if soup.find('img', {'class': 'main-image'}) else '',  # Extract image URL
                        #description=sdetail.find('div', {'class': 'b-detail__description'}).get_text(strip=True) if soup.find('div', {'class': 'b-detail__description'}) else 'No description found',  # Extract description
                    

                        """
                        <meta content="Byt/2+1" name="cXenseParse:qiw-reaCategory"/>
                        <meta content="Kolín" name="cXenseParse:qiw-reaCity"/>
                        <meta content="Kolín" name="cXenseParse:qiw-reaDistrict"/>
                        <meta content="Středočeský kraj" name="cXenseParse:qiw-reaRegion"/>
                        <meta content="CZ" name="cXenseParse:qiw-reaState"/>
                        <meta content="4" name="cXenseParse:qiw-reaPrice"/>
                        <meta content="Nemovitost" name="cXenseParse:qiw-reaType"/>
                        <meta content="Prodej" name="cXenseParse:qiw-reaVariant"/>
                        <meta content="article" name="cXenseParse:pageclass"/>

                        <div class="b-definition-columns mb-0">
                        <dt>
                        PENB
                        </dt>
                        <dd>
                        E (vyhl. č. 264/2020 Sb.)
                        </dd>

                        <dt>Plocha pozemku</dt>
                        <dd>1 m<sup>2</sup></dd>
                        <dt>Užitná plocha</dt>
                        <dd>132 m<sup>2</sup></dd>
                        <dt>Roční spotřeba energie</dt>
                        <dd>97 kWh</dd>
                        """
                        for dt in sdetail.find_all('dt'):
                            if dt.get_text(strip=True) == 'PENB':
                                energy_eff = dt.find_next_sibling('dd').get_text(strip=True)
                                break

                        typedisp = self.find_get_content(sdetail, 'meta', {'name': 'cXenseParse:qiw-reaCategory'})

                        areafind = sdetail.find('div', {'class': 'params-item area'})
                        
                        if areafind:
                            area = areafind.find('strong').get_text(strip=True)
                        else:
                            for dt in sdetail.find_all('dt'):
                                if dt.get_text(strip=True) == 'Užitná plocha':
                                    area = dt.find_next_sibling('dd').get_text(strip=True)
                                    break

                            for dt in sdetail.find_all('dt'):
                                if dt.get_text(strip=True) == 'Plocha pozemku':
                                    area_land = dt.find_next_sibling('dd').get_text(strip=True)
                                    break
                            
                        for dt in sdetail.find_all('dt'):
                            if dt.get_text(strip=True) == 'Roční spotřeba energie':
                                yearly_energy = dt.find_next_sibling('dd').get_text(strip=True)
                                break

                items.append(
                    RentalOffer(
                    src=self.name,
                    raw=deepcopy(item),
                    link = link,
                    title = ' '.join(item.find("h2", {"class": "c-products__title"}).get_text().strip().splitlines()),
                    location = item.find("p", {"class": "c-products__info"}).get_text().strip(),
                    price = int(re.sub(r"[^\d]", "", item.find("p", {"class": "c-products__price"}).get_text()) or "0"),
                    image_url = item.find("img").get("data-src"),
                    area=area,
                    area_land=area_land,
                    description=self.find_get_content(sdetail, 'div', {'class': 'b-desc pt-10 mt-10'}) if sdetail else None,
                    charges=None,
                    offer_type=self.find_get_textorcontent(sdetail, 'meta', {'name': 'cXenseParse:qiw-reaVariant'}) if sdetail else None,
                    estate_type=typedisp.split('/')[0] if typedisp else None,
                    disposition=typedisp.split('/')[1] if typedisp else None,
                    energy_eff=energy_eff,
                    yearly_energy=yearly_energy,
                ))

        return items
