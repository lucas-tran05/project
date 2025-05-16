from text.compressor import compress_file, decompress_file

def encode(file):
    return compress_file(file)

def decode(file, output_path=None):
    return decompress_file(file, output_path)