
import pytest

from line_coding import (
    nrz_l,
    nrz_i,
    manchester,
    differential_manchester,
    ami,
)
from scrambling import b8zs, hdb3
from decoding import decode_line_code


BITS = [1, 0, 1, 1, 0]


@pytest.mark.parametrize(
    "scheme, encoder",
    [
        ("NRZ-L", nrz_l),
        ("NRZ-I", nrz_i),
        ("Manchester", manchester),
        ("Differential Manchester", differential_manchester),
        ("AMI", ami),
    ],
)
def test_basic_line_code_round_trip(scheme, encoder):
    encoded = encoder(BITS)
    decoded = decode_line_code(scheme, encoded)

    assert decoded == BITS


def test_b8zs_eight_consecutive_zeros():
    bits = [0] * 8
    encoded = b8zs(bits)
    decoded = decode_line_code("B8ZS", encoded)

    assert decoded == bits


def test_hdb3_four_consecutive_zeros():
    bits = [0] * 4
    encoded = hdb3(bits)
    decoded = decode_line_code("HDB3", encoded)

    assert decoded == bits


def test_b8zs_after_normal_pulse():
    bits = [1] + [0] * 8
    encoded = b8zs(bits)
    decoded = decode_line_code("B8ZS", encoded)

    assert decoded == bits


def test_hdb3_after_normal_pulse():
    bits = [1] + [0] * 4
    encoded = hdb3(bits)
    decoded = decode_line_code("HDB3", encoded)

    assert decoded == bits
