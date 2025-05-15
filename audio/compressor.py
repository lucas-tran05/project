import pickle
import os
from utils.huffman import (
    build_huffman_tree, build_code_table,
    encode_data, pad_encoded_data, decode_data
)

def compress_audio_file(path):
    with open(path, "rb") as f:
        data = f.read()

    root = build_huffman_tree(data)
    code_table = build_code_table(root)
    encoded_data = encode_data(data, code_table)
    padded = pad_encoded_data(encoded_data)

    compressed_path = path + ".huff"
    with open(compressed_path, "wb") as f:
        f.write(padded)

    table_path = path + ".huff.table"
    with open(table_path, "wb") as f:
        pickle.dump(code_table, f)

    stats = {
        "Kích thước gốc (byte)": len(data),
        "Kích thước nén (byte)": len(padded),
        "Tỉ lệ nén (%)": round((1 - len(padded) / len(data)) * 100, 2) if len(data) else 0
    }

    return padded, code_table, stats


def decompress_audio_file(path):
    with open(path, "rb") as f:
        padded = f.read()

    table_path = path + ".table"
    with open(table_path, "rb") as f:
        code_table = pickle.load(f)

    bit_str = ''.join(f"{byte:08b}" for byte in padded)
    padding = int(bit_str[:8], 2)
    encoded_data = bit_str[8:-padding]
    decoded_data = decode_data(encoded_data, code_table)

    # Xử lý tên file đầu ra: abc.wav.huff -> abc.wav -> abc_decompress.wav
    if path.endswith(".huff"):
        original_path = path[:-5]  # Bỏ ".huff"
    else:
        original_path = path

    base, ext = os.path.splitext(original_path)
    output_path = f"{base}_decompress{ext}"

    with open(output_path, "wb") as f:
        f.write(decoded_data)

    return output_path
