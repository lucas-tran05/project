from img.image import compress_image, decompress_image

def compress(file):
    return compress_image(file)

def decompress(file, output_path=None):
    return decompress_image(file, output_path)
