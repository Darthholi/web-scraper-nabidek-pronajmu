from dataclasses import dataclass
from datetime import datetime
import re
from unidecode import unidecode
import pandas as pd

"""
approximations of charges:

1mwh rok

Zdroj
https://ecoten.cz/kalkulacka/

A <50 ... kWh/m2 (za rok)
B 97
C 142
D 191
E 246
F 286
G vic

Tuhle hodnotu vynasobit rozlohou v m2 a vydelit 1000
A vybasobit tim cim se topi:

(Za MWh )
1533 czt centralni panelakovy vdaleny
1176 hneey uhli
699 cerny uhli
4500 el energie
2300 elektrokotel
1118 koks
759 drevo
1169 peletky
1350 propan
1130 stepka
2340 tepelcrpadlo
1270 zemni plyn

"""

def minimal_nongative(x):
    pos = [a for a in x if x >= 0]
    if pos:
        return min(pos)
    return -1


# ordered by importance of match, i.e. latestt ypes are not to be expected and desired to be matched (because can be part of other words or just mentioned in the text randomly)
ESMATCHES = [
"byt|bytu", "dum|domu",
"garsonka|garsonky",
"atypicky|atypicke|atypical",
"pokoj",
"rodinny|rodinne",
"vila|vily",
"chalupa|chalupy",
"chata|chaty",
"bydleni",
"pamatka|pamatky",
"zemedelsky|zemedelske",
"komercni",
"pole",
"louka|louky",
"les",
"rybniku|rybnika",
"sad|sadu",
"zahrada|zahrady",
"ostatni pozemky|pozemk",
"kancelar|kancelarskych prostor",
"sklad|skladu",
"vyrobni prostor|vyrobnich prostor|vyrobniho prostor",
"obchodni prostor|obchodnich prostor|obchodniho prostor",
"ubytovani",
"restaurace",
"cinzovni",
"virtualni kancelar",
"ostatni komercni prostory",
"garaz|garaze|garazove",
"vinny sklep",
"pudni prostor|pudy|puda",
"mobilni domek|mobilniho domku",
"jine nemovitosti",
"na klic",
]

def eq_nonnone(x, y):
    return x is not None and x == y

