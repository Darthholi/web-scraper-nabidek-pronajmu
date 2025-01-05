from copy import deepcopy
import logging
import re

import requests
import json
from unidecode import unidecode
from bs4 import BeautifulSoup

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

        details = {}
        for item in soup.select("#rc-advertise-result .media.advertise.item"):
            image = item.find("div", "pull-left image")
            body = item.find("div", "media-body")

            link = "https://www.realcity.cz" + body.find("div", "title").a.get("href")

            parsed_headings = {}

            detail_res = requests.get(link)

            if detail_res.status_code == 200:
                sdetail = BeautifulSoup(detail_res.content, 'html.parser')
                """
                !DOCTYPE html>

                <html>
                <head>
                <script type="text/javascript">
                    var pp_gemius_use_cmp = true;
                </script>
                <script type="text/javascript">
                    <!--//--><![CDATA[//><!--
                    var pp_gemius_identifier = 'ndAwrX7ry9Ye5nZFCsOng8dRHbDktHuqdw7fFRi.xNX.I7';
                    // lines below shouldn't be edited
                    function gemius_pending(i) { window[i] = window[i] || function() { var x = window[i+'_pdata'] = window[i+'_pdata'] || []; x[x.length]=arguments;};};
                    gemius_pending('gemius_hit'); gemius_pending('gemius_event'); gemius_pending('pp_gemius_hit'); gemius_pending('pp_gemius_event');
                    (function(d,t) { try { var gt=d.createElement(t),s=d.getElementsByTagName(t)[0],l='http'+((location.protocol=='https:')?'s':''); gt.setAttribute('async','async');
                    gt.setAttribute('defer','defer'); gt.src=l+'://spir.hit.gemius.pl/xgemius.js'; s.parentNode.insertBefore(gt,s);} catch (e) {}})(document,'script');
                    //--><!]]>
                    </script>
                <script data-purposes="publishers-UPqtcgaE" type="didomi/javascript">
                    var google_tag_params = {
                        listing_id: "advertise-4311882", 
                        listing_pagetype: "offerdetail", 
                        listing_totalvalue: 13000
                    };
                </script>
                <script data-purposes="publishers-UPqtcgaE" type="didomi/javascript">
                /* <![CDATA[ */
                var google_conversion_id = 1035713307;
                var google_custom_params = window.google_tag_params;
                var google_remarketing_only = true;
                /* ]]> */
                </script>
                <script data-purposes="publishers-UPqtcgaE" src="//www.googleadservices.com/pagead/conversion.js" type="didomi/javascript"></script>
                <noscript>
                <div style="display:inline;">
                <img alt="" height="1" src="//googleads.g.doubleclick.net/pagead/viewthroughconversion/1035713307/?value=0&amp;guid=ON&amp;script=0" style="border-style:none;" width="1"/>
                </div>
                </noscript>
                <script data-purposes="publishers-UPqtcgaE" type="didomi/javascript">
                /* <![CDATA[ */
                var seznam_retargeting_id = 13792;
                /* ]]> */
                </script>
                <script data-purposes="publishers-UPqtcgaE" src="//c.imedia.cz/js/retargeting.js" type="didomi/javascript"></script> <script>
                        dataLayer = [];
                        (function() {
                            var args = {
                                'serverAdresa' : 'www.realcity.cz',
                                'group': 'classifieds',
                                'device' : 'responsive',
                                'pageLanguage' : "cs",
                                'url' : 'https://www.realcity.cz/nemovitost/pronajem-bytu-2-kk-kolin-4311882',
                                'version' : "live",
                                'attributes' : {"safety":0,"publishedDateTime":"2024-12-21T17:15:24+0100","keywords":null,"category":"byt",
                                "subCategory_1":"pronajem","subCategory_2":null,"subCategory_3":null,"country":"cz","kraj":"stredocesky","okres":"kolin",
                                "mesto":"kolin","seller_id":194502,
                                "disposition":"2-kk","ownership":"osobni","equipment":"castecne-zarizeno","construction":"panelova",
                                "price_czk":"13 000 Kč \/měs.","price_eur":"520 EUR \/měs.",
                                "usable_area":43,"short_title":"Pronájem bytu 2+kk",
                                "short_locality":"Kolín","short_description":"osobní vlastnictví, panelová konstrukce, dobrý stav,
                                  8. patro, umístění v centru, částečně zařízeno, energetická třída C (83-120 kWh\/m²\/rok)"},

                                'dmpData' : Object.assign({"device":"desktop","pageLanguage":"cs","site":"www.realcity.cz",
                                "publishedDateTime":"2024-12-21T17:15:24+0100","category":"byt","subCategory_1":"pronajem",
                                "country":"cz","kraj":"stredocesky","okres":"kolin","mesto":"kolin","seller_id":194502,"disposition":"2-kk",
                                "ownership":"osobni","equipment":"castecne-zarizeno","construction":"panelova","price_czk":"13 000 Kč \/měs.",
                                "price_eur":"520 EUR \/měs.","usable_area":43,"short_title":"Pronájem bytu 2+kk","short_locality":"Kolín",
                                "short_description":"osobní vlastnictví, panelová konstrukce, dobrý stav, 8. patro, umístění v centru, částečně zařízeno, energetická třída C (83-120 kWh\/m²\/rok)",
                                "template":"inzerat","serverAdresa":"www.realcity.cz","pageType":"ad","url":"https:\/\/www.realcity.cz\/nemovitost\/pronajem-bytu-2-kk-kolin-4311882","categories":["byt"],"categories-recs":["byt"],
                                "typ_inzeratu":"pronajem","adType":"rent","adType-recs":"pronájem","offer":"available","adStatus":"available",
                                "disposition-recs":"2+kk","equipment-recs":"částečně zařízeno","region":"stredocesky","region-recs":"středočeský",
                                "city":"kolin","city-recs":"Kolín","district":"kolin","district-recs":"kolín","priceCzk-recs":"13 000 Kč \/měs.",
                                "priceEur-recs":"520 EUR \/měs.","priceRealEstateRentalCzk":"10000-14999","sellerId":194502,
                                "shortDescription-recs":"osobní vlastnictví, panelová konstrukce, dobrý stav, 8. patro, umístění v centru, částečně zařízeno, 
                                energetická třída C (83-120 kWh\/m²\/rok)","shortTitle-recs":"Pronájem bytu 2+kk","usableArea-recs":"43 m²"},
                                  { 'device' : window.matchMedia('screen and (max-width: 767px)').matches ? "mobile" : "desktop"})
                            };
                            var data = Object.assign(args, { template : "inzerat", articleID : 4311882, publishedDateTime : "2024-12-21T17:15:24+0100", modifiedDateTime : "2024-12-28T16:45:03+0100" } || {});
                            dataLayer.push(data);
                        })();
                        
                        dataLayer.push({
                            session : "3edc995e579e1c55711f01646bb4c160"
                        });
                        dataLayer.push({
                            page : "V8:Advertise",
                            view : "detail"
                        });		


                        meta content="2024-12-21T17:15:24+0100" property="article:published_time"/>
                    <meta content="2024-12-28T16:45:03+0100" property="article:modified_time"/>
                """

                detailsscript = sdetail.find("script", {"type": None, "src": None})
                args = detailsscript.get_text().split("var args = {")[1].split("},")[0]

                details = json.loads("{"+args.replace("'","\"").replace("\t","").replace("\n","")+"} }")

                for li in sdetail.find_all('li', {"class": "list-group-item"}):
                    heading = li.find("span", {"class": "list-group-item-label"})
                    value = li.find("span", {"class": "list-group-item-value"})
                    if heading and value:
                        parsed_headings[unidecode(heading.get_text(strip=True).lower())] = value.get_text(strip=True)


            # "informace v RK" - ask being 0
            price = re.sub(r'\D+', '', body.find("div", "price").get_text().strip() or details["attributes"]["price_czk"])
            if not price:
                assert "informace v RK" in [body.find("div", "price").get_text().strip(), details["attributes"]["price_czk"]]
                price = 0

            # TODO this is one of the sites that do not provide more information
            items.append(
                RentalOffer(
                #scraper=self,
                src=self.name,
                raw=deepcopy(item),
                link=link,
                title=body.find("div", "title").a.get_text() or details["attributes"]["short_title"],
                location=body.find("div", "address").get_text().strip() or "Chybí adresa",
                price=price,
                image_url="https:" + image.img.get("src"),
                description=body.find("div", "description").get_text().strip() or details["attributes"]["short_description"],
                published=details["attributes"]["publishedDateTime"],
                disposition=details["attributes"].get("disposition", None),
                charges=None,
                offer_type=details["attributes"]["subCategory_1"],
                estate_type=details["attributes"]["category"],
                area=details["attributes"]["usable_area"],
                energy_eff=parsed_headings.get("energeticka trida", None),
                # Warn - "zastavena plocha" can mean the whole house not just the flat...
            ))
            

        return items
