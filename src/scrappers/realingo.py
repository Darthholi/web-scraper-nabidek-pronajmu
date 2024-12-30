from copy import deepcopy
import json
import logging
from urllib.parse import urljoin

from bs4 import BeautifulSoup
import requests
from tqdm import tqdm

from legacy.disposition import Disposition
from scrappers.rental_offer import RentalOffer
from scrappers.base import ScrapperBase
from scrappers.rental_offer import RentalOffer
import requests


class ScraperRealingo(ScrapperBase):
    """
    possibly all keys:

    Here are the keys extracted from the provided JSON:

- urqlClient
- store
  - router
  - filter
  - offer
    - list
      - data
      - total
      - queriedLimit
      - locationDetail
      - addressGeometry
    - details
      - 24194801
        - offer
          - id
          - preview
          - offer
            - id
            - url
            - purpose
            - property
            - visited
            - liked
            - reserved
            - createdAt
            - category
            - price
              - total
              - canonical
              - currency
              - type
              - squareMeter
              - squareMeterCanonical
              - vat
              - energyBillingMethod
              - energyCharges
              - energyChargesPerPerson
              - charges
              - chargesPerPerson
              - note
            - area
              - main
              - plot
              - floor
              - built
              - garden
              - office
              - production
              - nonresidential
              - shop
              - store
              - basin
              - cellar
              - balcony
              - terrace
              - loggia
            - photos
              - main
              - list
            - location
              - address
              - addressUrl
              - locationPrecision
              - latitude
              - longitude
            - deleted
            - adId
            - updatedAt
            - deletedAt
          - detail
            - id
            - externalUrl
            - description
            - buildingType
            - buildingStatus
            - buildingPosition
            - houseType
            - ownership
            - furniture
            - floor
            - floorUnderground
            - floorTotal
            - yearBuild
            - yearReconstructed
            - parking
            - parkingPlaces
            - garages
            - energyPerformance
            - energyPerformanceValue
            - energyPerformanceLawRequirement
            - availableFromDate
            - ceilingHeight
            - roomCount
            - flatCount
            - flatClass
            - gully
            - heating
            - telecommunication
            - electricity
            - waterSupply
            - gas
            - balcony
            - loggia
            - terrace
            - lift
            - cellar
            - isBarrierFree
            - isAuction
            - garret
            - basin
            - floodRisk
            - floodActiveZone
            - contact
              - type
              - person
              - company
          - mortgage
          - location
            - id
            - url
            - name
            - breadcrumbs
            - viewGeometry
              - bbox
              - type
              - coordinates


price {
                    total
                    canonical
                    currency
                    type
                    squareMeter
                    squareMeterCanonical
                    vat
                    energyBillingMethod
                    energyCharges
                    energyChargesPerPerson
                    charges
                    chargesPerPerson
                    note
                }
                area {
                    main
                    plot
                    floor
                    built
                    garden
                    office
                    production
                    nonresidential
                    shop
                    store
                    basin
                    cellar
                    balcony
                    terrace
                    loggia
                }
                photos {
                    main
                    list
                }
                location {
                    address
                    addressUrl
                    locationPrecision
                    latitude
                    longitude
                }
                deleted
                adId
                updatedAt
                deletedAt
                detail {
                    id
                    externalUrl
                    description
                    buildingType
                    buildingStatus
                    buildingPosition
                    houseType
                    ownership
                    furniture
                    floor
                    floorUnderground
                    floorTotal
                    yearBuild
                    yearReconstructed
                    parking
                    parkingPlaces
                    garages
                    energyPerformance
                    energyPerformanceValue
                    energyPerformanceLawRequirement
                    availableFromDate
                    ceilingHeight
                    roomCount
                    flatCount
                    flatClass
                    gully
                    heating
                    telecommunication
                    electricity
                    waterSupply
                    gas
                    balcony
                    loggia
                    terrace
                    lift
                    cellar
                    isBarrierFree
                    isAuction
                    garret
                    basin
                    floodRisk
                    floodActiveZone
                    contact {
                        type
                        person
                        company
                    }
                }
                mortgage
                location {
                    id
                    url
                    name
                    breadcrumbs
                    viewGeometry {
                        bbox
                        type
                        coordinates
                    }
                }
    
    """

    name = "realingo"
    logo_url = "https://www.realingo.cz/_next/static/media/images/android-chrome-144x144-cf1233ce.png"
    color = 0x00BC78
    base_url = "https://www.realingo.cz/graphql"

    _base_config = {
        "query": """
            query SearchOffer(
                $purpose: OfferPurpose, 
                $property: PropertyType, 
                $saved: Boolean, 
                $categories: [OfferCategory!],
                $area: RangeInput, 
                $plotArea: RangeInput, 
                $price: RangeInput, 
                $bounds: GpsBoundsInput, 
                $address: String,
                $transportType: TransportType, 
                $toleration: Float, 
                $buildingTypes: [BuildingType!], 
                $buildingStatuses: [BuildingStatus!],
                $buildingPositions: [BuildingPosition!], 
                $houseTypes: [HouseType!], 
                $floor: RangeInput, 
                $ownershipStatuses: [OwnershipStatus!],
                $furnitureStatuses: [FurnitureStatus!], 
                $maxAge: Int, 
                $contactType: ContactType, 
                $geometry: GeoJSONGeometry,
                $sort: OfferSort = NEWEST, 
                $first: Int = 20, 
                $skip: Int = 0
            ) {
                addressGeometry(
                    address: $address
                    geometry: $geometry
                    toleration: $toleration
                    transportType: $transportType
                ) {
                    geometry
                    mask
                }
                searchOffer(
                    filter: {
                        purpose: $purpose, 
                        property: $property, 
                        saved: $saved, 
                        address: $address,
                        transportType: $transportType, 
                        toleration: $toleration, 
                        categories: $categories, 
                        area: $area,
                        plotArea: $plotArea, 
                        price: $price, 
                        bounds: $bounds, 
                        buildingTypes: $buildingTypes,
                        buildingStatuses: $buildingStatuses, 
                        buildingPositions: $buildingPositions,
                        houseTypes: $houseTypes, 
                        floor: $floor, 
                        ownershipStatuses: $ownershipStatuses,
                        furnitureStatuses: $furnitureStatuses, 
                        maxAge: $maxAge, 
                        contactType: $contactType,
                        geometry: $geometry
                    }
                    sort: $sort
                    first: $first
                    skip: $skip
                    save: true
                ) {
                    location {
                        id
                        type
                        url
                        name
                        neighbours {
                            id
                            type
                            url
                            name
                        }
                        breadcrumbs {
                            url
                            name
                        }
                        relatedSearch {
                            ...SearchParametersAttributes
                        }
                        center
                    }
                    items {
                        ...SearchOfferAttributes
                    }
                    total
                }
            }
            fragment FilterAttributes on OfferFilter {
                purpose
                property
                categories
                address
                location {
                    name
                }
                toleration
                transportType
                bounds {
                    northEast {
                        latitude
                        longitude
                    }
                    southWest {
                        latitude
                        longitude
                    }
                }
                saved
                geometry
                area {
                    from
                    to
                }
                plotArea {
                    from
                    to
                }
                price {
                    from
                    to
                }
                buildingTypes
                buildingStatuses
                buildingPositions
                houseTypes
                floor {
                    from
                    to
                }
                ownershipStatuses
                furnitureStatuses
                maxAge
                contactType
            }
            fragment SearchParametersAttributes on SearchParameters {
                filter {
                    ...FilterAttributes
                }
                page
                priceMap
                sort
            }
            fragment SearchOfferAttributes on Offer {
                id
                url
                purpose
                property
                visited
                liked
                reserved
                createdAt
                category
                purpose
                property
                
                price {
                    total
                    canonical
                    currency
                    type
                    squareMeter
                    squareMeterCanonical
                    vat
                    energyBillingMethod
                    energyCharges
                    energyChargesPerPerson
                    charges
                    chargesPerPerson
                    note
                }
                area {
                    main
                    plot
                    floor
                    built
                    garden
                    office
                    production
                    nonresidential
                    shop
                    store
                    basin
                    cellar
                    balcony
                    terrace
                    loggia
                }
                photos {
                    main
                }
                location {
                    address
                    addressUrl
                    locationPrecision
                    latitude
                    longitude
                }
            }
        """,
        "operationName": "SearchOffer",
        "variables": {
            "address": [],
            "saved": False,
            "sort": "NEWEST",
            "first": 300,
            "skip": 0
        }
    }

    """
    disposition_mapping = {
        Disposition.FLAT_1KK: "FLAT1_KK",
        Disposition.FLAT_1: "FLAT11",
        Disposition.FLAT_2KK: "FLAT2_KK",
        Disposition.FLAT_2: "FLAT21",
        Disposition.FLAT_3KK: "FLAT3_KK",
        Disposition.FLAT_3: "FLAT31",
        Disposition.FLAT_4KK: "FLAT4_KK",
        Disposition.FLAT_4: "FLAT41",
        Disposition.FLAT_5_UP: ("FLAT5_KK", "FLAT51", "FLAT6_AND_MORE"),
        Disposition.FLAT_OTHERS: "OTHERS_FLAT",
    }
    """

    def __init__(self, config):
        super().__init__(config)


    def build_response(self) -> requests.Response:
        

        logging.debug("realingo request: %s", json.dumps(self._config))

        return requests.post(self.base_url, headers=self.headers, json=self._config)


    def category_to_string(self, id) -> str:
        return {
            "FLAT1_KK": "Byt 1+kk",
            "FLAT11": "Byt 1+1",
            "FLAT2_KK": "Byt 2+kk",
            "FLAT21": "Byt 2+1",
            "FLAT3_KK": "Byt 3+kk",
            "FLAT31": "Byt 3+1",
            "FLAT4_KK": "Byt 4+kk",
            "FLAT41": "Byt 4+1",
            "FLAT5_KK": "Byt 5+kk",
            "FLAT51": "Byt 5+1",
            "FLAT6_AND_MORE": "Byt 6+kk a v\u011bt\u0161\xed",
            "HOUSE_FAMILY": "Rodinn\xfd dům",
            "HOUSE_APARTMENT": "\u010cin\u017eovn\xed",
            "HOUSE_MANSION": "Vila",
            "LAND_COMMERCIAL": "Komer\u010dn\xed",
            "LAND_HOUSING": "Bydlen\xed",
            "LAND_GARDEN": "Zahrady",
            "LAND_AGRICULTURAL": "Zem\u011bd\u011blsk\xfd",
            "LAND_MEADOW": "Louka",
            "LAND_FOREST": "Les",
            "COMMERCIAL_OFFICE": "Kancel\xe1\u0159",
            "COMMERCIAL_STORAGE": "Sklad",
            "COMMERCIAL_MANUFACTURING": "V\xfdrobn\xed prostor",
            "COMMERCIAL_BUSINESS": "Obchod",
            "COMMERCIAL_ACCOMMODATION": "Ubytov\xe1n\xed",
            "COMMERCIAL_RESTAURANT": "Restaurace",
            "COMMERCIAL_AGRICULTURAL": "Zem\u011bd\u011blsk\xfd objekt",
            "OTHERS_HUT": "Chata",
            "OTHERS_COTTAGE": "Chalupa",
            "OTHERS_GARAGE": "Gar\xe1\u017e",
            "OTHERS_FARMHOUSE": "Zem\u011bd\u011blsk\xe1 usedlost",
            "OTHERS_POND": "Rybn\xedk",
            "OTHERS_FLAT": "Atypick\xfd",
            "OTHERS_OTHERS": "Pam\xe1tka",
            "OTHERS_MONUMENTS": "Ostatn\xed"
        }.get(id, "")


    def get_latest_offers(self) -> list[RentalOffer]:
        response = self.build_response().json()

        items: list[RentalOffer] = []
        if "data" not in response:
            raise ValueError(response['errors'])

        for offer in tqdm(response["data"]["searchOffer"]["items"]):
            # todo does not provide more details, would need to go to the details

            link = urljoin(self.base_url, offer["url"])

            #detail_res = requests.get(link)
            #if detail_res.status_code == 200:
            #    sdetail = BeautifulSoup(detail_res.content, 'html.parser')
                
            
            
            #    """
            #    <script id="__NEXT_DATA__" type="application/json">
            #    {"props":{"pageProps":{"urqlClient":null,"store":{"router":null,"filter":null,"offer":{"list":{"data":[],"total":null,"queriedLimit":null,"locationDetail":null,"addressGeometry":null},"details":{"24194801":{"offer":{"id":"24194801","preview":false,"offer":{"id":"24194801","url":"/pronajem/byt-2+1-kolin-280-02/24194801","purpose":"RENT","property":"FLAT","visited":false,"liked":null,"reserved":false,"createdAt":"2024-12-28T17:35:34.236Z","category":"FLAT21","price":{"total":15000,"canonical":15000,"currency":"CZK","type":"FIXED","squareMeter":null,"squareMeterCanonical":283.01886,"vat":null,"energyBillingMethod":null,"energyCharges":null,"energyChargesPerPerson":null,"charges":null,"chargesPerPerson":null,"note":null},"area":{"main":53,"plot":null,"floor":null,"built":null,"garden":null,"office":null,"production":null,"nonresidential":null,"shop":null,"store":null,"basin":null,"cellar":null,"balcony":null,"terrace":null,"loggia":null},"photos":{"main":"offer/gn5/gn52vwmg3v-1200x900xd8d8d8","list":["offer/hrn/hrnexsafkp-900x1200x484848","offer/a3a/a3abwhpxm8-900x1200x685858","offer/nhe/nhe1pgz4f9-900x1200x786868","offer/8w3/8w32nzucma-900x1200x484848"]},"location":{"address":"Kolín, 280 02","addressUrl":"Kolín_II,Kolín","locationPrecision":"TOWN","latitude":50.037738,"longitude":15.170059},"deleted":false,"adId":null,"updatedAt":"2024-12-28T17:35:34.236Z","deletedAt":null},"detail":{"id":"24194801","externalUrl":"https://reality.bazos.cz/inzerat/195919033/pronajem-bytu-v-koline.php","description":"Pronajmu byt 2+1, 53m² + balkón 9m². Byt je po rekonstrukci. Nájem 15.000,- + služby cca 5000,-. Byt je v Kolíně v ulici Funkeho, klidná část sídliště s možností parkování. Nachází se ve 2. patře ze 3. Bez výtahu. Byt je okamžitě k nastěhování.","buildingType":null,"buildingStatus":null,"buildingPosition":null,"houseType":null,"ownership":null,"furniture":null,"floor":null,"floorUnderground":null,"floorTotal":null,"yearBuild":null,"yearReconstructed":null,"parking":null,"parkingPlaces":null,"garages":null,"energyPerformance":null,"energyPerformanceValue":null,"energyPerformanceLawRequirement":null,"availableFromDate":null,"ceilingHeight":null,"roomCount":null,"flatCount":null,"flatClass":null,"gully":null,"heating":null,"telecommunication":null,"electricity":null,"waterSupply":null,"gas":null,"balcony":null,"loggia":null,"terrace":null,"lift":null,"cellar":null,"isBarrierFree":null,"isAuction":null,"garret":null,"basin":null,"floodRisk":null,"floodActiveZone":null,"contact":{"type":"EXTERNAL","person":null,"company":null}},"mortgage":null,"location":{"id":"94799","url":"Kolín_II,Kolín","name":"Kolín II, Kolín","breadcrumbs":[{"url":"Okres_Kolín","name":"Okres Kolín"},{"url":"Kolín","name":"Kolín"}],"viewGeometry":{"bbox":[15.15397,50.01916,15.20411,50.04258],"type":"Polygon","coordinates":[[[15.19337,50.03275],[15.19411,50.03222],[15.196,50.0311],[15.19654,50.03095],[15.19807,50.03115],[15.20117,50.0299],[15.20411,50.02926],[15.20399,50.02874],[15.19962,50.02964],[15.19945,50.02932],[15.19932,50.0291],[15.19905,50.02919],[15.1989,50.02912],[15.19846,50.02905],[15.1989,50.02837],[15.19841,50.02806],[15.19838,50.02806],[15.19859,50.02734],[15.19862,50.02721],[15.19862,50.027],[15.19835,50.02669],[15.19645,50.02658],[15.1965,50.02551],[15.19565,50.02458],[15.19642,50.02416],[15.19529,50.02278],[15.19476,50.02155],[15.19402,50.02086],[15.19259,50.02138],[15.19143,50.02018],[15.18905,50.01983],[15.18279,50.0201],[15.18055,50.01916],[15.1771,50.02106],[15.17803,50.02196],[15.17872,50.02197],[15.17995,50.02327],[15.17893,50.02322],[15.17767,50.02398],[15.17573,50.02477],[15.17492,50.02545],[15.17372,50.02496],[15.17141,50.02504],[15.17098,50.02535],[15.16916,50.02492],[15.16298,50.02665],[15.15958,50.02783],[15.15793,50.02793],[15.15816,50.02884],[15.15722,50.03013],[15.15678,50.03125],[15.15569,50.03184],[15.1584,50.03377],[15.15655,50.03431],[15.15397,50.03484],[15.15629,50.03745],[15.15723,50.03704],[15.15899,50.0385],[15.16005,50.038],[15.16236,50.03946],[15.16361,50.04],[15.16287,50.04092],[15.16472,50.04137],[15.16491,50.04042],[15.1657,50.03969],[15.16664,50.03937],[15.16409,50.03843],[15.16572,50.03728],[15.16681,50.03771],[15.16737,50.03714],[15.16919,50.03771],[15.1696,50.03719],[15.17089,50.03875],[15.17448,50.03882],[15.17452,50.03992],[15.17546,50.04102],[15.17718,50.04231],[15.17806,50.04258],[15.17889,50.0403],[15.18069,50.03872],[15.18268,50.03768],[15.18629,50.03646],[15.18956,50.03564],[15.19039,50.03484],[15.19337,50.03275]]]}},"similar":{"items":[{"id":"24171974","url":"/pronajem/byt-3+kk-kolin-280-02/24171974","purpose":"RENT","property":"FLAT","visited":null,"liked":null,"reserved":false,"createdAt":"2024-11-21T08:05:36.455Z","category":"FLAT3_KK","price":{"total":15000,"canonical":15000,"currency":"CZK"},"area":{"main":75,"plot":null},"photos":{"main":"offer/twx/twxvjv94d9-900x1200xc8e8f8"},"location":{"address":"Kolín, 280 02","addressUrl":"Kolín_II,Kolín","locationPrecision":"TOWN","latitude":50.037738,"longitude":15.170059}},{"id":"24077891","url":"/pronajem/byt-3+1-kolin-280-02/24077891","purpose":"RENT","property":"FLAT","visited":null,"liked":null,"reserved":false,"createdAt":"2024-07-30T08:35:58.968Z","category":"FLAT31","price":{"total":15000,"canonical":15000,"currency":"CZK"},"area":{"main":61,"plot":null},"photos":{"main":"offer/mdp/mdphe5uwtn-1200x800xd8d8c8"},"location":{"address":"Kolín, 280 02","addressUrl":"Kolín_II,Kolín","locationPrecision":"TOWN","latitude":50.037738,"longitude":15.170059}},{"id":"24188702","url":"/pronajem/byt-ostatni-ostatni-kolin-280-02/24188702","purpose":"RENT","property":"FLAT","visited":null,"liked":null,"reserved":false,"createdAt":"2024-12-13T17:35:12.904Z","category":"OTHERS_OTHERS","price":{"total":13500,"canonical":13500,"currency":"CZK"},"area":{"main":32,"plot":null},"photos":{"main":"offer/62s/62smgvhj1b-675x1200xb8b8a8"},"location":{"address":"Kolín, 280 02","addressUrl":"Kolín_II,Kolín","locationPrecision":"TOWN","latitude":50.037738,"longitude":15.170059}},{"id":"24193930","url":"/pronajem/byt-2+1-kolin-280-02/24193930","purpose":"RENT","property":"FLAT","visited":null,"liked":null,"reserved":false,"createdAt":"2024-12-26T09:05:39.149Z","category":"FLAT21","price":{"total":14500,"canonical":14500,"currency":"CZK"},"area":{"main":null,"plot":null},"photos":{"main":"offer/y4r/y4r81vsneb-1200x540xf8f8f8"},"location":{"address":"Kolín, 280 02","addressUrl":"Kolín_II,Kolín","locationPrecision":"TOWN","latitude":50.037738,"longitude":15.170059}},{"id":"24195007","url":"/pronajem/byt-2+kk-slunecni-nova-ves-i/24195007","purpose":"RENT","property":"FLAT","visited":null,"liked":null,"reserved":false,"createdAt":"2024-12-29T13:53:59.136Z","category":"FLAT2_KK","price":{"total":15000,"canonical":15000,"currency":"CZK"},"area":{"main":70,"plot":null},"photos":{"main":"offer/me6/me6z4zvwsf-1440x1080xe8e8d8"},"location":{"address":"Sluneční, Nová Ves I","addressUrl":"Sluneční,Nová_Ves_I","locationPrecision":"STREET","latitude":50.0482776,"longitude":15.1571364}},{"id":"24192864","url":"/pronajem/byt-2+kk-benesova-kolin/24192864","purpose":"RENT","property":"FLAT","visited":null,"liked":null,"reserved":false,"createdAt":"2024-12-21T16:20:50.070Z","category":"FLAT2_KK","price":{"total":13000,"canonical":13000,"currency":"CZK"},"area":{"main":43,"plot":null},"photos":{"main":"offer/67m/67m8sz2w1s-1600x898x5898d8"},"location":{"address":"Benešova, Kolín","addressUrl":"Benešova,Kolín","locationPrecision":"STREET","latitude":50.024789928824866,"longitude":15.186821358427897}},{"id":"24184364","url":"/pronajem/byt-2+1-v-brizach-kolin/24184364","purpose":"RENT","property":"FLAT","visited":null,"liked":null,"reserved":false,"createdAt":"2024-12-06T19:44:58.082Z","category":"FLAT21","price":{"total":14000,"canonical":14000,"currency":"CZK"},"area":{"main":59,"plot":null},"photos":{"main":"offer/qz5/qz5qj87tuw-1918x1080x181818"},"location":{"address":"V Břízách, Kolín","addressUrl":"V_Břízách,Kolín","locationPrecision":"EXACT","latitude":50.0261049,"longitude":15.1910222}},{"id":"24177794","url":"/pronajem/byt-2+1-brankovicka-kolin/24177794","purpose":"RENT","property":"FLAT","visited":null,"liked":null,"reserved":false,"createdAt":"2024-11-28T13:00:38.699Z","category":"FLAT21","price":{"total":12000,"canonical":12000,"currency":"CZK"},"area":{"main":60,"plot":60},"photos":{"main":"offer/f1m/f1mf9mstzb-1920x1280x988888"},"location":{"address":"Brankovická, Kolín","addressUrl":"Brankovická,Kolín","locationPrecision":"UNKNOWN","latitude":50.032879027778,"longitude":15.199960138889}}],"filter":{"purpose":"RENT","property":"FLAT","categories":[],"address":"Kolín","bounds":{"northEast":{"latitude":50.137738,"longitude":15.270059},"southWest":{"latitude":49.937737999999996,"longitude":15.070059}},"price":{"from":12000,"to":18000}},"total":24},"deleted":null,"poi":[{"type":"BUS","distance":1271,"name":"Lučební"},{"type":"CONVENIENCE","distance":1820,"name":"ENAPO Andílek"},{"type":"SUPERMARKET","distance":2197,"name":"Pramen"},{"type":"RESTAURANT","distance":1577,"name":"Restaurace Tatra"},{"type":"PUB","distance":1820,"name":"Na Sídlišti"},{"type":"MATERNITY_SCHOOL","distance":1690,"name":"Mateřská škola"},{"type":"SCHOOL","distance":1797,"name":"SOŠ informatiky a spojů a SOU"}],"chat":null}}}},"user":{"user":null},"admin":{"offer":{"offers":{},"previews":{}}}}}},"page":"/search","query":{},"buildId":"lkQR38ioe-TS86Y2K_dX1","isFallback":false,"customServer":true,"gip":true,"scriptLoader":[]}</script></body></html>
            #    
            #    """


            items.append(
                RentalOffer(
                #scraper = self,
                src=self.name,
                raw=deepcopy(offer),
                link = link,
                title = self.category_to_string(offer["category"]) + ", " + str(offer["area"]["main"]) + " m²",
                location = offer["location"]["address"],
                price = offer["price"]["total"],
                image_url = urljoin(self.base_url, "/static/images/" + (offer["photos"]["main"] or "")),
                estate_type=offer["property"]+" "+offer["category"],
                offer_type=offer["purpose"],
                published=offer["createdAt"],
                area=offer["area"]["main"],
                charges=None,
                disposition=offer["category"],
            ))

        return items