@dataclass
class RentalOffer:
    raw: dict

    src: str

    link: str

    title: str

    location: str

    price: int  # zero means "ask"

    charges: int

    image_url: str

    offer_type: str  # RENT SELL

    estate_type: str  # FLAT HOUSE

    disposition: str # X+1/kk/X-1/X-kk ...

    published: datetime = None

    description: str = None

    area: int | float | str | None = None

    area_land: int | str | None = None

    photos: list[str] | None = None

    energy_eff: str = None

    energy_eff_verbose: str = None

    yearly_energy: str = None

    active_at: datetime = None # scraped at

    external_urls: list[str] | None = None  # if it admits openly the site has it from somewhere else


    def __post_init__(self):
        """
        TODO:
        - charges not much filled, mostly NaNs
        - offer type is sometimes None, 'prodej', 'rent', 'RENT', 'SELL', 'PRONAJEM', 1, 3, '', None

       - published is the default of now if not used
       - energy eff is normalised, if there was more info it sits at verbose thing.
       - yearly energy not often used (lets eventually calculate)
        """
        assert (self.estate_type is None or isinstance(self.estate_type, str)) and (self.offer_type is None or (isinstance(self.offer_type, str) and len(self.offer_type) > 0))

        if self.active_at is None:
            self.active_at = datetime.now() 
        
        if self.published is None:
            self.published = self.active_at
        
        if not self.disposition:
            self.disposition = None

        sources = self._lowerrem_accents(self.title + " " + (self.description if self.description is not None else "") + " " + self.link)

        if not self.area:
            # TODO care for house aree and land area...
            area_match = re.search(r'([+-]?([0-9]*[.])?[0-9]+)(?=\s*[m2|m²])', sources)
            # or we can apply (\d+)(?=\s*[m2|m²])  # [+-]?([0-9]*[.])?[0-9]+
            if area_match:
                self.area = float(area_match.group(0))
        
        if not self.offer_type:
            sells = re.search("(prodej|sell)", sources)
            rents = re.search("(pronajem|rent)", sources)

            if sells:
                self.offer_type = "sell" 
            elif rents:
                self.offer_type = "rent" 

        if not self.estate_type:
            typematch = re.search(r'|'.join(ESMATCHES), sources)
            assert typematch
            if typematch:
                self.estate_type = typematch.group(0)

            # other way:
            #removebounds = [item for item in [area_position, ofpos, disppos] if item is not None]
            #removebounds = sorted(removebounds, key=lambda x: x[0])
            #extract = sources[:removebounds[-1][1]]
            #for remove in removebounds[::-1]:
             #   extract = extract[:remove[0]] + extract[remove[1]:]
            #extract = extract[removebounds[0][0]:]
            #self.estate_type = extract.strip()
            #self.estate_type = sources[removebounds[0][1]:removebounds[1][0]].strip()
        
        if not self.disposition:
            dispmatch = re.search(r'(\d+[\+\-](1|kk))|atypical', sources)
            if dispmatch:
                self.disposition = dispmatch.group(0)

        # Now these words define the usual "sell [something] [area and or dispositions]"
        # to extract the disposition, we extract the text from min(all those found) to max(all those found)
        # and then just delete the matches and leave with the rest

        self.__normalise__()

    def _lowerrem_accents(self, string):
        if str is None:
            return None
        return unidecode(string.lower()) if isinstance(string, str) else string
    
    def _norm_string(self, string):
        normalisation ={
            "pronajem": "rent",
            "prodej": "sell",
            "1-1": "1+1",
            "1-kk": "1+kk",
            "2-1": "2+1",
            "2-kk": "2+kk",
            "3-1": "3+1",
            "3-kk": "3+kk",
            "4-1": "4+1",
            "4-kk": "4+kk",
            "5-1": "5+1",
            "5-kk": "5+kk",
            "byt": "flat",
            "dum": "house",
            "flat11": "1+1",
            "flat21": "2+1",
            "flat1_kk": "1+kk",
            "flat2_kk": "2+kk",
            "flat3_kk": "3+kk",
            "flat41": "4+1",
            "flat31": "3+1",
            "flat4_kk": "4+kk",
            "flat51": "5+1",
            "flat5_kk": "5+kk",

            "flat flat11": "1+1",
            "flat flat21": "2+1",
            "flat flat1_kk": "1+kk",
            "flat flat2_kk": "2+kk",
            "flat flat3_kk": "3+kk",
            "flat flat41": "4+1",
            "flat flat31": "3+1",
            "flat flat4_kk": "4+kk",
            "flat flat51": "5+1",
            "flat flat5_kk": "5+kk",
            
            "disp_2_1": "2+1",
            "disp_2_kk": "2+kk",
            "disp_3_kk": "3+kk",
            "disp_1_kk": "1+kk",
            "disp_1_1": "1+1",
            "disp_3_1": "3+1",
            "disp_4_1": "4+1",
            "disp_4_kk": "4+kk",
            "disp_5_1": "5+1",
            "disp_5_kk": "5+kk",
        }
        string = self._lowerrem_accents(string)
        return normalisation.get(string, string)

    def __normalise__(self):
        self.price = int(self.price)

        self.offer_type = self._norm_string(self.offer_type)
        self.disposition = self._norm_string(self.disposition)
        self.estate_type = self._norm_string(self.estate_type)

        if isinstance(self.area, str):
            self.area = float(self.area.replace("m2", "").strip())

        if self.energy_eff and len(self.energy_eff) > 1:
            self.energy_eff_verbose = self.energy_eff
            match = re.search(r'[A-G]', self.energy_eff)
            if match:
                self.energy_eff = match.group(0)
            else:
                self.energy_eff = None

        
        if self.estate_type in ["flat"] and not(self.disposition):
            raise ValueError("Disposition not filled")


    def dict(self):
        return self.__dict__.copy()

    def update(self, x):
        self.published = min(x for x in [self.published, x.published] if x is not None)
        self.active_at = max(x for x in [self.active_at, x.active_at] if x is not None)

        for key, value in x.__dict__.items():
            if key in ["published", "active_at"]:
                continue
            if value is not None:
                setattr(self, key, value)

    def equals(self, x):
        """
        Lets say this is a bit higher logic than the hash.

        Explicitely do not use:
            raw - this might be soo detailed and also a raw html with rado mstuff to that
            src
            image url
            photos: list[str] | None = None
            yearly_energy: str = None
            active_at: datetime = None # scraped at
        """
        if eq_nonnone(self.link, x.link) or eq_nonnone(self.description, x.description) \
            or eq_nonnone(self.external_urls, x.link) or eq_nonnone(self.link, x.external_urls) or eq_nonnone(self.external_urls, x.external_urls):
            return True
        
        # the following can be a subject of more investigations as sometimes it might be unfilled...)
        if self.location == x.location and self.price == x.price \
            and self.charges == x.charges and self.offer_type == x.offer_type and self.estate_type == x.estate_type \
            and self.disposition == x.disposition and self.area == x.area \
            and self.area_land == x.area_land and self.energy_eff == x.energy_eff:
            return True
        return False


