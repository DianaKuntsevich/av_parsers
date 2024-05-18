from dataclasses import dataclass, field

@dataclass(slots=True)
class Auto:
    id_car: str
    link: str = ''
    price_usd: int = 0
    price_byn: int = 0
    price_eur: int = 0
    price_rub: int = 0
    city_location: str = ''
    seller: str = ''
    description: str = ''
    exchange: str = ''
    organization: str = ''
    year: int = ''
    brand: str = ''
    model: str = ''
    condition: str = ''
    alloy_wheels: bool = None
    abs: bool = None
    esp: bool = None
    anti_slip_system: bool = None
    immobilizer: bool = None
    front_safebags: bool = None
    side_safebags: bool = None
    rear_safebags: bool = None
    rain_detector: bool = None
    rear_view_camera: bool = None
    parktronics: bool = None
    hatch: bool = None
    cruise_control: bool = None
    steering_wheel_media_control: bool = None
    electro_seat_adjustment: bool = None
    front_glass_lift: bool = None
    rear_glass_lift: bool = None
    seat_heating: bool = None
    mirror_heating: bool = None
    steering_wheel_heating: bool = None
    climate_control: bool = None
    aux_ipod: bool = None
    bluetooth: bool = None
    cd_mp3_player: bool = None
    usb: bool = None
    media_screen: bool = None
    xenon_lights: bool = None
    fog_lights: bool = None
    led_lights: bool = None
    generation: str = ''
    number_of_seats: str = ''
    engine_capacity: str = ''
    engine_type: str = ''
    transmission_type: str = ''
    generation_with_years: str = ''
    interior_color: str = ''
    interior_material: str = ''
    body_type: str = ''
    drive_type: str = ''
    color: str = ''
    mileage_km: int = 0
    image: list = field(default_factory=list)





