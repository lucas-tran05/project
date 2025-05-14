import pickle
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

    return compressed_path, table_path, len(data), len(padded), code_table

def decompress_audio_file(path):
    # Đọc dữ liệu nén từ .huff
    with open(path, "rb") as f:
        padded = f.read()

    # Đọc bảng mã từ .huff.table
    table_path = path + ".table"
    with open(table_path, "rb") as f:
        code_table = pickle.load(f)

    bit_str = ''.join(f"{byte:08b}" for byte in padded)
    padding = int(bit_str[:8], 2)
    encoded_data = bit_str[8:-padding]
    decoded_data = decode_data(encoded_data, code_table)

    output_path = path.replace(".huff", "_decompressed_audio")
    with open(output_path, "wb") as f:
        f.write(decoded_data)

    return output_path, code_table
