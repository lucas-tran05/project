# Project: A data encryption and decryption application using the Huffman algorithm with a graphical user interface.
# To fulfil the requirement of FIT Course by Pham@PTIT
# Tran Quoc Cuong - B23DCAT034 - 13
# Duong Thien Ngan - B23DCAT209 - 13
# Le Van Duy - B23DCAT074 - 13

from audio.compressor import compress_audio, decompress_audio

def compress(file):
    return compress_audio(file)

def decompress(file , output_path=None):
    return decompress_audio(file, output_path)
