"""
This file contains configurations for QFN packages according to MO-220-K.01.
Not all possible combinations are generated. You can enable more combinations in the table below.
"""

from dataclasses import dataclass

from typing import Optional

from common import format_ipc_dimension as fp
from qfn_common import Size, Variant

# table 1 values
overall_heights = dict(
    V=1.00,
    W=0.80,
)

# body length/width have the same assignment
body_size = dict(
    A=1.0,
    B=1.5,
    C=2.0,
    D=2.5,
    E=3.0,
    F=3.5,
    G=4.0,
    H=5.0,
    J=6.0,
    K=7.0,
    L=8.0,
    M=9.0,
    N=10.0,
    P=11.0,
    R=12.0,
    S=4.5,
    T=5.5,
    U=6.5,
)

terminal_pitch = dict(
    A=1.00,
    B=0.80,
    C=0.65,
    D=0.50,
    E=0.40,
)

# table 3
lead_width = {
    1.00: 0.40,
    0.80: 0.30,
    0.65: 0.30,
    0.50: 0.25,
    0.40: 0.20,
}


@dataclass
class VariantRow:
    tag: str
    D: float
    E: float
    D1: Optional[float]
    E1: Optional[float]
    D2: float
    E2: float
    L: float
    ND: int
    NE: int


# table 6
# other values are derived from variation designators
variant_table_definition = [
    #           tag      D     E     D1    E1    D2    E2    L     ND  NE
    VariantRow('xEEB  ', 3.00, 3.00, 2.75, 2.75, 0.70, 0.70, 0.55, 1, 1),
    VariantRow('xGEB  ', 4.00, 3.00, 3.75, 2.75, 1.70, 0.70, 0.55, 3, 1),
    VariantRow('xGGB  ', 4.00, 4.00, 3.75, 3.75, 1.70, 1.70, 0.55, 3, 3),
    VariantRow('xGGB-1', 4.00, 4.00, None, None, 2.20, 2.20, 0.55, 4, 3),
]


min_K = 0.20


def load_variants() -> list[Variant]:
    variants: list[Variant] = []
    for row in variant_table_definition:
        length_code = row.tag[1]
        width_code = row.tag[2]
        pitch_code = row.tag[3]
        body_size_y = body_size[width_code]
        body_size_x = body_size[length_code]
        pitch = terminal_pitch[pitch_code]
        num_pins = 2 * row.ND + 2 * row.NE
        for height_code in ('V',):  # we ignore 'W' to have less packages
            assert row.D >= 2 * row.L + 2 * min_K + row.D2, row
            assert row.E >= 2 * row.L + 2 * min_K + row.E2, row
            overall_height = overall_heights[height_code]
            variants.append(
                Variant(
                    standard='MO-220-K.01',
                    name=f'H{height_code}F-PQFN-{num_pins}P{fp(pitch)}_{fp(body_size_x)}X{fp(body_size_y)}X{fp(overall_height)}-{row.tag[1:4]}',
                    overall_height=overall_height,
                    body_size_x=body_size_x,
                    body_size_y=body_size_y,
                    pitch=pitch,
                    # upper_body_size_y=row.D1,
                    # upper_body_size_x=row.E1,
                    exposed_pad=Size(width=row.D2, length=row.E2),
                    lead_length_east_west=row.L,
                    lead_length_north_south=row.L,
                    lead_width=lead_width[terminal_pitch[pitch_code]],
                    num_pins_north_south=row.ND,
                    num_pins_east_west=row.NE,
                    min_clearance=min_K,
                )
            )
    return variants
