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
    alloy_wheels: bool = False
    abs: bool = False
    esp: bool = False
    anti_slip_system: bool = False
    immobilizer: bool = False
    front_safebags: bool = False
    side_safebags: bool = False
    rear_safebags: bool = False
    rain_detector: bool = False
    rear_view_camera: bool = False
    parktronics: bool = False
    hatch: bool = False
    cruise_control: bool = False
    steering_wheel_media_control: bool = False
    electro_seat_adjustment: bool = False
    front_glass_lift: bool = False
    rear_glass_lift: bool = False
    seat_heating: bool = False
    mirror_heating: bool = False
    steering_wheel_heating: bool = False
    climate_control: bool = False
    aux_ipod: bool = False
    bluetooth: bool = False
    cd_mp3_player: bool = False
    usb: bool = False
    media_screen: bool = False
    xenon_lights: bool = False
    fog_lights: bool = False
    led_lights: bool = False
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





