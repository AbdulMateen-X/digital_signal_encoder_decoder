
import random


def generate_random_bits(length):
    """Generate a completely random binary sequence."""
    if length <= 0:
        raise ValueError("Length must be positive.")

    return [random.randint(0, 1) for _ in range(length)]


def generate_fixed_zero_bits(length, zero_run=4):
    """Generate random bits containing four or eight consecutive zeros."""
    if zero_run not in (4, 8):
        raise ValueError("Zero run must be either 4 or 8.")

    if length < zero_run:
        raise ValueError(
            f"Length must be at least {zero_run} bits."
        )

    bits = generate_random_bits(length)

    # Choose a random position where the required zeros will be inserted.
    start = random.randint(0, length - zero_run)
    bits[start:start + zero_run] = [0] * zero_run

    return bits


def bits_to_string(bits):
    """Convert a list of bits into a readable binary string."""
    return "".join(str(bit) for bit in bits)


def longest_palindrome(bits):
    """
    Find the longest palindromic substring using Manacher's algorithm.
    Time complexity: O(n).
    """
    if not bits:
        return []

    sequence = bits_to_string(bits)

    # Insert separators so odd- and even-length palindromes
    # can be handled by the same algorithm.
    transformed = "^#" + "#".join(sequence) + "#$"

    radius = [0] * len(transformed)
    center = 0
    right = 0

    best_center = 0
    best_length = 0

    for i in range(1, len(transformed) - 1):
        mirror = 2 * center - i

        if i < right:
            radius[i] = min(right - i, radius[mirror])

        while (
            transformed[i + 1 + radius[i]]
            == transformed[i - 1 - radius[i]]
        ):
            radius[i] += 1

        if i + radius[i] > right:
            center = i
            right = i + radius[i]

        if radius[i] > best_length:
            best_length = radius[i]
            best_center = i

    # Convert the transformed-string position to the original string.
    start = (best_center - best_length) // 2
    palindrome = sequence[start:start + best_length]

    return [int(bit) for bit in palindrome]
