import pickle
import os
from utils.huffman import (
    build_huffman_tree, build_code_table,
    encode_data, pad_encoded_data, decode_data
)

def compress_image(input_path):
    """
    Nén file ảnh sử dụng thuật toán Huffman.
    
    Args:
        input_path (str): Đường dẫn đến file ảnh đầu vào.
    
    Returns:
        tuple: (padded_bytes, codebook, stats)
            - padded_bytes: Dữ liệu đã nén (bytes).
            - codebook: Bảng mã Huffman.
            - stats: Thống kê về kích thước gốc, kích thước nén và tỉ lệ nén.
    """
    # Đọc dữ liệu ảnh từ file
    with open(input_path, 'rb') as f:
        image_data = f.read()

    # Tạo bảng tần suất
    freq_table = {}
    for byte in image_data:
        freq_table[byte] = freq_table.get(byte, 0) + 1

    # Xây dựng cây Huffman và bảng mã
    tree = build_huffman_tree(image_data)
    codebook = build_code_table(tree)
    encoded = encode_data(image_data, codebook)
    padded_bytes = pad_encoded_data(encoded)

    # Tạo tên file đầu ra với đuôi .image.huff
    base_name = os.path.splitext(input_path)[0]  # Lấy tên file không có đuôi
    output_path = base_name + ".image.huff"
    
    # Lưu cây Huffman và dữ liệu mã hóa
    with open(output_path + ".tree", 'wb') as out:
        pickle.dump(tree, out)
    with open(output_path, 'wb') as out:
        out.write(padded_bytes)

    # Tính toán thống kê
    stats = {
        "Kích thước gốc (bytes)": len(image_data),
        "Kích thước nén (bytes)": len(padded_bytes),
        "Tỉ lệ nén (%)": round(100 * len(padded_bytes) / len(image_data), 2) if len(image_data) > 0 else 0
    }
    return padded_bytes, codebook, stats

def decompress_image(input_path, output_path=None):
    """
    Giải nén file ảnh từ định dạng .image.huff.
    
    Args:
        input_path (str): Đường dẫn đến file .image.huff đã nén.
        output_path (str, optional): Đường dẫn đến file ảnh giải nén. Nếu không cung cấp,
                                    sẽ tự động tạo tên file với đuôi _decompressed.
    
    Returns:
        str: Đường dẫn đến file ảnh đã giải nén.
    """
    # Đọc cây Huffman và dữ liệu mã hóa
    with open(input_path + ".tree", 'rb') as f:
        tree = pickle.load(f)
    with open(input_path, 'rb') as f:
        byte_data = f.read()

    # Chuyển dữ liệu byte thành chuỗi bit
    bit_str = ''.join(f"{byte:08b}" for byte in byte_data)
    padding_len = int(bit_str[:8], 2)
    bit_str = bit_str[8:-padding_len] if padding_len > 0 else bit_str[8:]

    # Giải mã dữ liệu
    decoded_bytes = decode_data(bit_str, tree)

    # Tạo tên file đầu ra nếu không được cung cấp
    if output_path is None:
        base_name = os.path.splitext(input_path)[0]  # Lấy tên file không có đuôi .image.huff
        base_name = base_name.replace(".image", "")  # Loại bỏ .image nếu có
        # Giữ nguyên đuôi file gốc (nếu có) hoặc mặc định là .png
        original_ext = os.path.splitext(base_name)[1] or ".png"
        output_path = base_name + "_decompressed" + original_ext

    # Lưu file giải mã
    with open(output_path, 'wb') as out:
        out.write(decoded_bytes)

    return output_path