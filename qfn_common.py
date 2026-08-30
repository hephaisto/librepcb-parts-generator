from dataclasses import dataclass


@dataclass(frozen=True)
class Size:
    x: float
    y: float


@dataclass(frozen=True)
class Variant:
    name: str
    standard: str
    overall_height: float  # A
    body_size_x: float  # D
    body_size_y: float  # E
    pitch: float  # e
    # only for rendering, unused because we don't differentiate between different package versions
    # upper_body_size_x: float  # D1
    # upper_body_size_y: float  # E1
    exposed_pad: Size | None  # D2/E2
    lead_length_east_west: float  # L
    lead_length_north_south: float  # L
    lead_width: float  # b
    num_pins_east_west: int  # ND
    num_pins_north_south: int  # NE
    min_clearance: float  # K

    @property
    def num_pins(self) -> int:
        return 2 * (self.num_pins_east_west + self.num_pins_north_south)
