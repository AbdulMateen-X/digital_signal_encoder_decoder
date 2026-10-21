# Digital Signal Encoder and Decoder
**Course:** ITT 036 — Programming Assignment 1  
**Language:** Python

## 1. Objective

To develop a digital signal encoder and decoder supporting digital data generation, line coding, scrambling, Pulse Code Modulation (PCM), and graphical visualization of encoded and reconstructed signals.

## 2. Language and Libraries Used

- **Python 3:** Core implementation and menu-driven user interface.
- **NumPy:** Numerical computation and analog signal sampling.
- **Matplotlib:** Visualization of line-coded signals and PCM staircase reconstruction.
- **pytest:** Automated testing of encoding, decoding, and scrambling functionality.

## 3. Implementation and Features

- **Digital Data Generation (`digital_data.py`):** Generates random binary streams and streams containing four or eight consecutive zeros. Identifies the longest palindromic substring using an efficient algorithm.
- **Line Coding (`line_coding.py`):** Implements NRZ-L, NRZ-I, Manchester, Differential Manchester, and AMI.
- **Scrambling (`scrambling.py`):** Implements B8ZS and HDB3, selected only when the user chooses AMI and enables scrambling.
- **PCM (`pcm.py`):** Samples and quantizes an analog signal, converts samples into a binary stream, decodes the stream, and plots the reconstructed staircase signal. PCM output can also be passed to a line-coding scheme.
- **Decoding (`decoding.py`):** Recovers digital data from encoded signal levels, including manually supplied levels, without requiring the original bitstream as decoder input.
- **Visualization (`visualization.py`):** Plots encoded waveforms and PCM reconstruction.
- **Main Interface (`main.py`):** Provides menus for digital or analog input, encoding, optional decoding, and scrambling selection.
- **Testing (`test_decoding.py`, `test_cases.py`):** Provides automated tests for decoder round trips, line coding, and scrambling.

## 4. Assumptions

- Digital data consists of binary values 0 and 1.
- Encoded signal levels are represented by -1, 0, and +1.
- Decoders use the initial signal level or pulse polarity assumed by the corresponding encoder.
- PCM uses uniform quantization over the configured amplitude range.
- Manually entered encoded levels must follow the selected coding scheme.

## 5. How to Run

Install dependencies from the project directory:

`pip install -r requirements.txt`

Run the application:

`python main.py`

Run the decoder tests:

`python -m pytest -v test_decoding.py`

Run the component tests:

`python -m pytest -v test_cases.py`

Run both test files:

`python -m pytest -v test_decoding.py test_cases.py`

## 6. References and Acknowledgment

- NumPy documentation: https://numpy.org/doc/
- Matplotlib documentation: https://matplotlib.org/stable/
- pytest documentation: https://docs.pytest.org/

**AI assistance was used during development and debugging.**