from dataclasses import dataclass
from datetime import datetime
import re
from unidecode import unidecode

def minimal_nongative(x):
    pos = [a for a in x if x >= 0]
    if pos:
        return min(pos)
    return -1


# ordered by importance of match, i.e. latestt ypes are not to be expected and desired to be matched (because can be part of other words or just mentioned in the text randomly)
ESMATCHES = [
"byt|bytu", "dum|domu",
"garsonka|garsonky",
"atypicky|atypicke",
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
"ostatni pozemky",
"kancelare",
"sklad|skladu",
"vyrobni prostor",
"obchodni prostor",
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

@dataclass
class RentalOffer:
    raw: dict

    src: str

    link: str

    title: str

    location: str

    price: int

    charges: int

    image_url: str

    offer_type: str  # RENT SELL

    estate_type: str  # FLAT HOUSE

    disposition: str # X+1/kk

    published: str = None

    description: str = None

    area: int | str | None = None

    photos: list[str] | None = None

    energy_eff: str = None

    active_at: datetime = None # scraped at


    def __post_init__(self):
        if self.active_at is None:
            self.active_at = datetime.now() 


        sources = unidecode((self.title + " " + self.description if self.description is not None else "").lower())
        #area_position = None

        if not self.area:# or not self.estate_type:
            # TODO care for house aree and land area...
            area_match = re.search(r'([+-]?([0-9]*[.])?[0-9]+)(?=\s*[m2|m²])', sources)
            # or we can apply (\d+)(?=\s*[m2|m²])  # [+-]?([0-9]*[.])?[0-9]+
            if area_match:
                if not self.area:
                    self.area = float(area_match.group(0))
                #area_position = area_match.start(), area_match.end()
        
        #ofpos = None
        if not self.offer_type:# or not self.estate_type:
            sells = re.search("(prodej|sell)", sources)
            rents = re.search("(pronajem|rent)", sources)

            if sells:
                if not self.offer_type:
                    self.offer_type = "SELL" 
                #ofpos = sells.start(), sells.end()
            elif rents:
                if not self.offer_type:
                    self.offer_type = "RENT" 
                #ofpos = rents.start(), rents.end()
        
        #disppos = None
        if not self.disposition:# or not self.estate_type:
            dispmatch = re.search(r'(\d+\+(1|kk))', sources)
            if dispmatch:
                if not self.disposition:
                    self.disposition = dispmatch.group(0)
                #disppos = dispmatch.start(), dispmatch.end()

        # Now these words define the usual "sell [something] [area and or dispositions]"
        # to extract the disposition, we extract the text from min(all those found) to max(all those found)
        # and then just delete the matches and leave with the rest

        if not self.estate_type:
            typematch = re.search(r'|'.join(ESMATCHES), sources)
            if typematch:
                if not self.estate_type:
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


    def dict(self):
        return self.__dict__.copy()

