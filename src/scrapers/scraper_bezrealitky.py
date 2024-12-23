""" Scraper for BezRealitky.cz
author: Mark Barzali
"""

import json
from abc import ABC as abstract
from typing import ClassVar

from disposition import Disposition
from scrapers.scraper_base import ScraperBase
from scrapers.rental_offer import RentalOffer
import requests

class ScraperBezrealitky(ScraperBase):
    # https://github.com/kanospet/bezrealitky/blob/main/main.pys
    # https://api.bezrealitky.cz/graphql/?query={__schema%20{queryType%20{name%20fields%20{name}}mutationType%20{name%20fields%20{name}}}}
    # https://api.bezrealitky.cz/graphql/?query={__type%20(name%3A%20%22Query%22)%20{fields%20{name%20args%20{name%20type%20{name}}}}}
    # try also by: https://api.bezrealitky.cz/graphql/?query={listAdverts%20(regionOsmIds%3A%20[%22R441253%22]){list{id,uri}}}

    name = "BezRealitky"
    logo_url = "https://www.bezrealitky.cz/manifest-icon-192.maskable.png"
    color = 0x00CC00
    base_url = "https://www.bezrealitky.cz"
    API: ClassVar[str] = "https://api.bezrealitky.cz/"

    # offerType=PRODEJ&estateType=DUM&regionOsmIds=R441315&osm_value=Kolín%2C+Střední+Čechy%2C+Česko&location=exact&currency=CZK

    _base_config = {
        "operationName": "AdvertList",
        "variables": {
            "limit": 400,
            "offset": 0,
            "order": "TIMEORDER_DESC",
            "locale": "CS",
            "offerType": [],
            "estateType": [],
            "disposition": [],
            "regionOsmIds": [],
        },
        "query": """query AdvertList($locale: Locale!, $estateType: [EstateType],
         $offerType: [OfferType], $disposition: [Disposition], $region: ID, 
         $regionOsmIds: [ID], $regionOsmId: ID,
         $locationPoint: GPSPointInput, $locationRadius: Int,
         $limit: Int = 15, $offset: Int = 0,
         $order: ResultOrder = TIMEORDER_DESC, $petFriendly: Boolean, $balconyFrom: Float,
         $balconyTo: Float, $loggiaFrom: Float, $loggiaTo: Float,
         $terraceFrom: Float, $terraceTo: Float, $cellarFrom: Float, $cellarTo: Float, $parking: Boolean,
         $garage: Boolean, $newBuilding: Boolean, $lift: Boolean, $ownership: [Ownership],
         $construction: [Construction], $equipped: [Equipped], $priceFrom: Int, $priceTo: Int, $surfaceFrom: Int,
         $surfaceTo: Int, $advertId: [ID], $roommate: Boolean, $includeImports: Boolean, $boundaryPoints: [GPSPointInput],
         $discountedOnly: Boolean, $barrierFree: Boolean, $polygonBuffer: Int, $availableFrom: DateTime) 
         {\n  
         listAdverts(\n    offerType: $offerType\n    estateType: $estateType\n    disposition: $disposition\n
            limit: $limit\n    regionId: $region\n    regionOsmIds: $regionOsmIds\n     regionOsmId: $regionOsmId\n
            locationPoint: $locationPoint\n     locationRadius: $locationRadius\n        offset: $offset\n
            order: $order\n    petFriendly: $petFriendly\n    balconySurfaceFrom: $balconyFrom\n
            balconySurfaceTo: $balconyTo\n    loggiaSurfaceFrom: $loggiaFrom\n
            loggiaSurfaceTo: $loggiaTo\n    terraceSurfaceFrom: $terraceFrom\n
            terraceSurfaceTo: $terraceTo\n    cellarSurfaceFrom: $cellarFrom\n
            cellarSurfaceTo: $cellarTo\n    parking: $parking\n    garage: $garage\n
            newBuilding: $newBuilding\n    lift: $lift\n    ownership: $ownership\n
            construction: $construction\n    equipped: $equipped\n    priceFrom: $priceFrom\n
            priceTo: $priceTo\n    surfaceFrom: $surfaceFrom\n    surfaceTo: $surfaceTo\n
            ids: $advertId\n    roommate: $roommate\n    includeImports: $includeImports\n
            boundaryPoints: $boundaryPoints\n    discountedOnly: $discountedOnly\n
            polygonBuffer: $polygonBuffer\n    barrierFree: $barrierFree\n    availableFrom: $availableFrom\n  )
            {\n    
            list {\n      id\n      uri\n      estateType\n      offerType\n      disposition\n
                        imageAltText(locale: $locale)\n      mainImage {\n        id\n
            url(filter: RECORD_THUMB)\n        __typename\n      }\n
            address(locale: $locale)\n      surface\n      surfaceLand\n      tags(locale: $locale)\n      price\n
            charges\n      currency\n      petFriendly\n      reserved\n      highlighted\n      roommate\n
            project {\n        id\n        __typename\n      }\n      gps {\n        lat\n        lng\n
            __typename\n      }\n      mortgageData(locale: $locale) {\n        rateLow\n        rateHigh\n
            loan\n        years\n        __typename\n      }\n      originalPrice\n      isDiscounted\n
            nemoreport {\n        id\n        status\n        timeCreated\n        __typename\n      }\n
            isNew\n      videos {\n        id\n        previewUrl\n        status\n        __typename\n      }\n
            links {\n        id\n        url\n        type\n        status\n        __typename\n      }\n
            __typename\n    }\n    totalCount\n    __typename\n  }\n
            actionList: listAdverts(\n    offerType: $offerType\n    estateType: $estateType\n
            disposition: $disposition\n    regionId: $region\n    regionOsmIds: $regionOsmIds\n     regionOsmId: $regionOsmId\n
            locationPoint: $locationPoint\n     locationRadius: $locationRadius\n             
            offset: $offset\n    order: $order\n    petFriendly: $petFriendly\n    balconySurfaceFrom: $balconyFrom\n
            balconySurfaceTo: $balconyTo\n    loggiaSurfaceFrom: $loggiaFrom\n    loggiaSurfaceTo: $loggiaTo\n
            terraceSurfaceFrom: $terraceFrom\n    terraceSurfaceTo: $terraceTo\n    cellarSurfaceFrom: $cellarFrom\n
            cellarSurfaceTo: $cellarTo\n    parking: $parking\n    garage: $garage\n    newBuilding: $newBuilding\n
            lift: $lift\n    ownership: $ownership\n    construction: $construction\n    equipped: $equipped\n    priceFrom: $priceFrom\n
            priceTo: $priceTo\n    surfaceFrom: $surfaceFrom\n    surfaceTo: $surfaceTo\n    ids: $advertId\n    roommate: $roommate\n
            includeImports: $includeImports\n    boundaryPoints: $boundaryPoints\n    discountedOnly: true\n    limit: 3\n
            availableFrom: $availableFrom\n  ) {\n    list {\n      id\n      uri\n      estateType\n      offerType\n
            disposition\n      imageAltText(locale: $locale)\n      mainImage {\n        id\n        url(filter: RECORD_THUMB)\n
            __typename\n      }\n      address(locale: $locale)\n      surface\n      surfaceLand\n
            tags(locale: $locale)\n      price\n      charges\n      currency\n      petFriendly\n      reserved\n
            highlighted\n      roommate\n      project {\n        id\n        __typename\n      }\n
            gps {\n        lat\n        lng\n        __typename\n      }\n      mortgageData(locale: $locale) {\n
            rateLow\n        rateHigh\n        loan\n        years\n        __typename\n      }\n      originalPrice\n
            isDiscounted\n      nemoreport {\n        id\n        status\n        timeCreated\n        __typename\n      }\n
            isNew\n      videos {\n        id\n        previewUrl\n        status\n        __typename\n      }\n
            links {\n        id\n        url\n        type\n        status\n        __typename\n      }\n
            __typename\n    }\n    totalCount\n    __typename\n  }\n}\n"""
    }

    class Routes(abstract):
        GRAPHQL: ClassVar[str] = "graphql/"
        OFFERS: ClassVar[str] = "nemovitosti-byty-domy/"


    def __init__(self, config):
        super().__init__(config)

    @staticmethod
    def _create_link_to_offer(item: dict) -> str:
        return f"{ScraperBezrealitky.base_url}/{ScraperBezrealitky.Routes.OFFERS}{item}"

    def build_response(self) -> requests.Response:
        return requests.post(
            url=f"{ScraperBezrealitky.API}{ScraperBezrealitky.Routes.GRAPHQL}",
            json=self._config
        )

    def get_latest_offers(self) -> list[RentalOffer]:
        response = self.build_response().json()

        return [  # type: list[RentalOffer]
            RentalOffer(
                scraper=self,
                link=self._create_link_to_offer(item["uri"]),
                title=item["imageAltText"],
                location=item["address"],
                price=f"{item['price']} / {item['charges']}",
                image_url=item["mainImage"]["url"] if item["mainImage"] else "",
            )
            for item in response["data"]["listAdverts"]["list"]
        ]


