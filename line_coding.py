
def nrz_l(bits):
    """
    NRZ-L encoding:
    0 -> +1 (high level)
    1 -> -1 (low level)
    """
    if not bits:
        raise ValueError("Input bit sequence cannot be empty.")

    if any(bit not in (0, 1) for bit in bits):
        raise ValueError("Input must contain only 0 and 1.")

    return [1 if bit == 0 else -1 for bit in bits]


def nrz_i(bits, initial_level=-1):
    """
    NRZ-I encoding:
    1 -> transition at the beginning of the bit interval
    0 -> no transition

    The signal starts at initial_level, which must be +1 or -1.
    The returned level for each bit is the level during that bit.
    """
    if not bits:
        raise ValueError("Input bit sequence cannot be empty.")

    if any(bit not in (0, 1) for bit in bits):
        raise ValueError("Input must contain only 0 and 1.")

    if initial_level not in (-1, 1):
        raise ValueError("Initial level must be +1 or -1.")

    level = initial_level
    encoded = []

    for bit in bits:
        if bit == 1:
            level *= -1

        encoded.append(level)

    return encoded


def manchester(bits):
    """
    Manchester encoding:
    0 -> high-to-low (+1, -1)
    1 -> low-to-high (-1, +1)

    There is always a transition in the middle of each bit.
    """
    if not bits:
        raise ValueError("Input bit sequence cannot be empty.")

    if any(bit not in (0, 1) for bit in bits):
        raise ValueError("Input must contain only 0 and 1.")

    encoded = []

    for bit in bits:
        if bit == 0:
            encoded.extend([1, -1])
        else:
            encoded.extend([-1, 1])

    return encoded


def differential_manchester(bits, initial_level=-1):
    """
    Differential Manchester encoding:
    - Always transition in the middle of each bit.
    - 0 -> transition at the beginning of the bit.
    - 1 -> no transition at the beginning of the bit.

    initial_level is the signal level immediately before the first bit.
    Two levels are returned for every input bit.
    """
    if not bits:
        raise ValueError("Input bit sequence cannot be empty.")

    if any(bit not in (0, 1) for bit in bits):
        raise ValueError("Input must contain only 0 and 1.")

    if initial_level not in (-1, 1):
        raise ValueError("Initial level must be +1 or -1.")

    level = initial_level
    encoded = []

    for bit in bits:
        # A zero causes a transition at the start of the bit.
        if bit == 0:
            level *= -1

        # First half of the bit interval.
        encoded.append(level)

        # Mandatory transition in the middle of every bit.
        level *= -1
        encoded.append(level)

    return encoded



def ami(bits, initial_pulse=-1):
    """
    Alternate Mark Inversion (AMI):
    0 -> 0
    1 -> alternating +1 and -1 pulses.
    """
    if not bits:
        raise ValueError("Input bit sequence cannot be empty.")

    if any(bit not in (0, 1) for bit in bits):
        raise ValueError("Input must contain only 0 and 1.")

    if initial_pulse not in (-1, 1):
        raise ValueError("initial_pulse must be +1 or -1.")

    last_pulse = initial_pulse
    encoded = []

    for bit in bits:
        if bit == 0:
            encoded.append(0)
        else:
            last_pulse *= -1
            encoded.append(last_pulse)

    return encoded
