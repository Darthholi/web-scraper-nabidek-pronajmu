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


    def get_all_fields(self):
        introspection_query = {
            "query": """
                {
                    __schema {
                        queryType {
                            fields {
                                name
                                type {
                                    name
                                    kind
                                    ofType {
                                        name
                                        kind
                                        ofType {
                                            name
                                            kind
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            """
        }

        response = requests.post(self.base_url, headers=self.headers, json=introspection_query)
        return response.json()

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

        for offer in tqdm(response["data"]["searchOffer"]["items"], desc="Realingo", leave=False):
            # todo does not provide more details, would need to go to the details

            link = urljoin(self.base_url, offer["url"])

            detail = {}
            if self.details_allowed:
                detail_res = requests.get(link)
                if detail_res.status_code == 200:
                    sdetail = BeautifulSoup(detail_res.content, 'html.parser')

                    properties = json.loads(sdetail.find("script", {"id":"__NEXT_DATA__"}).get_text())
                    id = list(properties["props"]["pageProps"]["store"]["offer"]["details"].keys())[0]
                    properties = properties["props"]["pageProps"]["store"]["offer"]["details"][id]["offer"]
                    # properties["offer"] should be similar to offer
                    detail = properties["detail"]

            price = offer["price"]["total"]
            if price is None:
                assert offer["price"]["type"] == "NEGOTIABLE"
                price = 0

            items.append(
                RentalOffer(
                #scraper = self,
                src=self.name,
                raw=deepcopy(offer),
                link = link,
                title = self.category_to_string(offer["category"]) + ", " + str(offer["area"]["main"]) + " m²",
                location = offer["location"]["address"],
                price = price,
                image_url = urljoin(self.base_url, "/static/images/" + (offer["photos"]["main"] or "")),
                estate_type=offer["property"],
                offer_type=offer["purpose"],
                published=offer["createdAt"],
                area=offer["area"]["main"],
                charges=None,
                disposition=offer["category"],
                description=detail.get("description", None),
                external_urls=[detail.get("externalUrl", None)],
            ))

        return items
