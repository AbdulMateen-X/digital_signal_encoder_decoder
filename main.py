
from digital_data import (
    generate_random_bits,
    generate_fixed_zero_bits,
    bits_to_string,
    longest_palindrome,
)

from line_coding import (
    nrz_l,
    nrz_i,
    manchester,
    differential_manchester,
    ami,
)

from scrambling import b8zs, hdb3
from visualization import plot_line_code

from pcm import (
    generate_analog_signal,
    pcm_encode,
    pcm_decode,
    plot_pcm,
)

from decoding import decode_line_code


# ---------------------------------------------------------
# Digital data generation
# ---------------------------------------------------------

def generate_data():
    print("\n--- Digital Data Generator ---")
    print("1. Completely random binary data")
    print("2. Random data containing four consecutive zeros")
    print("3. Random data containing eight consecutive zeros")

    choice = input("Choose an option (1-3): ").strip()

    if choice not in ("1", "2", "3"):
        print("Invalid choice.")
        return None

    try:
        length = int(input("Enter the number of bits: "))

        if length <= 0:
            print("Length must be positive.")
            return None

        if choice == "1":
            bits = generate_random_bits(length)
        elif choice == "2":
            bits = generate_fixed_zero_bits(length, 4)
        else:
            bits = generate_fixed_zero_bits(length, 8)

        palindrome = longest_palindrome(bits)

        print("\n--- Generated Data ---")
        print("Digital stream:", bits_to_string(bits))
        print("Longest palindrome:", bits_to_string(palindrome))
        print("Palindrome length:", len(palindrome))

        return bits

    except ValueError as error:
        print("Input error:", error)
        return None


def read_bits():
    raw_bits = input(
        "Enter binary data, or press Enter to generate random data: "
    ).strip()

    if raw_bits:
        if any(bit not in "01" for bit in raw_bits):
            raise ValueError("Input must contain only 0 and 1.")
        return [int(bit) for bit in raw_bits]

    length = int(input("Enter the number of bits: "))

    if length <= 0:
        raise ValueError("Length must be positive.")

    return generate_random_bits(length)


# ---------------------------------------------------------
# Decoder helpers
# ---------------------------------------------------------

def decode_prompt(scheme_name, encoded):
    """Ask whether the user wants to decode the encoded signal."""

    answer = input(
        "\nDo you want to decode this signal? (y/n): "
    ).strip().lower()

    if answer not in ("y", "yes"):
        if answer not in ("n", "no"):
            print("Invalid response; skipping decoding.")
        return

    try:
        decoded = decode_line_code(scheme_name, encoded)

        print("\n--- Decoding Results ---")
        print("Encoded levels:", encoded)
        print("Decoded bitstream:", bits_to_string(decoded))

        print(
            "Decoded stream matches original:",
            decoded == getattr(decode_prompt, "_original_bits", []),
        )

    except (ValueError, TypeError) as error:
        print("Decoding error:", error)


def decode_received_signal():
    """
    Decode manually supplied signal levels.
    The original bitstream is not requested or used.
    """

    schemes = [
        "NRZ-L",
        "NRZ-I",
        "Manchester",
        "Differential Manchester",
        "AMI",
        "B8ZS",
        "HDB3",
    ]

    print("\n--- Decode a Received Signal ---")

    for index, scheme in enumerate(schemes, start=1):
        print(f"{index}. {scheme}")

    choice = input("Choose a coding scheme (1-7): ").strip()

    if not choice.isdigit() or not 1 <= int(choice) <= len(schemes):
        print("Invalid choice.")
        return

    scheme_name = schemes[int(choice) - 1]

    raw = input(
        "Enter encoded signal levels separated by spaces "
        "(-1, 0, 1): "
    ).strip()

    try:
        encoded = [int(value) for value in raw.split()]

        if not encoded:
            raise ValueError("Signal cannot be empty.")

        if any(level not in (-1, 0, 1) for level in encoded):
            raise ValueError("Levels must be -1, 0, or 1.")

        decoded = decode_line_code(scheme_name, encoded)

        print("\n--- Decoding Results ---")
        print("Scheme:", scheme_name)
        print("Encoded levels:", encoded)
        print("Decoded bitstream:", bits_to_string(decoded))

        palindrome = longest_palindrome(decoded)
        print("Longest palindrome:", bits_to_string(palindrome))

    except (ValueError, TypeError) as error:
        print("Decoding error:", error)


# ---------------------------------------------------------
# Line coding
# ---------------------------------------------------------



