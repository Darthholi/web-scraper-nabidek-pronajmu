import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from scrappers.manager import scrapper_classes



scrapers_settings = {
"BezRealitky":{"variables":{
            "estateType": ["BYT", "DUM"],
            "offerType": ["PRODEJ", "PRONAJEM"],
            #"disposition": [],
            "regionOsmIds": ["R441253"],
            #"regionOsmId": "R441253",  # Kolin
            #"locationPoint": {
            #    "lat": 50.02814,
            #    "lng": 15.20057
            #    },
            #"locationRadius": 10,
}
},
"UlovDomov": {"bounds": {
                "south_west": {
                    "lat": 49.92814,
                    "lng": 15.05057
                },
                "north_east": {
                    "lat": 50.12814,
                    "lng": 15.35057
                },
            },},
"Sreality": {"API_INSIDE_URL_SELECTIONS": "region=Kolín&region-id=3412&region-typ=municipality"},
"Eurobydleni": {
            "sql[locality][locality][input]": "Kolín, Česko",
            "sql[locality][locality][city]": "Kolín, Česko",
            "sql[locality][locality][zip_code]": "",
            "sql[locality][locality][types]": "locality",
            "sql[locality][location][lat]": "50.02814",
            "sql[locality][location][lng]": "15.20057",
            "sql[locality][viewport][south]": "49.92814",
            "sql[locality][viewport][west]": "15.05057",
            "sql[locality][viewport][north]": "50.12814",
            "sql[locality][viewport][east]": "15.35057",
        },
"iDNESReality": {"url": "https://reality.idnes.cz/s/kolin/"},
"REALCITY": {"url": "https://www.realcity.cz/nemovitosti?search=%7B%22prefLoc%22%3A%5B742%5D%2C%22mloc%22%3A%7B%22name%22%3A%22Kol%5Cu00edn%22%7D%2C%22withImage%22%3Atrue%7D"},
"realingo": {"variables": {"address": "Kolin",}},
"Remax": {"url": "https://www.remax-czech.cz/reality/vyhledavani/?desc_text=Kol%C3%ADn&hledani=1&order_by_published_date=0"},
}


def main():
    for settings in scrapers_settings:
        sc_instance = scrapper_classes[settings](scrapers_settings[settings])
        result = sc_instance.get_latest_offers()
        assert result is not None

if __name__ == "__main__":
    main()