# imports
import os , heapq
from collections import defaultdict
from bitstring import BitArray


# Global variables
dic_char_codes = {}
frequency = defaultdict(int)



# GIT HUB link : https://github.com/AbelhaJR/Huffman

# Functions 


# 1 - Read File
def read_file(file_path : str)-> str:
    """Allow the python script reading the text file , 
    removing all paragraphs and changing spaces by '-'."""
    with open(file_path,"r",encoding="utf-8") as text_file :
       return text_file.read()


# 2 - Huffman Coding
def huffman_coding(file_text : str)->list:
    """Uses the Huffman Coding technique to compress data ,
    allowing size reduction without losing anything."""


    # Import the frequency default dictionary
    global frequency
    for character in file_text :
        frequency[character] += 1
    
    heap = [[frequency, [letter, '']] for letter, frequency in frequency.items()]
    
    heapq.heapify(heap) # Push the smallest ( the smallest element is the one with the lowest frequency) to index 0
    while len(heap) > 1:

        # Removes the smallest item that stays at index 0
        first_small_element = heapq.heappop(heap)
        second_small_element = heapq.heappop(heap)
       
        # Add 0 or 1 to the number of bits
        for pair in first_small_element[1:]:
            pair[1] = '0' + pair[1]
        # Add 0 or 1 to the number of bits
        for pair in second_small_element[1:]:
            pair[1] = '1' + pair[1]
        
        
        
        heapq.heappush(heap, [first_small_element[0] + second_small_element[0]] + first_small_element[1:] + second_small_element[1:])
    # Return the iterable in sorted order , in this case we use lambda because if we didnt use it we would have to create a separate function for that .
    return sorted(heapq.heappop(heap)[1:], key=lambda element: (len(element[-1]), element))



# 3 - Encoding
def encoded_bits_text(huffman_coding : list , file_text : str ) -> str:
    """Allow to encode the huffman tree refering to the characters and bit code."""

    # Import global variables dic_char_codes
    global dic_char_codes


    for pair in huffman_coding :
        dic_char_codes[pair[0]] = pair[1]
    
    # Return a translation table that maps each character
    table = file_text.maketrans(dic_char_codes) 

    return file_text.translate(table)


# 4 - Padding encoding
def pad_encoded_text(encoded_bits_text : str) -> str:
    """Allow to add the ammount of zeros to beggiining the if the overall lenght of final encoded is not multiple of 8 (8-bit)."""
    padding = 8-(len(encoded_bits_text)%8)

    text = encoded_bits_text.ljust(len(encoded_bits_text)+padding,'0')

    padded_data = "{0:08b}".format(padding)

    encoded = padded_data + text

    return encoded

# 5 - compressed file
def compressed_file(file_path : str)-> str:
    """Allow to compress a specific file by using helper functions that are in the python script."""
    file_text = read_file(file_path)


    # Get the file name split -> [0] = file_name / [1] = file_extension
    file_name = os.path.splitext(file_path)[0]
  
    # Create the new file -> file_name + file_extension
    file_details = file_name + ".bin"
   
    bit_code_unique_character = encoded_bits_text(huffman_coding(file_text),file_text)

    padding_bit_code_unique_character = pad_encoded_text(bit_code_unique_character)

    # Transform String of corresponding bit codes to a BitArray by using the library bitString
    bit = BitArray(bin=padding_bit_code_unique_character)

    # We use the parameter 'wb' -> w = write , b = bit
    with open(file_details,'wb') as compressed_file :
        bit.tofile(compressed_file)
    
    return file_details


# 6 - Decompress file
def decompress_file(compressed_file_path : str)->str :
    """Allow to decompressed a specific file by using helper functions that are in the python script."""

    # Get the file name split -> [0] = file_name / [1] = file_extension
    file_name = os.path.splitext(compressed_file_path)[0]

    # Create the new file -> file_name + file_extension
    file_details = file_name+ "_after.txt"


     # We use the parameter 'rb' -> r = read , b = bit
    with open(compressed_file_path,'rb') as compressed_file:
        bit_string = ""
        byte = compressed_file.read(1)

        while(len(byte) > 0):

            byte = ord(byte)

            bits = bin(byte)[2:].rjust(8,'0')
            
            # Add bits to the bit_string
            bit_string += bits

            byte =compressed_file.read(1)
        # Initially to encode we use padding to add in case of need zeros to the initially code (8-bit) , so now is necessary to remove it
        encoded_text = remove_paddding(bit_string)

        decoded_text = decode_text(encoded_text)
    with open(file_details ,'w',encoding='utf-8') as output :
        output.write(decoded_text)
    return file_details

# 7 - Remove padding
def remove_paddding(bit_string : str) -> str :
    """Allow to remove the extra padding adding in the encode."""

    # String Slice to remove the first 8 characters
    padded_info = bit_string[:8]
    extra_padding = int(padded_info,2)

    bit_string = bit_string[8:]

    encoded_text = bit_string[:-1*extra_padding]

    return encoded_text

# 8 - Deconding
def decode_text(encoded_text : str) -> str :
    """Allow to decode the compressed file containing the bit code for every single character in the original file."""
    global dic_char_codes

    current_code = ""
    decoded_text = ""

    # We reverse the dictionary to be easier acessing the keys with the bit code
    chars_and_codes_reverse= dict((y, x) for x, y in dic_char_codes.items())

    for bit in encoded_text:
        current_code+=bit
        if(current_code in chars_and_codes_reverse):
            char=chars_and_codes_reverse[current_code]
            decoded_text+=char
            current_code=""

    return decoded_text

# 9 - Script
def run_script():
    """Allow to execute both compression and decompression."""
    file_path = str(input("Insert File Path :"))
    compressed = compressed_file(file_path)
    decompress = decompress_file(compressed)

run_script()




