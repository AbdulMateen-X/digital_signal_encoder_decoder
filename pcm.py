
import numpy as np
import matplotlib.pyplot as plt


def generate_analog_signal(num_samples=32, frequency=2, duration=1.0):
    """
    Generate a sampled sine wave.

    Returns:
        sample_times: time of each sample
        samples: amplitude at each sample time
        continuous_times: dense time axis for plotting the original wave
        continuous_signal: smooth reference sine wave
    """
    if num_samples < 2:
        raise ValueError("Number of samples must be at least 2.")
    if frequency <= 0 or duration <= 0:
        raise ValueError("Frequency and duration must be positive.")

    sample_times = np.linspace(0, duration, num_samples, endpoint=False)
    samples = np.sin(2 * np.pi * frequency * sample_times)

    continuous_times = np.linspace(0, duration, 1000, endpoint=False)
    continuous_signal = np.sin(
        2 * np.pi * frequency * continuous_times
    )

    return sample_times, samples, continuous_times, continuous_signal


def quantize_samples(samples, bits_per_sample=3):
    """
    Uniformly quantize samples in the range [-1, 1].

    Returns:
        indices: integer quantization indices
        quantized: reconstructed quantized amplitudes
    """
    if not 1 <= bits_per_sample <= 8:
        raise ValueError("Bits per sample must be between 1 and 8.")

    samples = np.asarray(samples, dtype=float)

    if samples.size == 0:
        raise ValueError("Samples cannot be empty.")

    if np.any(samples < -1) or np.any(samples > 1):
        raise ValueError("Samples must lie between -1 and +1.")

    number_of_levels = 2 ** bits_per_sample
    step_size = 2.0 / number_of_levels

    # Map [-1, 1] to indices 0 through number_of_levels - 1.
    indices = np.floor((samples + 1.0) / step_size).astype(int)
    indices = np.clip(indices, 0, number_of_levels - 1)

    # Use the midpoint of each quantization interval as its output.
    quantized = -1.0 + (indices + 0.5) * step_size

    return indices, quantized


def pcm_encode(samples, bits_per_sample=3):
    """
    Encode sample amplitudes as a PCM binary bitstream.

    Returns:
        bitstream: list of bits
        indices: quantization indices
        quantized: quantized sample amplitudes
    """
    indices, quantized = quantize_samples(samples, bits_per_sample)

    bitstream = []
    for index in indices:
        binary_code = format(int(index), f"0{bits_per_sample}b")
        bitstream.extend(int(bit) for bit in binary_code)

    return bitstream, indices, quantized


def pcm_decode(bitstream, bits_per_sample=3):
    """
    Decode a PCM bitstream into quantization indices and amplitudes.
    """
    if not 1 <= bits_per_sample <= 8:
        raise ValueError("Bits per sample must be between 1 and 8.")

    if not bitstream:
        raise ValueError("Bitstream cannot be empty.")

    if any(bit not in (0, 1) for bit in bitstream):
        raise ValueError("Bitstream must contain only 0 and 1.")

    if len(bitstream) % bits_per_sample != 0:
        raise ValueError(
            "Bitstream length must be divisible by bits_per_sample."
        )

    number_of_levels = 2 ** bits_per_sample
    step_size = 2.0 / number_of_levels

    indices = []
    for start in range(0, len(bitstream), bits_per_sample):
        group = bitstream[start:start + bits_per_sample]
        index = int("".join(str(bit) for bit in group), 2)
        indices.append(index)

    indices = np.asarray(indices, dtype=int)
    quantized = -1.0 + (indices + 0.5) * step_size

    return indices, quantized


def plot_pcm(
    sample_times,
    samples,
    continuous_times,
    continuous_signal,
    decoded_samples,
):
    """Plot the analog signal, sampled values and PCM staircase."""
    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(
        continuous_times,
        continuous_signal,
        label="Original analog signal",
        linewidth=2,
    )

    ax.scatter(
        sample_times,
        samples,
        label="Sampled values",
        zorder=3,
    )

    ax.step(
        sample_times,
        decoded_samples,
        where="mid",
        label="PCM staircase reconstruction",
        linewidth=2,
    )

    ax.set_title("PCM Encoding and Decoding")
    ax.set_xlabel("Time (seconds)")
    ax.set_ylabel("Amplitude")
    ax.set_ylim(-1.3, 1.3)
    ax.grid(True, alpha=0.3)
    ax.legend()

    plt.tight_layout()
    plt.show()
