import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os, heapq, pickle
from collections import defaultdict

class HuffmanNode:
    def __init__(self, char=None, freq=0):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
    def __lt__(self, other):
        return self.freq < other.freq

def build_frequency_table(text):
    freq = defaultdict(int)
    for char in text:
        freq[char] += 1
    return freq

def build_huffman_tree(frequency):
    heap = [HuffmanNode(c, f) for c, f in frequency.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        a, b = heapq.heappop(heap), heapq.heappop(heap)
        merged = HuffmanNode(freq=a.freq + b.freq)
        merged.left, merged.right = a, b
        heapq.heappush(heap, merged)
    return heap[0]

def generate_codes(node, prefix='', codebook=None):
    if codebook is None: codebook = {}
    if node.char: codebook[node.char] = prefix
    if node.left: generate_codes(node.left, prefix + '0', codebook)
    if node.right: generate_codes(node.right, prefix + '1', codebook)
    return codebook

def encode_text(text, codebook):
    return ''.join(codebook[c] for c in text)

def pad_encoded_text(encoded_text):
    extra = 8 - len(encoded_text) % 8
    return f"{extra:08b}" + encoded_text + '0' * extra

def get_byte_array(padded_encoded_text):
    return bytearray(int(padded_encoded_text[i:i+8], 2) for i in range(0, len(padded_encoded_text), 8))

def remove_padding(padded_text):
    pad_len = int(padded_text[:8], 2)
    return padded_text[8:-pad_len]

def decode_text(bits, tree):
    decoded, node = '', tree
    for bit in bits:
        node = node.left if bit == '0' else node.right
        if node.char:
            decoded += node.char
            node = tree
    return decoded

class HuffmanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Huffman Compression GUI")
        self.root.geometry("1000x700")
        self.tree = None
        self.codebook = {}

        self.build_interface()

    def build_interface(self):
        # Header
        header = tk.Label(self.root, text="Huffman Text Compressor", font=("Arial", 20, "bold"), fg="#004d99")
        header.pack(pady=10)

        # Control Frame
        ctrl_frame = tk.Frame(self.root)
        ctrl_frame.pack(pady=5)

        tk.Button(ctrl_frame, text="Nén File Văn Bản", command=self.compress_file, width=20, bg="#b3e0ff").pack(side=tk.LEFT, padx=10)
        tk.Button(ctrl_frame, text="Giải Nén File .huff", command=self.decompress_file, width=20, bg="#b3ffd9").pack(side=tk.LEFT, padx=10)

        # Output Frame with Tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, pady=10)

        self.result_tab = tk.Text(notebook, wrap=tk.WORD)
        self.codes_tab = tk.Text(notebook, wrap=tk.WORD)
        self.tree_tab = tk.Text(notebook, wrap=tk.WORD)

        notebook.add(self.result_tab, text="📊 Thông Tin Nén")
        notebook.add(self.codes_tab, text="💡 Bảng Mã Nhị Phân")
        notebook.add(self.tree_tab, text="🌳 Cây Huffman")

    def display_tree(self, node, prefix="", is_left=True):
        if node is None:
            return ""
        label = f"'{node.char}'" if node.char else "•"
        line = f"{prefix}{'├── ' if is_left else '└── '}{label} ({node.freq})\n"
        new_prefix = prefix + ("│   " if is_left else "    ")
        return (line +
                self.display_tree(node.left, new_prefix, True) +
                self.display_tree(node.right, new_prefix, False))

    def compress_file(self):
        path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt *.docx")])
        if not path:
            return

        try:
            if path.endswith(".docx"):
                try:
                    import docx
                except ImportError:
                    messagebox.showerror("Thiếu thư viện",
                                         "Chưa cài thư viện 'python-docx'.\nHãy chạy lệnh:\npip install python-docx")
                    return
                doc = docx.Document(path)
                text = "\n".join([para.text for para in doc.paragraphs])
            else:
                with open(path, 'r', encoding='utf-8') as f:
                    text = f.read()

            freq = build_frequency_table(text)
            self.tree = build_huffman_tree(freq)
            self.codebook = generate_codes(self.tree)

            encoded = encode_text(text, self.codebook)
            padded = pad_encoded_text(encoded)
            byte_data = get_byte_array(padded)

            out_path = path + ".huff"
            with open(out_path, 'wb') as out:
                pickle.dump((self.tree, byte_data), out)

            original_size = os.path.getsize(path)
            compressed_size = os.path.getsize(out_path)
            ratio = 100 * (1 - compressed_size / original_size)

            self.result_tab.delete('1.0', tk.END)
            self.result_tab.insert(tk.END, f"✔ Đã nén thành công!\n")
            self.result_tab.insert(tk.END, f"🗃 File lưu: {out_path}\n")
            self.result_tab.insert(tk.END, f"💾 Dung lượng gốc: {original_size} bytes\n")
            self.result_tab.insert(tk.END, f"📉 Dung lượng nén: {compressed_size} bytes\n")
            self.result_tab.insert(tk.END, f"📊 Tỉ lệ nén: {ratio:.2f}%\n")

            self.codes_tab.delete('1.0', tk.END)
            for k in sorted(self.codebook):
                display_char = k if k.isprintable() else repr(k)
                self.codes_tab.insert(tk.END, f"'{display_char}': {self.codebook[k]}\n")

            self.tree_tab.delete('1.0', tk.END)
            self.tree_tab.insert(tk.END, self.display_tree(self.tree))

        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def decompress_file(self):
        path = filedialog.askopenfilename(filetypes=[("Huffman files", "*.huff")])
        if not path:
            return

        try:
            with open(path, 'rb') as f:
                tree, byte_data = pickle.load(f)

            bit_str = ''.join(f"{byte:08b}" for byte in byte_data)
            encoded = remove_padding(bit_str)
            decoded = decode_text(encoded, tree)

            out_path = path.replace(".huff", "_decoded.txt")
            with open(out_path, 'w', encoding='utf-8') as out:
                out.write(decoded)

            self.result_tab.delete('1.0', tk.END)
            self.result_tab.insert(tk.END, "✔ Đã giải nén thành công!\n")
            self.result_tab.insert(tk.END, f"🗃 File tạo ra: {out_path}\n")

        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = HuffmanApp(root)
    root.mainloop()
