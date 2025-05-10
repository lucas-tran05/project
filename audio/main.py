import os
import pickle
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from collections import Counter
import heapq

class Node:
    def __init__(self, freq, byte=None, left=None, right=None):
        self.freq = freq
        self.byte = byte
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(data):
    freq = Counter(data)
    heap = [Node(freq=freq[byte], byte=bytes([byte])) for byte in freq]
    heapq.heapify(heap)

    while len(heap) > 1:
        n1 = heapq.heappop(heap)
        n2 = heapq.heappop(heap)
        merged = Node(n1.freq + n2.freq, left=n1, right=n2)
        heapq.heappush(heap, merged)

    return heap[0] if heap else None

def build_code_table(node, prefix="", code_table=None):
    if code_table is None:
        code_table = {}
    if node:
        if node.byte is not None:
            code_table[node.byte] = prefix
        build_code_table(node.left, prefix + "0", code_table)
        build_code_table(node.right, prefix + "1", code_table)
    return code_table

def encode_data(data, code_table):
    return ''.join(code_table[bytes([b])] for b in data)

def pad_encoded_data(encoded_data):
    extra_padding = 8 - len(encoded_data) % 8
    encoded_data += "0" * extra_padding
    padded_info = "{0:08b}".format(extra_padding)
    encoded_data = padded_info + encoded_data
    b = bytearray()
    for i in range(0, len(encoded_data), 8):
        byte = encoded_data[i:i+8]
        b.append(int(byte, 2))
    return bytes(b)

def decode_data(encoded_data, code_table):
    reversed_code_table = {v: k for k, v in code_table.items()}
    current_code = ""
    decoded_bytes = bytearray()

    for bit in encoded_data:
        current_code += bit
        if current_code in reversed_code_table:
            decoded_bytes.extend(reversed_code_table[current_code])
            current_code = ""
    return decoded_bytes

class HuffmanAudioCompressorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Huffman Audio Compressor")
        self.code_table = {}

        self.notebook = ttk.Notebook(root)
        self.tab_info = ttk.Frame(self.notebook)
        self.tab_code = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_info, text='Thông Tin Nén')
        self.notebook.add(self.tab_code, text='Bảng Mã Nhị Phân')
        self.notebook.pack(expand=True, fill='both')

        self.btn_compress = tk.Button(root, text="Nén File Audio", command=self.compress_file, bg="#add8e6")
        self.btn_decompress = tk.Button(root, text="Giải Nén File .huff", command=self.decompress_file, bg="#90ee90")
        self.btn_compress.pack(pady=10)
        self.btn_decompress.pack(pady=10)

        self.text_info = tk.Text(self.tab_info, wrap=tk.WORD, height=15)
        self.text_info.pack(expand=True, fill='both', padx=10, pady=10)

        self.text_code = tk.Text(self.tab_code, wrap=tk.WORD, height=15)
        self.text_code.pack(expand=True, fill='both', padx=10, pady=10)

    def compress_file(self):
        file_path = filedialog.askopenfilename(title="Chọn file audio", filetypes=[("Audio Files", "*.wav *.mp3 *.aac *.flac *.ogg")])
        if not file_path:
            return

        with open(file_path, "rb") as f:
            data = f.read()

        root = build_huffman_tree(data)
        self.code_table = build_code_table(root)
        encoded_data = encode_data(data, self.code_table)
        padded_data = pad_encoded_data(encoded_data)

        output_path = file_path + ".huff"
        with open(output_path, "wb") as f:
            pickle.dump((padded_data, self.code_table), f)

        original_size = len(data)
        compressed_size = len(padded_data)
        ratio = 100 * compressed_size / original_size

        self.text_info.delete('1.0', tk.END)
        self.text_info.insert(tk.END, f"Đã nén thành công!\nFile lưu: {output_path}\n")
        self.text_info.insert(tk.END, f"Dung lượng gốc: {original_size} bytes\n")
        self.text_info.insert(tk.END, f"Dung lượng nén: {compressed_size} bytes\n")
        self.text_info.insert(tk.END, f"Tỉ lệ nén: {ratio:.2f}%\n")

        self.display_code_table()

    def decompress_file(self):
        file_path = filedialog.askopenfilename(title="Chọn file .huff", filetypes=[("Huffman Compressed", "*.huff")])
        if not file_path:
            return

        with open(file_path, "rb") as f:
            padded_data, code_table = pickle.load(f)

        bit_string = ''.join(f"{byte:08b}" for byte in padded_data)
        padding = int(bit_string[:8], 2)
        encoded_data = bit_string[8:-padding]

        decoded_data = decode_data(encoded_data, code_table)

        output_path = file_path.replace(".huff", "_decompressed_audio")
        with open(output_path, "wb") as f:
            f.write(decoded_data)

        self.text_info.delete('1.0', tk.END)
        self.text_info.insert(tk.END, f"Đã giải nén thành công!\nFile lưu: {output_path}\n")

        self.code_table = code_table
        self.display_code_table()

    def display_code_table(self):
        self.text_code.delete('1.0', tk.END)
        self.text_code.insert(tk.END, "Byte\t|\tMã Nhị Phân\n")
        self.text_code.insert(tk.END, "-" * 40 + "\n")
        for byte, code in sorted(self.code_table.items(), key=lambda x: x[1]):
            display_byte = byte.hex()
            self.text_code.insert(tk.END, f"{display_byte}\t|\t{code}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = HuffmanAudioCompressorGUI(root)
    root.mainloop()
