# BHA-27(BITS Hashing Algorithm-27): Custom ID Hashing Algorithm for BITS ID.

BHA-27 is a Python implementation of a custom hashing algorithm for validating and hashing BITS student ID numbers. It includes bit-level transformations, mathematical constants, and modular arithmetic to generate a secure hash based on user-defined hash lengths.

## 🔍 Features
- Validates BITS-style student IDs using regex
- Allows customizable hash size (8, 16, 24, 32 bits, etc.)
- Uses unique salts derived from irrational constants
- Performs binary transformations:
  - XOR operations
  - Bitwise rotations
  - Modulo addition
- Outputs final hash in hexadecimal format

## ⚙️ How It Works

0. ID Verification Via Regex Patterns. 

1. Padding & Conversion: 
    1. Uses hard coded constants for padding.
	  2. Lets the user decide the padding size (32, 64, 128, etc)
	  3. Concatenates String + ID + String.
	  4. Converts the concatenated string to binary.
    5. Splits into blocks of 8 bits

3. Math part (for each block of 8 bits):
    1. XOR the binary string with the binary representation of the size of the hash. 
	  2. XOR the result from step 1 with the binary representation of 27. 
	  3. BITWISE ROTATE the result from step ii) to the right by 7 bits. 
	  4. BITWISE ROTATE the result from step ii) to the left by 9 bits.
    5. Perform Modulo Addition of the results from step iii) and step iv).