def records_into_dataframe(all_results):
    alldicts = [item.dict() for item in all_results]
    df = pd.DataFrame(alldicts)
    df["active_at"] = pd.to_datetime(df["active_at"])
    df["published"] = pd.to_datetime(df["published"])
    df["originated_time"] = datetime.now() 
    return df

def merge_update_database(old: pd.DataFrame, new: pd.DataFrame):
    """
    Selects items not older than one month from "old" and merges them with "new" in the following way:

    Items are considered the same if:
      - these columns are equal:
        link
      - or if these columns are equal:
        location, price, charges, offer_type, estate_type, disposition, area, energy_eff
    
    The older items then should be updated in a way that:
    - all columns that are not None in the new item are updated in the old item
    - The column "published" is updated to the older (non-None) of the two
    - The column "active_at" is updated to the newer (non-None) of the two
    """
    new = deduplicate_dataframe(new)  # the new might contain duplicates from different sources
    newids = new.originated_time.max()
    assert newids == new.originated_time.min(), "all the new items should be from the same time"

    threshold = pd.Timedelta("30 days")

    old = old[old["active_at"] > datetime.now() - threshold]
    old_donottouch = old[old["active_at"] <= datetime.now() - threshold]

    subset = pd.concat([old, new], ignore_index=True)
    subset = deduplicate_dataframe(subset)

    combined_df = pd.concat([old_donottouch, subset], ignore_index=True)
    ids_of_news = combined_df[combined_df.originated_time == newids].index

    return combined_df, ids_of_news


def deduplicate_dataframe(df: pd.DataFrame):
    """
    Deduplicates items in the dataframe based on the same logic as merge_update_database.
    Returns the deduplicated dataframe and indexes of rows that were not duplicates.
    """
    def concatenate_rows(df, cols):
        return df[cols].astype(str).agg('-'.join, axis=1)

    def deduplicate_andupdateby_columns(df, cols):
        df = df.sort_values(by=cols).reset_index(drop=True)
        df['concat'] = concatenate_rows(df, cols)
        deduplicated_items = df.drop_duplicates(subset='concat', keep='first', ignore_index=True)

        for index, row in deduplicated_items.iterrows():
            duplicates = df[df['concat'] == row['concat']]  # this can possibly be made faster as we are traversing the sorted dataframe and always start from where we ended before
            if len(duplicates) > 1:
                for col in df.columns:
                    if col not in ["published", "active_at", 'concat', "originated_time"]:
                        non_na_rows = duplicates[~duplicates[col].isna()]
                        if not non_na_rows.empty:
                            latest_row = non_na_rows.loc[non_na_rows['active_at'].idxmax()]
                            deduplicated_items.at[index, col] = latest_row[col]
                deduplicated_items.at[index, 'published'] = min(duplicates['published'])
                deduplicated_items.at[index, 'active_at'] = max(duplicates['active_at'])
                deduplicated_items.at[index, 'originated_time'] = min(duplicates['originated_time'])
        del deduplicated_items['concat']
        return deduplicated_items

    # First deduplicate by "link"
    df = deduplicate_andupdateby_columns(df, ["link"])

    # Now deduplicate by other columns
    cols_to_concat = ["offer_type", "estate_type", "disposition", "price", "charges", "area", "energy_eff", "location"]
    deduplicated_items = deduplicate_andupdateby_columns(df, cols_to_concat)

    return deduplicated_items
