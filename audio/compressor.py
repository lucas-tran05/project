import pickle
import os
from utils.huffman import (
    build_huffman_tree, build_code_table,
    encode_data, pad_encoded_data, decode_data
)

def compress_audio(input_path):
    with open(input_path, 'rb') as f:
        audio_data = f.read()

    freq_table = {}
    for byte in audio_data:
        freq_table[byte] = freq_table.get(byte, 0) + 1

    tree = build_huffman_tree(audio_data)
    codebook = build_code_table(tree)
    encoded = encode_data(audio_data, codebook)
    padded_bytes = pad_encoded_data(encoded)

    # Xóa đuôi .mp3 (nếu có) và thêm .huff
    base_name = os.path.splitext(input_path)[0]  # Lấy tên file không có đuôi
    output_path = base_name + ".huff"
    
    with open(output_path + ".tree", 'wb') as out:
        pickle.dump(tree, out)
    with open(output_path, 'wb') as out:
        out.write(padded_bytes)

    stats = {
        "Kích thước gốc (bytes)": len(audio_data),
        "Kích thước nén (bytes)": len(padded_bytes),
        "Tỉ lệ nén (%)": round(100 * len(padded_bytes) / len(audio_data), 2) if len(audio_data) > 0 else 0
    }
    return padded_bytes, codebook, stats

def decompress_audio(input_path, output_path=None):
    with open(input_path + ".tree", 'rb') as f:
        tree = pickle.load(f)
    with open(input_path, 'rb') as f:
        byte_data = f.read()

    bit_str = ''.join(f"{byte:08b}" for byte in byte_data)
    padding_len = int(bit_str[:8], 2)
    bit_str = bit_str[8:-padding_len] if padding_len > 0 else bit_str[8:]

    decoded_bytes = decode_data(bit_str, tree)

    if output_path is None:
        # Xóa đuôi .huff và thêm _decompressed
        base_name = os.path.splitext(input_path)[0]
        output_path = base_name + "_decompressed"

    with open(output_path, 'wb') as out:
        out.write(decoded_bytes)

    return output_path