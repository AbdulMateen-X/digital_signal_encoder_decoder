
def b8zs(bits, initial_pulse=-1):
    """
    B8ZS scrambling.

    Each run of eight zeros is replaced with:
        000VB0VB

    V = bipolar violation: same polarity as the preceding pulse.
    B = normal bipolar pulse: opposite polarity to the preceding pulse.

    initial_pulse is the polarity of the pulse immediately before
    the input sequence. It defaults to -1, so the first normal
    AMI mark has polarity +1.
    """
    if not bits:
        raise ValueError("Input bit sequence cannot be empty.")

    if any(bit not in (0, 1) for bit in bits):
        raise ValueError("Input must contain only 0 and 1.")

    if initial_pulse not in (-1, 1):
        raise ValueError("initial_pulse must be +1 or -1.")

    encoded = []
    last_pulse = initial_pulse
    i = 0

    while i < len(bits):
        if bits[i:i + 8] == [0] * 8:
            p = last_pulse

            # 000VB0VB, with polarity determined by the previous pulse.
            encoded.extend([0, 0, 0, p, -p, 0, -p, p])

            # The final B pulse has polarity p.
            last_pulse = p
            i += 8
        elif bits[i] == 0:
            encoded.append(0)
            i += 1
        else:
            last_pulse *= -1
            encoded.append(last_pulse)
            i += 1

    return encoded


def hdb3(bits, initial_pulse=-1):
    """
    HDB3 scrambling.

    Four consecutive zeros are replaced by:
        000V if the number of nonzero pulses since the previous
        violation is odd.
        B00V if that count is even.

    V = violation pulse, same polarity as the preceding pulse.
    B = normal bipolar pulse, opposite polarity to the preceding pulse.
    """
    if not bits:
        raise ValueError("Input bit sequence cannot be empty.")

    if any(bit not in (0, 1) for bit in bits):
        raise ValueError("Input must contain only 0 and 1.")

    if initial_pulse not in (-1, 1):
        raise ValueError("initial_pulse must be +1 or -1.")

    encoded = []
    last_pulse = initial_pulse
    pulses_since_violation = 0
    i = 0

    while i < len(bits):
        if bits[i:i + 4] == [0] * 4:
            if pulses_since_violation % 2 == 1:
                # 000V: violation pulse has the same polarity
                # as the preceding pulse.
                violation = last_pulse
                encoded.extend([0, 0, 0, violation])
            else:
                # B00V: B is a normal pulse, then V repeats
                # the polarity of B to create a violation.
                balancing = -last_pulse
                violation = balancing
                encoded.extend([balancing, 0, 0, violation])

            last_pulse = violation
            pulses_since_violation = 0
            i += 4
        elif bits[i] == 0:
            encoded.append(0)
            i += 1
        else:
            last_pulse *= -1
            encoded.append(last_pulse)
            pulses_since_violation += 1
            i += 1

    return encoded
