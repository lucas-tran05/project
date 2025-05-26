# -*- coding: utf-8 -*-
# core/gui.py
import tkinter as tk
from tkinter import filedialog
import os
from tkinter import filedialog, messagebox, ttk
from modules import audio_module, text_module, image_module

def launch_main_gui():
    class HuffmanApp:
        def __init__(self, root):
            self.root = root
            self.root.title("Huffman Encoder/Decoder")
            self.root.geometry("500x400")
            self.root.configure(bg="#f2f2f2")

            self.file_path = tk.StringVar()
            self.file_type = tk.StringVar(value="text")

            self.build_interface()

        def build_interface(self):
            header = tk.Label(self.root, text="Hệ Thống Nén & Giải Nén Huffman", font=("Arial", 16, "bold"), fg="#004d99", bg="#f2f2f2")
            header.pack(pady=15)

            type_frame = tk.LabelFrame(self.root, text="Chọn loại file", padx=10, pady=5, bg="#f2f2f2")
            type_frame.pack(fill="x", padx=20, pady=5)

            for text, val in [("Text", "text"), ("Image", "image"), ("Audio", "audio")]:
                tk.Radiobutton(type_frame, text=text, variable=self.file_type, value=val, bg="#f2f2f2", font=("Arial", 10)).pack(side="left", padx=10)

            file_frame = tk.Frame(self.root, bg="#f2f2f2")
            file_frame.pack(fill="x", padx=20, pady=10)

            tk.Button(file_frame, text="Chọn File", command=self.choose_file, bg="#cce6ff", width=15).pack(side="left")
            tk.Entry(file_frame, textvariable=self.file_path, width=60, font=("Arial", 10)).pack(side="left", padx=10)

            btn_frame = tk.Frame(self.root, bg="#f2f2f2")
            btn_frame.pack(pady=10)

            tk.Button(btn_frame, text="Mã hóa", command=self.encode_file, bg="#cce6ff", width=15).pack(side="left", padx=20)
            tk.Button(btn_frame, text="Giải mã", command=self.decode_file, bg="#cce6ff", width=15).pack(side="left", padx=20)

            notebook = ttk.Notebook(self.root)
            notebook.pack(fill="both", expand=True, padx=15, pady=10)

            self.result_tab = tk.Text(notebook, wrap=tk.WORD, font=("Consolas", 11))
            self.codes_tab = tk.Text(notebook, wrap=tk.WORD, font=("Consolas", 11))

            notebook.add(self.result_tab, text="Kết Quả")
            notebook.add(self.codes_tab, text="Bảng Mã Huffman")

        def choose_file(self):
            filetype = self.file_type.get()
            if filetype == "text":
                filetypes = [("Text files", "*.txt *.docx")]
            elif filetype == "image":
                filetypes = [("Image files", "*.png *.jpg *.bmp")]
            elif filetype == "audio":
                filetypes = [("Audio files", "*.mp3")]

            path = filedialog.askopenfilename(filetypes=filetypes)
            if path:
                self.file_path.set(path)

        def encode_file(self):
            path = self.file_path.get()
            if not path:
                messagebox.showerror("Lỗi", "Vui lòng chọn file.")
                return

            filetype = self.file_type.get()
            try:
                if filetype == "text":
                    bits, code_table, stats = text_module.encode(path)
                elif filetype == "image":
                    bits, code_table, stats = image_module.compress(path)
                elif filetype == "audio":
                    bits, code_table, stats = audio_module.compress(path)
                else:
                    messagebox.showerror("Lỗi", "Loại file không hợp lệ.")
                    return

                self.result_tab.delete("1.0", tk.END)
                self.result_tab.insert(tk.END, "✔ Đã nén file thành công!\n\n")
                if stats:
                    for label, value in stats.items():
                        self.result_tab.insert(tk.END, f"{label}: {value}\n")

                self.show_code_table(code_table)
                messagebox.showinfo("Xong", "Mã hóa hoàn tất. File .huff đã được lưu.")
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))

        def decode_file(self):
            filetype = self.file_type.get()
            
            # Định nghĩa filetypes dựa trên loại file được chọn
            if filetype == "text":
                filetypes = [("Huffman Text Files", "*.text.huff")]
            elif filetype == "image":
                filetypes = [("Huffman Image Files", "*.image.huff")]
            elif filetype == "audio":
                filetypes = [("Huffman Audio Files", "*.audio.huff")]
            
            # Mở dialog để chọn file mã hóa Huffman
            huff_path = filedialog.askopenfilename(filetypes=filetypes)
            if not huff_path:
                return

            # Lấy tên file gốc (loại bỏ phần mở rộng .huff, .text.huff, .image.huff, hoặc .audio.huff)
            original_name = os.path.basename(huff_path)
            for ext in [".text.huff", ".image.huff", ".audio.huff", ".huff"]:
                original_name = original_name.replace(ext, "")
            
            # Gợi ý phần mở rộng cho file giải mã
            ext_map = {
                "text": "",
                "image": ".bmp", 
                "audio": ".wav"
            }
            ext = ext_map.get(filetype, "")

            # Gợi ý tên file lưu
            suggested_name = f"DECODE_{original_name}{ext}"

            # Mở dialog để chọn nơi lưu file giải mã
            save_path = filedialog.asksaveasfilename(
                defaultextension=ext,
                filetypes=[(f"{filetype.capitalize()} Files", f"*{ext}"), ("All Files", "*.*")],
                initialfile=suggested_name,
                title="Chọn nơi lưu file giải mã"
            )
            if not save_path:
                return

            try:
                if filetype == "text":
                    out_path = text_module.decode(huff_path, save_path)
                elif filetype == "image":
                    out_path = image_module.decompress(huff_path, save_path)
                elif filetype == "audio":
                    out_path = audio_module.decompress(huff_path, save_path)
                else:
                    messagebox.showerror("Lỗi", "Loại file không hợp lệ.")
                    return

                self.result_tab.delete("1.0", tk.END)
                self.result_tab.insert(tk.END, f"✔ Giải mã thành công!\n📂 File tạo ra: {out_path}")
                messagebox.showinfo("Xong", "Giải mã hoàn tất.")
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))

        def show_code_table(self, code_table):
            self.codes_tab.delete("1.0", tk.END)
            for k, v in code_table.items():
                display_char = k if isinstance(k, str) and k.isprintable() else repr(k)
                self.codes_tab.insert(tk.END, f"{display_char}: {v}\n")

    root = tk.Tk()
    app = HuffmanApp(root)
    root.mainloop()
