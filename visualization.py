
import numpy as np
import matplotlib.pyplot as plt


def plot_line_code(bits, encoded_levels, scheme):
    """
    Plot the original bitstream and its encoded waveform.

    NRZ schemes: one level per bit.
    Manchester schemes: two levels per bit (half-bit intervals).
    """
    if not bits:
        raise ValueError("Cannot plot an empty bit sequence.")

    if scheme in ("Manchester", "Differential Manchester"):
        levels_per_bit = 2
    else:
        levels_per_bit = 1

    expected_length = len(bits) * levels_per_bit

    if len(encoded_levels) != expected_length:
        raise ValueError(
            f"{scheme} requires {expected_length} encoded levels, "
            f"but received {len(encoded_levels)}."
        )

    n = len(bits)

    fig, (ax_bits, ax_signal) = plt.subplots(
        2,
        1,
        figsize=(12, 6),
        sharex=True,
        gridspec_kw={"height_ratios": [1, 2]},
    )

    # Original digital data: each bit lasts one time unit.
    bit_edges = np.arange(n + 1)
    bit_x = np.repeat(bit_edges, 2)[1:-1]
    bit_y = np.repeat(bits, 2)

    ax_bits.step(bit_x, bit_y, where="post", linewidth=2)
    ax_bits.set_yticks([0, 1])
    ax_bits.set_ylim(-0.3, 1.3)
    ax_bits.set_ylabel("Bit")
    ax_bits.set_title("Original Digital Data")
    ax_bits.grid(True, alpha=0.3)

    # Encoded signal: half-bit intervals for Manchester schemes.
    interval = 1 / levels_per_bit
    signal_edges = np.arange(len(encoded_levels) + 1) * interval
    signal_x = np.repeat(signal_edges, 2)[1:-1]
    signal_y = np.repeat(encoded_levels, 2)

    ax_signal.step(
        signal_x,
        signal_y,
        where="post",
        linewidth=2,
    )
    ax_signal.set_yticks([-1, 0, 1])
    ax_signal.set_ylim(-1.5, 1.5)
    ax_signal.set_ylabel("Voltage level")
    ax_signal.set_xlabel("Bit interval")
    ax_signal.set_title(f"{scheme} Encoded Waveform")
    ax_signal.set_xticks(bit_edges)
    ax_signal.grid(True, alpha=0.3)

    # Show bit boundaries on both plots.
    for boundary in bit_edges:
        ax_bits.axvline(boundary, linestyle=":", alpha=0.3)
        ax_signal.axvline(boundary, linestyle=":", alpha=0.3)

    # Show the midpoint of each bit for Manchester schemes.
    if levels_per_bit == 2:
        for midpoint in np.arange(n) + 0.5:
            ax_signal.axvline(
                midpoint,
                linestyle="--",
                alpha=0.2,
            )

    plt.tight_layout()
    plt.show()
