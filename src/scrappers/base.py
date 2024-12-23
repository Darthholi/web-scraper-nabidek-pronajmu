from abc import abstractmethod
from typing import Any

from requests import Response

from legacy.disposition import Disposition
from scrappers.rental_offer import RentalOffer
from legacy.utils import flatten

from pydantic.utils import deep_update


class ScrapperBase():
    """Hlavní třída pro získávání aktuálních nabídek pronájmu bytů z různých služeb
    """

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    headers = {"User-Agent": user_agent}

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def logo_url(self) -> str:
        pass

    @property
    @abstractmethod
    def color(self) -> int:
        pass

    def __init__(self, config) -> None:
        self._config = self._base_config.copy()
        self._config = deep_update(self._config, config)

    @property
    @abstractmethod
    def _base_confg() -> dict:
        return {}

    @abstractmethod
    def build_response() -> Response:
        """Vytvoří a pošle dotaz na server pro získání nabídek podle nakonfigurovaných parametrů

        Raises:
            NotImplementedError: Pokud potomek neimplementuje tuto metodu

        Returns:
            Response: Odpověď nabídkového serveru obsahující neparsované nabídky
        """
        raise NotImplementedError("Server request builder is not implemeneted")

    @abstractmethod
    def get_latest_offers() -> list[RentalOffer]:
        """Načte a vrátí seznam nejnovějších nabídek bytů k pronájmu z dané služby

        Raises:
            NotImplementedError: Pokud potomek neimplementuje tuto metodu

        Returns:
            list[RentalOffer]: Seznam nabízených bytů k pronájmu
        """
        raise NotImplementedError("Fetching new results is not implemeneted")
