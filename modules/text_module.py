# Project: A data encryption and decryption application using the Huffman algorithm with a graphical user interface.
# To fulfil the requirement of FIT Course by Pham@PTIT
# Tran Quoc Cuong - B23DCAT034 - 13
# Duong Thien Ngan - B23DCAT209 - 13
# Le Van Duy - B23DCAT074 - 13

from text.compressor import compress_file, decompress_file

def encode(file):
    return compress_file(file)

def decode(file, output_path=None):
    return decompress_file(file, output_path)