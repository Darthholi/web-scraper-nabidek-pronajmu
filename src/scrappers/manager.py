import logging
import traceback

from legacy.config import *
from legacy.disposition import Disposition
from scrappers.rental_offer import RentalOffer
from scrappers.base import ScrapperBase
from scrappers.bravis import ScraperBravis
from scrappers.euro_bydleni import ScraperEuroBydleni
from scrappers.idnes_reality import ScraperIdnesReality
from scrappers.realcity import ScraperRealcity
from scrappers.realingo import ScraperRealingo
from scrappers.remax import ScraperRemax
from scrappers.sreality import ScraperSreality
from scrappers.ulov_domov import ScraperUlovDomov
from scrappers.bezrealitky import ScraperBezrealitky


scrapper_classes = {scrapper.name: scrapper for scrapper in [ScraperBravis,
        ScraperEuroBydleni,
        ScraperIdnesReality,
        ScraperRealcity,
        ScraperRealingo,
        ScraperRemax,
        ScraperSreality,
        ScraperUlovDomov,
        ScraperBezrealitky]}





def fetch_latest_offers(scrapers: list[ScrapperBase]) -> list[RentalOffer]:
    """Získá všechny nejnovější nabídky z dostupných serverů

    Returns:
        list[RentalOffer]: Seznam nabídek
    """

    offers: list[RentalOffer] = []
    for scraper in scrapers:
        try:
            for offer in scraper.get_latest_offers():
                offers.append(offer)
        except Exception:
            logging.error(traceback.format_exc())

    return offers
