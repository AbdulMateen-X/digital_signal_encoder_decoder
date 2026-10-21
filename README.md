# Digital Signal Encoder and Decoder — Specification Report

**Course:** ITT 036 — Programming Assignment 1  
**Language:** Python

## Objective

To implement a digital signal generator, line-coding encoder and decoder, scrambling techniques, and Pulse Code Modulation (PCM) encoder and decoder with graphical signal visualization.

## Technologies and Libraries

- **Python:** Core implementation and command-line interaction.
- **NumPy:** Numerical operations, signal sampling, and PCM processing.
- **Matplotlib:** Visualization of line-coded waveforms and PCM staircase reconstruction.
- **pytest:** Automated testing of encoding, decoding, and component functionality.

## Implementation and Features

1. **Digital Data Generator (`digital_data.py`):** Generates random binary data and sequences containing four or eight consecutive zeros. Finds the longest palindromic substring efficiently.
2. **Line Coding (`line_coding.py`):** Implements NRZ-L, NRZ-I, Manchester, Differential Manchester, and AMI.
3. **Scrambling (`scrambling.py`):** Implements B8ZS and HDB3 for handling long zero sequences in AMI-based transmission.
4. **PCM (`pcm.py`):** Samples and quantizes an analog signal, converts samples into a binary stream, decodes the stream, and plots the reconstructed staircase signal.
5. **Decoding (`decoding.py`):** Reconstructs digital data from encoded signal levels without using the original bitstream as the decoder's input.
6. **Visualization (`visualization.py`):** Displays encoded signal waveforms and PCM signal reconstruction.
7. **Application Interface (`main.py`):** Provides menu-driven digital and analog input workflows, encoding options, and decoding options.
8. **Testing (`test_decoding.py`, `test_cases.py`):** Contains automated tests for decoder functionality, encoding-decoding round trips, and scrambling cases.

## Assumptions

- Digital streams contain only binary values 0 and 1.
- Encoded signal levels are represented by -1, 0, and +1.
- Decoding uses the initial signal level or pulse polarity specified by the implementation.
- PCM uses uniform quantization over the configured signal range.
- Manually entered encoded levels must follow the selected line-coding scheme.

## How to Run

Install dependencies:

`pip install -r requirements.txt`

Run the application:

`python main.py`

Run the automated tests:

`python -m pytest -v test_decoding.py test_cases.py`

## References and Acknowledgment

References: NumPy documentation (https://numpy.org/doc/) and Matplotlib documentation (https://matplotlib.org/stable/).

AI assistance was used during development and debugging.