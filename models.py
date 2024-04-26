from dataclasses import dataclass, field

@dataclass(slots=True)
class Auto:
    id_car: str = ''
    link: str = ''
    price_usd: float = None
    price_byn: float = None
    price_eur: float = None
    price_rub: float = None
    city_location: str = ''
    seller: str = ''
    description: str = ''
    exchange: str = ''
    organization: str = ''
    year: int = ''
    brand: str = ''
    model: str = ''
    condition: str = ''
    properties: list = field(default_factory=list)
    image: list = field(default_factory=list)




