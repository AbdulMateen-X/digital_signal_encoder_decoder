
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


def test_nrz_l_round_trip():
    encoded = nrz_l(BITS)
    assert decode_line_code("NRZ-L", encoded) == BITS


def test_nrz_i_round_trip():
    encoded = nrz_i(BITS)
    assert decode_line_code("NRZ-I", encoded) == BITS


def test_manchester_round_trip():
    encoded = manchester(BITS)
    assert decode_line_code("Manchester", encoded) == BITS


def test_differential_manchester_round_trip():
    encoded = differential_manchester(BITS)
    assert decode_line_code("Differential Manchester", encoded) == BITS


def test_ami_round_trip():
    encoded = ami(BITS)
    assert decode_line_code("AMI", encoded) == BITS


def test_b8zs_eight_zeros():
    bits = [0] * 8
    encoded = b8zs(bits)
    assert decode_line_code("B8ZS", encoded) == bits


def test_hdb3_four_zeros():
    bits = [0] * 4
    encoded = hdb3(bits)
    assert decode_line_code("HDB3", encoded) == bits


def test_b8zs_after_one():
    bits = [1] + [0] * 8
    encoded = b8zs(bits)
    assert decode_line_code("B8ZS", encoded) == bits


def test_hdb3_after_one():
    bits = [1] + [0] * 4
    encoded = hdb3(bits)
    assert decode_line_code("HDB3", encoded) == bits
