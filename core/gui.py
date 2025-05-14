# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from modules import audio_module, text_module, image_module

def launch_main_gui():
    class HuffmanApp:
        def __init__(self, root):
            self.root = root
            self.root.title("Huffman Encoder/Decoder")
            self.root.geometry("600x400")

            self.file_path = tk.StringVar()
            self.file_type = tk.StringVar(value="text")

            self.create_widgets()

        def create_widgets(self):
            # File type selector
            type_frame = tk.LabelFrame(self.root, text="Chọn kiểu file")
            type_frame.pack(fill="x", padx=10, pady=10)

            types = [("Text", "text"), ("Image", "image"), ("Audio", "audio")]
            for label, value in types:
                tk.Radiobutton(type_frame, text=label, variable=self.file_type, value=value).pack(side="left", padx=10)

            # File chooser
            file_frame = tk.Frame(self.root)
            file_frame.pack(fill="x", padx=10, pady=5)

            tk.Button(file_frame, text="Chọn File", command=self.choose_file).pack(side="left")
            tk.Entry(file_frame, textvariable=self.file_path, width=50).pack(side="left", padx=10)

            # Action buttons
            btn_frame = tk.Frame(self.root)
            btn_frame.pack(pady=10)

            tk.Button(btn_frame, text="Mã hóa", command=self.encode_file, width=15).pack(side="left", padx=10)
            tk.Button(btn_frame, text="Giải mã", command=self.decode_file, width=15).pack(side="left", padx=10)

            # Huffman table output
            self.code_frame = tk.LabelFrame(self.root, text="Bảng mã Huffman")
            self.code_frame.pack(fill="both", expand=True, padx=10, pady=10)

            self.code_text = tk.Text(self.code_frame)
            self.code_text.pack(fill="both", expand=True)

        def choose_file(self):
            filetype = self.file_type.get()
            if filetype == "text":
                filetypes = [("Text files", "*.txt")]
            elif filetype == "image":
                filetypes = [("Image files", "*.png;*.jpg;*.bmp")]
            elif filetype == "audio":
                filetypes = [("Audio files", "*.wav;*.mp3")]
            else:
                filetypes = [("All files", "*.*")]

            path = filedialog.askopenfilename(filetypes=filetypes)
            if path:
                self.file_path.set(path)

        def encode_file(self):
            path = self.file_path.get()
            if not path:
                messagebox.showerror("Lỗi", "Vui lòng chọn file.")
                return

            filetype = self.file_type.get()
            if filetype == "text":
                bits, code_table = text_module.encode(path)
            elif filetype == "image":
                bits, code_table = image_module.encode(path)
            elif filetype == "audio":
                bits, code_table = audio_module.encode(path)
            else:
                messagebox.showerror("Lỗi", "Loại file không hợp lệ.")
                return

            self.show_code_table(code_table)
            messagebox.showinfo("Xong", "Mã hóa thành công. File .huff đã được lưu.")

        def decode_file(self):
            huff_path = filedialog.askopenfilename(filetypes=[("Huffman Encoded Files", "*.huff")])
            if not huff_path:
                return

            filetype = self.file_type.get()
            if filetype == "text":
                text_module.decode(huff_path)
            elif filetype == "image":
                image_module.decode(huff_path)
            elif filetype == "audio":
                audio_module.decode(huff_path)
            else:
                messagebox.showerror("Lỗi", "Loại file không hợp lệ.")
                return

            messagebox.showinfo("Xong", "Giải mã hoàn tất. File gốc đã được khôi phục.")

        def show_code_table(self, code_table):
            self.code_text.delete("1.0", tk.END)
            for k, v in code_table.items():
                self.code_text.insert(tk.END, f"{repr(k)}: {v}\n")

    root = tk.Tk()
    app = HuffmanApp(root)
    root.mainloop()
