# Code for a hashing algo that takes in the ID number of a student, verifies it and returns its hash.

def BHA27(id_input):
    
    import random
    import string
    import math

# The random string approach was abandonded due to the complete random nature of the generated string.  
# In order for BHA_27 to produce a pseudorandom output, it was decided to use hard coded constants instead of a random string.
# The code for random salts is present throughout this file enclosed in tripple brackets.

    '''def generate_random_string(length):
        # Generate a random string of the specified length
        characters = string.ascii_letters + string.digits  # Includes A-Z, a-z, and 0-9
        return ''.join(random.choice(characters) for _ in range(length))'''

    '''size_str = int((padding_size -1 - 13)/2) # Calculate the size of the random strings based on the hash size'''

    '''salt1 = generate_random_string(size_str)  # Generate a random string as salt
    salt2 = generate_random_string(size_str + 1)  # Generate another random string as salt'''
      
    # Loop until the user enters a valid padding size.
    while True:
        padding_size = int(input("Enter size of the hash (8, 16, 24, 32, etc): "))
        if padding_size % 8 == 0 and padding_size < 48:
            break  # Exit the loop if input is valid
        print("Please enter a size that is a multiple of 8 & less than 48. \n")

    print("\nHashing your ID Number...")


    # HARD CODED CONSTANTS: 7TH ROOT OF 2 AND 2ND ROOT OF 7
    CONST1 = 2 ** (1/7) * 7 ** (1/2) 
    CONST2 = 7 ** (1/7) * 2 ** (1/2)

    # Take fractional parts
    FRAC_CONST1 = math.modf(CONST1)[0]
    FRAC_CONST2 = math.modf(CONST2)[0]

    # FIRST 27 BITS OF THE FRACTIONAL PARTS
    C1 = format(int(FRAC_CONST1 * (2 ** 27)), '027b')
    C2 = format(int(FRAC_CONST2 * (2 ** 27)), '027b')
    Padding = str(00000000) # 8 bits of padding to ensure the ID is 32 bits long.



    '''id_padded= salt1 + id_input + salt2 ''' # Concatenate the ID with the salt 
   
    id_padded= C1 + id_input + C2 + Padding # Concatenate the ID with the constants

    #print("\n", "Pre Salt: ", salt1, "\n", "ID: ", id_input, "\n", "Post Salt: ", salt2)
    print("\n", "Pre Salt: ", C1, "\n", "ID: ", id_input, "\n", "Post Salt: ", C2)

    # Convert the concatenated string to bin
    padded_binary = ' '.join(format(x, '08b') for x in bytearray(id_padded, 'utf-8')) 
    print("\nBinary representation of ID & Salt:", padded_binary)

    padded_binary = padded_binary.replace(" ", "") 

    # Split the bin into blocks of 32 bits
    binary_blocks = [padded_binary[i:i+32] for i in range(0, len(padded_binary), 32)]
    print("\nBinary blocks (4 bytes each):")

    # Access individual blocks using their index
    for i, block in enumerate(binary_blocks):
        print(f"B{i + 1}: {block}")
    print("\n")


    # 1. Perform XOR on each block with the bin of the padding size
    padding_binary = format(padding_size, '032b')  # Convert padding size to 32-bit binary

    xor_results = []  # To store XOR results for each block
    for i, block in enumerate(binary_blocks):
        xor_result = int(block, 2) ^ int(padding_binary, 2)  # XOR with the padding size
        xor_result_binary = format(xor_result, '032b')  # Convert the result back to bin
        xor_results.append(xor_result_binary) # Store the results for further calc
        print(f"XOR result of B{i + 1}:", xor_result_binary)
    print("\n")

    # 2. Perform XOR with the bin of 27
    xor_27_results = []  # To store XOR results for each block with 27
    for i, xor_result_binary in enumerate(xor_results):
        xor_with_27 = int(xor_result_binary, 2) ^ int(format(27, '032b'), 2)
        xor_with_27_binary = format(xor_with_27, '032b')  # Convert the result back to binary
        xor_27_results.append(xor_with_27_binary)  # Store the results for further calc
        print(f"XOR (w 27) of B{i + 1} :", xor_with_27_binary)
    print("\n")

    # 3.1 Perform bitwise rotation to the right by 7 bits 
    r_rot_and_results = []  # To store the final results
    for i, xor_with_27_binary in enumerate(xor_results):
        # Rotate right by 7 bits
        r_rot = (int(xor_with_27_binary, 2) >> 7) | ((int(xor_with_27_binary, 2) & 0b1111111) << (32 - 7)) # 0b1111111 is 127 in decimal and is used to isolate the least significant 7 bits and the << operator is used to shift these bits to the left by 32-7 (as to not exceed the 32 bit limit) making them the most significant 7 bits.
        r_rot_bin = format(r_rot & 0xFFFFFFFF, '032b')  # Ensure 32-bit binary representation

        print(f"Right rotation of B{i + 1} by 7 bits:", r_rot_bin)
        r_rot_and_results.append(r_rot_bin) # Store the results for further calc
    print("\n")



    # 3.2 Perform bitwise rotation to the left by 9 bits 
    l_rot_and_results = []  # To store the final results
    for i, xor_with_27_binary in enumerate(xor_results):
        # Rotate left by 9 bits
        l_rot = (int(xor_with_27_binary, 2) << 9) | ((int(xor_with_27_binary, 2) & 0xFFFFFFFF) >> (32 - 7)) #As python does not have a limit on the size of integers, we use 0xFFFFFFFF to ensure that the result does not exceed a 32-bit number. 
        l_rot_bin = format(l_rot, '032b')  # Convert to 32-bit binary

        print(f"Left rotation of B{i + 1} by 9 bits:", l_rot_bin)
        l_rot_and_results.append(l_rot_bin) # Store the results for further calc
    print("\n")


    # Perform addition modulo 2^padding_size of l_rotated and r_rotated
    modulo_add_results = []  # Store the final results
    modulo = 2 ** padding_size  # Calculate 2^padding_size

    for i in range(len(l_rot_and_results)):
        # Convert binary strings to integers
        l_rot_int = int(l_rot_and_results[i], 2)
        r_rot_int = int(r_rot_and_results[i], 2)
        
        
        # Perform addition modulo 2^padding_size
        modulo_add = (l_rot_int + r_rot_int) % modulo
        modulo_add_binary = format(modulo_add, f'0{padding_size}b')  # Convert to binary with padding_size bits
        modulo_add_results.append(modulo_add_binary)

        print(f"Modulo addition result of B{i + 1}:", modulo_add_binary)


    # Concatenate all the modulo addition results to get the final hash.
    final_hash = ''.join(modulo_add_results)

    # Convert the final hash from binary to hexadecimal
    final_hash_hex = hex(int(final_hash, 2))[2:]  # Convert binary to int, then to hex, and remove '0x' prefix
    print("\nFinal hash :", final_hash_hex)


import re

# regex pattern for the ID
pattern1 = r"^20\d{2}(B\dA\d)\d{4}[PGH]$"
pattern2 = r"^20\d{2}(A\dPS)\d{4}[PGH]$"
pattern3 = r"^20\d{2}(B\dPS)\d{4}[PGH]$"

# Validate the ID number

while True:
    id_input = input("Enter your ID Number: ").strip().replace(" ", "").upper()
    print("\nValidating your ID Number...")
    
    if re.match(pattern1, id_input) or re.match(pattern2, id_input) or re.match(pattern3, id_input):
        print(f"Your ID Number is valid. Your BITS ID is: {id_input}\n")
        break
    else:
        print("Your ID Number is invalid. Please enter a valid BITS ID!\n")

BHA27(id_input) # Call the defined function BHA27().