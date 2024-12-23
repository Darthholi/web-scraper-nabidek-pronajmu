from srappers.scrapes_manager import scrapper_classes

scrapers_settings = {
"BezRealitky": 
{
    "operationName": "AdvertList",
    "variables": {
        "limit": 15,
        "offset": 75,
        "order": "TIMEORDER_DESC",
        "locale": "CS",
        "offerType": [],
        "estateType": [],
        "disposition": [],
        "regionOsmIds": []
    },
    "query": "query AdvertList($locale: Locale!, $estateType: [EstateType], $offerType: [OfferType], $disposition: [Disposition], $region: ID, $regionOsmIds: [ID], $limit: Int = 15, $offset: Int = 0, $order: ResultOrder = TIMEORDER_DESC, $petFriendly: Boolean, $balconyFrom: Float, $balconyTo: Float, $loggiaFrom: Float, $loggiaTo: Float, $terraceFrom: Float, $terraceTo: Float, $cellarFrom: Float, $cellarTo: Float, $parking: Boolean, $garage: Boolean, $newBuilding: Boolean, $lift: Boolean, $ownership: [Ownership], $construction: [Construction], $equipped: [Equipped], $priceFrom: Int, $priceTo: Int, $surfaceFrom: Int, $surfaceTo: Int, $advertId: [ID], $roommate: Boolean, $includeImports: Boolean, $boundaryPoints: [GPSPointInput], $discountedOnly: Boolean, $barrierFree: Boolean, $polygonBuffer: Int, $availableFrom: DateTime) {\n  listAdverts(\n    offerType: $offerType\n    estateType: $estateType\n    disposition: $disposition\n    limit: $limit\n    regionId: $region\n    regionOsmIds: $regionOsmIds\n    offset: $offset\n    order: $order\n    petFriendly: $petFriendly\n    balconySurfaceFrom: $balconyFrom\n    balconySurfaceTo: $balconyTo\n    loggiaSurfaceFrom: $loggiaFrom\n    loggiaSurfaceTo: $loggiaTo\n    terraceSurfaceFrom: $terraceFrom\n    terraceSurfaceTo: $terraceTo\n    cellarSurfaceFrom: $cellarFrom\n    cellarSurfaceTo: $cellarTo\n    parking: $parking\n    garage: $garage\n    newBuilding: $newBuilding\n    lift: $lift\n    ownership: $ownership\n    construction: $construction\n    equipped: $equipped\n    priceFrom: $priceFrom\n    priceTo: $priceTo\n    surfaceFrom: $surfaceFrom\n    surfaceTo: $surfaceTo\n    ids: $advertId\n    roommate: $roommate\n    includeImports: $includeImports\n    boundaryPoints: $boundaryPoints\n    discountedOnly: $discountedOnly\n    polygonBuffer: $polygonBuffer\n    barrierFree: $barrierFree\n    availableFrom: $availableFrom\n  ) {\n    list {\n      id\n      uri\n      estateType\n      offerType\n      disposition\n      imageAltText(locale: $locale)\n      mainImage {\n        id\n        url(filter: RECORD_THUMB)\n        __typename\n      }\n      address(locale: $locale)\n      surface\n      surfaceLand\n      tags(locale: $locale)\n      price\n      charges\n      currency\n      petFriendly\n      reserved\n      highlighted\n      roommate\n      project {\n        id\n        __typename\n      }\n      gps {\n        lat\n        lng\n        __typename\n      }\n      mortgageData(locale: $locale) {\n        rateLow\n        rateHigh\n        loan\n        years\n        __typename\n      }\n      originalPrice\n      isDiscounted\n      nemoreport {\n        id\n        status\n        timeCreated\n        __typename\n      }\n      isNew\n      videos {\n        id\n        previewUrl\n        status\n        __typename\n      }\n      links {\n        id\n        url\n        type\n        status\n        __typename\n      }\n      __typename\n    }\n    totalCount\n    __typename\n  }\n  actionList: listAdverts(\n    offerType: $offerType\n    estateType: $estateType\n    disposition: $disposition\n    regionId: $region\n    regionOsmIds: $regionOsmIds\n    offset: $offset\n    order: $order\n    petFriendly: $petFriendly\n    balconySurfaceFrom: $balconyFrom\n    balconySurfaceTo: $balconyTo\n    loggiaSurfaceFrom: $loggiaFrom\n    loggiaSurfaceTo: $loggiaTo\n    terraceSurfaceFrom: $terraceFrom\n    terraceSurfaceTo: $terraceTo\n    cellarSurfaceFrom: $cellarFrom\n    cellarSurfaceTo: $cellarTo\n    parking: $parking\n    garage: $garage\n    newBuilding: $newBuilding\n    lift: $lift\n    ownership: $ownership\n    construction: $construction\n    equipped: $equipped\n    priceFrom: $priceFrom\n    priceTo: $priceTo\n    surfaceFrom: $surfaceFrom\n    surfaceTo: $surfaceTo\n    ids: $advertId\n    roommate: $roommate\n    includeImports: $includeImports\n    boundaryPoints: $boundaryPoints\n    discountedOnly: true\n    limit: 3\n    availableFrom: $availableFrom\n  ) {\n    list {\n      id\n      uri\n      estateType\n      offerType\n      disposition\n      imageAltText(locale: $locale)\n      mainImage {\n        id\n        url(filter: RECORD_THUMB)\n        __typename\n      }\n      address(locale: $locale)\n      surface\n      surfaceLand\n      tags(locale: $locale)\n      price\n      charges\n      currency\n      petFriendly\n      reserved\n      highlighted\n      roommate\n      project {\n        id\n        __typename\n      }\n      gps {\n        lat\n        lng\n        __typename\n      }\n      mortgageData(locale: $locale) {\n        rateLow\n        rateHigh\n        loan\n        years\n        __typename\n      }\n      originalPrice\n      isDiscounted\n      nemoreport {\n        id\n        status\n        timeCreated\n        __typename\n      }\n      isNew\n      videos {\n        id\n        previewUrl\n        status\n        __typename\n      }\n      links {\n        id\n        url\n        type\n        status\n        __typename\n      }\n      __typename\n    }\n    totalCount\n    __typename\n  }\n}\n"
}.update(
{
            "estateType": [],
            "offerType": "PRODEJ",
            "disposition": [],
            "regionOsmIds": ["R441315"],  # kolin

}

)
}


def main():
    for settings in scrapers_settings:
        sc_instance = scrapper_classes[settings](scrapers_settings[settings])
        sc_instance.get_latest_offers()