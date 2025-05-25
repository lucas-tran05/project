from audio.compressor import compress_audio, decompress_audio

def compress(file):
    return compress_audio(file)

def decompress(file , output_path=None):
    return decompress_audio(file, output_path)