def line_coding_menu(bits=None):
    schemes = {
        "1": ("NRZ-L", nrz_l),
        "2": ("NRZ-I", nrz_i),
        "3": ("Manchester", manchester),
        "4": ("Differential Manchester", differential_manchester),
        "5": ("AMI", ami),
    }

    print("\n--- Line Coding ---")
    print("1. NRZ-L")
    print("2. NRZ-I")
    print("3. Manchester")
    print("4. Differential Manchester")
    print("5. AMI")

    choice = input("Choose a scheme (1-5): ").strip()

    if choice not in schemes:
        print("Invalid choice.")
        return

    try:
        if bits is None:
            bits = read_bits()

        scheme_name, encoder = schemes[choice]

        if scheme_name == "AMI":
            scramble_choice = input(
                "Do you want scrambling? (y/n): "
            ).strip().lower()

            if scramble_choice in ("y", "yes"):
                print("\n--- Scrambling Schemes ---")
                print("1. B8ZS")
                print("2. HDB3")

                scramble_type = input(
                    "Choose a scrambling scheme (1-2): "
                ).strip()

                if scramble_type == "1":
                    scheme_name = "B8ZS"
                    encoder = b8zs
                elif scramble_type == "2":
                    scheme_name = "HDB3"
                    encoder = hdb3
                else:
                    print("Invalid scrambling choice.")
                    return

            elif scramble_choice not in ("n", "no"):
                print("Invalid choice. Enter y or n.")
                return

        encoded = encoder(bits)

        print("\nOriginal bits:", bits_to_string(bits))
        print("Coding scheme:", scheme_name)
        print("Encoded levels:", encoded)

        plot_line_code(bits, encoded, scheme_name)

        # Ask whether the user wants to decode the encoded signal.
        decode_prompt(scheme_name, encoded)

    except (ValueError, TypeError) as error:
        print("Input error:", error)



# ---------------------------------------------------------
# Digital input workflow
# ---------------------------------------------------------

def digital_input_workflow():
    print("\n--- Digital Input ---")
    print("1. Generate digital data")
    print("2. Enter a binary stream")

    choice = input("Choose an option (1-2): ").strip()

    try:
        if choice == "1":
            bits = generate_data()
            if bits is None:
                return

        elif choice == "2":
            bits = read_bits()
            palindrome = longest_palindrome(bits)

            print("\nDigital stream:", bits_to_string(bits))
            print("Longest palindrome:", bits_to_string(palindrome))
            print("Palindrome length:", len(palindrome))

        else:
            print("Invalid choice.")
            return

        line_coding_menu(bits)

    except ValueError as error:
        print("Input error:", error)


# ---------------------------------------------------------
# Analog input and PCM
# ---------------------------------------------------------

def analog_input_workflow():
    print("\n--- Analog Input: PCM ---")

    try:
        num_samples = int(input("Enter number of samples (e.g. 32): "))
        frequency = float(input("Enter signal frequency in Hz (e.g. 2): "))
        duration = float(input("Enter signal duration in seconds (e.g. 1): "))
        bits_per_sample = int(input("Enter bits per sample (e.g. 3): "))

        if num_samples < 2:
            raise ValueError("Number of samples must be at least 2.")

        if frequency <= 0 or duration <= 0:
            raise ValueError("Frequency and duration must be positive.")

        if not 1 <= bits_per_sample <= 8:
            raise ValueError("Bits per sample must be between 1 and 8.")

        (
            sample_times,
            samples,
            continuous_times,
            continuous_signal,
        ) = generate_analog_signal(
            num_samples=num_samples,
            frequency=frequency,
            duration=duration,
        )

        bitstream, indices, quantized = pcm_encode(
            samples,
            bits_per_sample,
        )

        decoded_indices, decoded_samples = pcm_decode(
            bitstream,
            bits_per_sample,
        )

        print("\n--- PCM Results ---")
        print("Number of samples:", len(samples))
        print("Bits per sample:", bits_per_sample)
        print("Total PCM bits:", len(bitstream))
        print("PCM bitstream:", bits_to_string(bitstream))
        print("Quantization indices:", indices.tolist())
        print("Decoded indices:", decoded_indices.tolist())

        plot_pcm(
            sample_times,
            samples,
            continuous_times,
            continuous_signal,
            decoded_samples,
        )

        choice = input(
            "\nPass PCM-generated bits to line coding? (y/n): "
        ).strip().lower()

        if choice in ("y", "yes"):
            line_coding_menu(bitstream)
        elif choice not in ("n", "no"):
            print("Invalid choice; returning to the main menu.")

    except (ValueError, TypeError) as error:
        print("Input error:", error)


# ---------------------------------------------------------
# Main application
# ---------------------------------------------------------

def main():
    while True:
        print("\n=== Digital Signal Encoder and Decoder ===")
        print("1. Digital input")
        print("2. Analog input (PCM)")
        print("3. Decode a received encoded signal")
        print("4. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            digital_input_workflow()

        elif choice == "2":
            analog_input_workflow()

        elif choice == "3":
            decode_received_signal()

        elif choice == "4":
            print("Exiting program.")
            break

        else:
            print("Invalid choice. Please select 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
