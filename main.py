
from digital_data import (
    generate_random_bits,
    generate_fixed_zero_bits,
    bits_to_string,
    longest_palindrome,
)


def generate_data():
    print("\n--- Digital Data Generator ---")
    print("1. Completely random binary data")
    print("2. Random data containing four consecutive zeros")
    print("3. Random data containing eight consecutive zeros")

    choice = input("Choose an option (1-3): ").strip()

    if choice not in ("1", "2", "3"):
        print("Invalid choice. Please select 1, 2, or 3.")
        return

    try:
        length = int(input("Enter the number of bits: "))

        if length <= 0:
            print("Length must be positive.")
            return

        if choice == "1":
            bits = generate_random_bits(length)
        elif choice == "2":
            bits = generate_fixed_zero_bits(length, 4)
        else:
            bits = generate_fixed_zero_bits(length, 8)

        palindrome = longest_palindrome(bits)

        print("\n--- Results ---")
        print("Generated digital data:")
        print(bits_to_string(bits))

        print("\nLongest palindromic substring:")
        print(bits_to_string(palindrome))

        print("Palindrome length:", len(palindrome))
        print("Total number of bits:", len(bits))

    except ValueError as error:
        print("Input error:", error)


def main():
    while True:
        print("\n=== Digital Signal Encoder and Decoder ===")
        print("1. Generate digital data")
        print("2. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            generate_data()
        elif choice == "2":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
