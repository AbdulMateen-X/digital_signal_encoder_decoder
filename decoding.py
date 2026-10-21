
def _validate_levels(levels, allowed=(-1, 0, 1)):
    if not levels:
        raise ValueError("Encoded signal cannot be empty.")

    if any(level not in allowed for level in levels):
        raise ValueError(
            f"Signal levels must be among {allowed}."
        )


def _validate_binary(bits):
    if not bits:
        raise ValueError("Bitstream cannot be empty.")

    if any(bit not in (0, 1) for bit in bits):
        raise ValueError("Bits must contain only 0 and 1.")


def nrz_l_decode(levels):
    """NRZ-L: +1 represents 0; -1 represents 1."""
    _validate_levels(levels, allowed=(-1, 1))
    return [0 if level == 1 else 1 for level in levels]


def nrz_i_decode(levels, initial_level=-1):
    """NRZ-I: a transition at a bit boundary represents 1."""
    _validate_levels(levels, allowed=(-1, 1))

    if initial_level not in (-1, 1):
        raise ValueError("Initial level must be -1 or +1.")

    bits = []
    previous = initial_level

    for level in levels:
        bits.append(1 if level != previous else 0)
        previous = level

    return bits


def manchester_decode(levels):
    """Manchester: [+1, -1] -> 0; [-1, +1] -> 1."""
    _validate_levels(levels, allowed=(-1, 1))

    if len(levels) % 2 != 0:
        raise ValueError("Manchester signal needs two levels per bit.")

    bits = []

    for i in range(0, len(levels), 2):
        pair = levels[i:i + 2]

        if pair == [1, -1]:
            bits.append(0)
        elif pair == [-1, 1]:
            bits.append(1)
        else:
            raise ValueError(
                f"Invalid Manchester pair at position {i}: {pair}"
            )

    return bits


def differential_manchester_decode(levels, initial_level=-1):
    """
    A transition at the start of a bit represents 0.
    No transition at the start represents 1.
    Every bit has a middle transition.
    """
    _validate_levels(levels, allowed=(-1, 1))

    if initial_level not in (-1, 1):
        raise ValueError("Initial level must be -1 or +1.")

    if len(levels) % 2 != 0:
        raise ValueError(
            "Differential Manchester needs two levels per bit."
        )

    bits = []
    previous = initial_level

    for i in range(0, len(levels), 2):
        first, second = levels[i:i + 2]

        if first == second:
            raise ValueError(
                f"Missing middle transition at position {i}."
            )

        bits.append(0 if first != previous else 1)
        previous = second

    return bits


def ami_decode(levels, initial_pulse=-1):
    """Decode ordinary AMI: nonzero pulses represent 1."""
    _validate_levels(levels)

    if initial_pulse not in (-1, 1):
        raise ValueError("Initial pulse must be -1 or +1.")

    bits = []
    previous = initial_pulse

    for i, level in enumerate(levels):
        if level == 0:
            bits.append(0)
        else:
            if level == previous:
                raise ValueError(
                    f"AMI bipolar violation at position {i}; "
                    "use the B8ZS/HDB3 decoder if scrambling was used."
                )

            bits.append(1)
            previous = level

    return bits


def b8zs_decode(levels, initial_pulse=-1):
    """Decode AMI levels containing standard B8ZS substitutions."""
    _validate_levels(levels)

    if initial_pulse not in (-1, 1):
        raise ValueError("Initial pulse must be -1 or +1.")

    bits = []
    last_pulse = initial_pulse
    i = 0

    while i < len(levels):
        # Standard B8ZS pattern: 000VB0VB
        p = last_pulse
        pattern = [0, 0, 0, p, -p, 0, p, -p]

        if levels[i:i + 8] == pattern:
            bits.extend([0] * 8)
            last_pulse = -p
            i += 8
            continue

        level = levels[i]

        if level == 0:
            bits.append(0)
        else:
            if level == last_pulse:
                raise ValueError(
                    f"Unexpected bipolar violation at position {i}."
                )

            bits.append(1)
            last_pulse = level

        i += 1

    return bits


def hdb3_decode(levels, initial_pulse=-1):
    """
    Decode HDB3 substitutions:
    000V when the number of pulses since the last violation is odd;
    B00V when it is even.
    """
    _validate_levels(levels)

    if initial_pulse not in (-1, 1):
        raise ValueError("Initial pulse must be -1 or +1.")

    bits = []
    last_pulse = initial_pulse
    pulses_since_violation = 0
    i = 0

    while i < len(levels):
        group = levels[i:i + 4]

        # 000V: V has the same polarity as the previous pulse.
        if (
            len(group) == 4
            and group[:3] == [0, 0, 0]
            and group[3] == last_pulse
        ):
            bits.extend([0, 0, 0, 0])
            pulses_since_violation = 0
            i += 4
            continue

        # B00V: B and V have the same polarity, opposite
        # to the preceding pulse. This is used for even parity.
        balancing_pulse = -last_pulse

        if (
            len(group) == 4
            and group == [
                balancing_pulse, 0, 0, balancing_pulse
            ]
            and pulses_since_violation % 2 == 0
        ):
            bits.extend([0, 0, 0, 0])
            last_pulse = balancing_pulse
            pulses_since_violation = 0
            i += 4
            continue

        level = levels[i]

        if level == 0:
            bits.append(0)
        else:
            if level == last_pulse:
                raise ValueError(
                    f"Unexpected HDB3 violation at position {i}."
                )

            bits.append(1)
            last_pulse = level
            pulses_since_violation += 1

        i += 1

    return bits


def decode_line_code(
    scheme,
    levels,
    initial_level=-1,
    initial_pulse=-1
):
    """Dispatch to the decoder selected by the user."""
    decoders = {
        "NRZ-L": lambda: nrz_l_decode(levels),
        "NRZ-I": lambda: nrz_i_decode(levels, initial_level),
        "Manchester": lambda: manchester_decode(levels),
        "Differential Manchester": lambda:
            differential_manchester_decode(levels, initial_level),
        "AMI": lambda: ami_decode(levels, initial_pulse),
        "B8ZS": lambda: b8zs_decode(levels, initial_pulse),
        "HDB3": lambda: hdb3_decode(levels, initial_pulse),
    }

    if scheme not in decoders:
        raise ValueError(f"Unsupported line-coding scheme: {scheme}")

    return decoders[scheme]()
