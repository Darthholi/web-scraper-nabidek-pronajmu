from tqdm import tqdm
from scrappers.manager import scrapper_classes

import pandas as pd
import os

from scrappers.rental_offer import deduplicate_dataframe, merge_update_database, records_into_dataframe

scrapers_settings = {
"Kolin_test": {
    "REALCITY": {"url": "https://www.realcity.cz/nemovitosti?search=%7B%22prefLoc%22%3A%5B742%5D%2C%22mloc%22%3A%7B%22name%22%3A%22Kol%5Cu00edn%22%7D%2C%22withImage%22%3Atrue%7D"},
},
    
    
    "Kolin":
                     {
"iDNESReality": {"url": "https://reality.idnes.cz/s/kolin/"},
"realingo": {"variables": {"address": "Kolin",}},
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
"Remax": {"url": "https://www.remax-czech.cz/reality/vyhledavani/?desc_text=Kol%C3%ADn&hledani=1&order_by_published_date=0"},
"REALCITY": {"url": "https://www.realcity.cz/nemovitosti?search=%7B%22prefLoc%22%3A%5B742%5D%2C%22mloc%22%3A%7B%22name%22%3A%22Kol%5Cu00edn%22%7D%2C%22withImage%22%3Atrue%7D"},
},
}


def main():
    for location in scrapers_settings:
        if "test" in location:
            continue
        all_results = []
        for settings in tqdm(scrapers_settings[location], desc=location):
            sc_instance = scrapper_classes[settings](scrapers_settings[location][settings])
            all_results.extend(sc_instance.get_latest_offers())
        df = records_into_dataframe(all_results)
        #df.to_parquet(location+".parquet")
        del df["raw"]
        if os.path.exists(location + ".parquet"):
            existing_df = pd.read_parquet(location + ".parquet")
            #existing_df = pd.read_csv(location + ".csv", parse_dates=["active_at", "published"])
            #existing_df["active_at"] = pd.to_datetime(existing_df["active_at"])
            #existing_df["published"] = pd.to_datetime(existing_df["published"])
            df, indexes = merge_update_database(existing_df, df)

            print(f"Total {len(df)} records")
            print(f"New {len(indexes)} records")
            print(df.loc[indexes])

        else:
            df = deduplicate_dataframe(df)
        df.to_parquet(location + ".parquet", index=False)
            
        assert all_results is not None
            

if __name__ == "__main__":
    main()