"""
class ScraperBezrealitky(ScraperBase):

    name = "BezRealitky"
    logo_url = "https://www.bezrealitky.cz/manifest-icon-192.maskable.png"
    color = 0x00CC00
    base_url = "https://www.bezrealitky.cz"
    file: ClassVar[str] = "./graphql/bezrealitky.json"

    API: ClassVar[str] = "https://api.bezrealitky.cz/"
    OFFER_TYPE: ClassVar[str] = "PRONAJEM"
    ESTATE_TYPE: ClassVar[str] = "BYT"
    # BRNO: ClassVar[str] = "R438171"
    KOLIN: ClassVar[str] = "R441315"

    class Routes(abstract):
        GRAPHQL: ClassVar[str] = "graphql/"
        OFFERS: ClassVar[str] = "nemovitosti-byty-domy/"

    disposition_mapping = {
        Disposition.FLAT_1KK: "DISP_1_KK",
        Disposition.FLAT_1: "DISP_1_1",
        Disposition.FLAT_2KK: "DISP_2_KK",
        Disposition.FLAT_2: "DISP_2_1",
        Disposition.FLAT_3KK: "DISP_3_KK",
        Disposition.FLAT_3: "DISP_3_1",
        Disposition.FLAT_4KK: "DISP_4_KK",
        Disposition.FLAT_4: "DISP_4_1",
        Disposition.FLAT_5_UP: None,
        Disposition.FLAT_OTHERS: None,
    }

    def __init__(self, dispositions: Disposition):
        super().__init__(dispositions)
        self._read_config()
        self._patch_config()

    def _read_config(self) -> None:
        with open(ScraperBezrealitky.file, "r") as file:
            self._config = json.load(file)

    def _patch_config(self):
        match = {
            "estateType": self.ESTATE_TYPE,
            "offerType": self.OFFER_TYPE,
            "disposition": self.get_dispositions_data(),
            "regionOsmIds": [self.BRNO],
        }
        self._config["variables"].update(match)

    @staticmethod
    def _create_link_to_offer(item: dict) -> str:
        return f"{ScraperBezrealitky.base_url}/{ScraperBezrealitky.Routes.OFFERS}{item}"

    def build_response(self) -> requests.Response:
        return requests.post(
            url=f"{ScraperBezrealitky.API}{ScraperBezrealitky.Routes.GRAPHQL}",
            json=self._config
        )

    def get_latest_offers(self) -> list[RentalOffer]:
        response = self.build_response().json()

        return [  # type: list[RentalOffer]
            RentalOffer(
                scraper=self,
                link=self._create_link_to_offer(item["uri"]),
                title=item["imageAltText"],
                location=item["address"],
                price=f"{item['price']} / {item['charges']}",
                image_url=item["mainImage"]["url"] if item["mainImage"] else "",
            )
            for item in response["data"]["listAdverts"]["list"]
        ]
"""
