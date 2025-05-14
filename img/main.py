import os
import heapq
from tkinter import Tk, Button, Label, filedialog, messagebox

# --- File Handling Functions ---
def read_image_bit_string(path):
    with open(path, 'rb') as image:
        bit_string = ""
        byte = image.read(1)
        while len(byte) > 0:
            byte = ord(byte)
            bits = bin(byte)[2:].rjust(8, '0')
            bit_string += bits
            byte = image.read(1)
    return bit_string

def write_image(bit_string, path):
    abs_path = os.path.join(os.path.dirname(__file__), path)  # Lưu trong thư mục cùng với file mã nguồn
    os.makedirs(os.path.dirname(abs_path), exist_ok=True)
    with open(abs_path, 'wb') as image:
        for i in range(0, len(bit_string), 8):
            byte = bit_string[i:i + 8]
            image.write(bytes([int(byte, 2)]))

# --- Huffman Coding Functions ---
class Node:
    def __init__(self, frequency, symbol, left=None, right=None):
        self.frequency = frequency
        self.symbol = symbol
        self.left = left
        self.right = right
        self.huffman_direction = ''

    def __lt__(self, nxt):
        return self.frequency < nxt.frequency

huffman_codes = {}

def calculate_huffman_codes(node, code=''):
    code += node.huffman_direction
    if node.left:
        calculate_huffman_codes(node.left, code)
    if node.right:
        calculate_huffman_codes(node.right, code)
    if not node.left and not node.right:
        huffman_codes[node.symbol] = code
    return huffman_codes

def get_merged_huffman_tree(byte_to_frequency):
    huffman_tree = []
    for byte, frequency in byte_to_frequency.items():
        heapq.heappush(huffman_tree, Node(frequency, byte))
    while len(huffman_tree) > 1:
        left = heapq.heappop(huffman_tree)
        right = heapq.heappop(huffman_tree)
        left.huffman_direction = "0"
        right.huffman_direction = "1"
        merged_node = Node(left.frequency + right.frequency, left.symbol + right.symbol, left, right)
        heapq.heappush(huffman_tree, merged_node)
    return huffman_tree[0]

def get_frequency(image_bit_string):
    byte_to_frequency = {}
    for i in range(0, len(image_bit_string), 8):
        byte = image_bit_string[i:i + 8]
        if byte not in byte_to_frequency:
            byte_to_frequency[byte] = 0
        byte_to_frequency[byte] += 1
    return byte_to_frequency

def compress(image_bit_string):
    byte_to_frequency = get_frequency(image_bit_string)
    merged_huffman_tree = get_merged_huffman_tree(byte_to_frequency)
    calculate_huffman_codes(merged_huffman_tree)
    write_huffman_tree(merged_huffman_tree, "huffman_tree.txt")  # Lưu cây Huffman vào file
    return get_compressed_image(image_bit_string)

def get_compressed_image(image_bit_string):
    compressed_image_bit_string = ""
    for i in range(0, len(image_bit_string), 8):
        byte = image_bit_string[i:i + 8]
        compressed_image_bit_string += huffman_codes[byte]
    return compressed_image_bit_string

def decompress(compressed_image_bit_string):
    decompressed_image_bit_string = ""
    current_code = ""
    for bit in compressed_image_bit_string:
        current_code += bit
        for byte, code in huffman_codes.items():
            if current_code == code:
                decompressed_image_bit_string += byte
                current_code = ""
    return decompressed_image_bit_string

# --- Writing Huffman Tree in Hierarchical Format ---
def write_huffman_tree(tree_root, path):
    def serialize(node, level=0):
        if node is None:
            return ""
        # Tạo chuỗi cho mỗi nút với mức độ thụt lề
        result = f"{' ' * 2 * level}({node.frequency})\n"
        if node.left:
            result += f"{' ' * 2 * level}├── {node.symbol if node.symbol else 'Left'}\n"
            result += serialize(node.left, level + 1)
        if node.right:
            result += f"{' ' * 2 * level}└── {node.symbol if node.symbol else 'Right'}\n"
            result += serialize(node.right, level + 1)
        return result

    abs_path = os.path.join(os.path.dirname(__file__), path)  # Lưu trong thư mục hiện tại
    os.makedirs(os.path.dirname(abs_path), exist_ok=True)
    with open(abs_path, 'w', encoding='utf-8') as f:  # Mở file với mã hóa utf-8
        f.write(serialize(tree_root))

def write_full_byte_mapping(image_bit_string, huffman_codes, path="byte_full_mapping.txt"):
    # Tạo ánh xạ byte gốc -> chuỗi nhị phân
    byte_to_binary = {}
    for i in range(0, len(image_bit_string), 8):
        byte = image_bit_string[i:i + 8]
        byte_value = int(byte, 2)
        byte_repr = repr(bytes([byte_value]))  # dạng b'\xA0'
        byte_to_binary[byte_repr] = byte

    # Lưu vào file với cấu trúc 'byte -> binary -> huffman_code'
    abs_path = os.path.join(os.path.dirname(__file__), path)
    os.makedirs(os.path.dirname(abs_path), exist_ok=True)
    with open(abs_path, 'w', encoding='utf-8') as f:
        for byte_repr, binary_str in byte_to_binary.items():
            huffman_code = huffman_codes.get(binary_str, "N/A")  # Nếu không có mã Huffman thì ghi "N/A"
            f.write(f"{byte_repr} -> {binary_str} -> {huffman_code}\n")


# --- GUI Functions ---
def compress_action():
    image_path = filedialog.askopenfilename(title="Chọn ảnh để mã hóa")
    if not image_path:
        return
    image_bit_string = read_image_bit_string(image_path)
    compressed_bit_string = compress(image_bit_string)

    # Ghi ánh xạ byte -> chuỗi nhị phân -> mã Huffman
    write_full_byte_mapping(image_bit_string, huffman_codes)

    save_path = filedialog.asksaveasfilename(
        defaultextension=".bin",
        filetypes=[("Binary Files", "*.bin")],
        title="Lưu file nén"
    )
    if not save_path:
        return
    write_image(compressed_bit_string, save_path)
    messagebox.showinfo("Thành công", f"Mã hóa thành công!\nTỉ lệ nén: {len(image_bit_string) / len(compressed_bit_string):.2f}")

def decompress_action():
    compressed_path = filedialog.askopenfilename(title="Chọn file nén")
    if not compressed_path:
        return
    compressed_bit_string = read_image_bit_string(compressed_path)
    decompressed_bit_string = decompress(compressed_bit_string)

    save_path = filedialog.asksaveasfilename(
        defaultextension=".jpg",
        filetypes=[("JPEG Image", "*.jpg"), ("All Files", "*.*")],
        title="Lưu ảnh sau giải mã"
    )
    if not save_path:
        return
    write_image(decompressed_bit_string, save_path)
    messagebox.showinfo("Thành công", "Giải mã thành công!")

# --- Main GUI ---
root = Tk()
root.title("Huffman Image Compressor")
root.geometry("300x150")

Label(root, text="Chương trình nén ảnh bằng mã Huffman", pady=10).pack()

Button(root, text="Mã hóa ảnh", width=20, command=compress_action).pack(pady=5)
Button(root, text="Giải mã ảnh", width=20, command=decompress_action).pack(pady=5)

root.mainloop()
