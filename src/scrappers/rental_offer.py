from dataclasses import dataclass
from typing import Union


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

    offer_type: str

    estate_type: str

    published: str = None

    description: str = None

    area: int | str | None = None

    photos: list[str] | None = None

    def dict(self):
        return self.__dict__.copy()

