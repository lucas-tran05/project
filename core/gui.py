# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from modules import audio_module, text_module, image_module

def launch_main_gui():
    class HuffmanApp:
        def __init__(self, root):
            self.root = root
            self.root.title("Huffman Encoder/Decoder")
            self.root.geometry("700x500")
            self.root.configure(bg="#f2f2f2")

            self.file_path = tk.StringVar()
            self.file_type = tk.StringVar(value="text")

            self.build_interface()

        def build_interface(self):
            header = tk.Label(self.root, text="Hệ Thống Nén & Giải Nén Huffman", font=("Arial", 20, "bold"), fg="#004d99", bg="#f2f2f2")
            header.pack(pady=15)

            # ====== Frame chọn loại file ======
            type_frame = tk.LabelFrame(self.root, text="Chọn loại file", padx=10, pady=5, bg="#f2f2f2")
            type_frame.pack(fill="x", padx=20, pady=5)

            for text, val in [("Text", "text"), ("Image", "image"), ("Audio", "audio")]:
                tk.Radiobutton(type_frame, text=text, variable=self.file_type, value=val, bg="#f2f2f2", font=("Arial", 11)).pack(side="left", padx=10)

            # ====== Frame chọn file ======
            file_frame = tk.Frame(self.root, bg="#f2f2f2")
            file_frame.pack(fill="x", padx=20, pady=10)

            tk.Button(file_frame, text="📂 Chọn File", command=self.choose_file, bg="#cce6ff", width=15).pack(side="left")
            tk.Entry(file_frame, textvariable=self.file_path, width=60, font=("Arial", 10)).pack(side="left", padx=10)

            # ====== Nút nén và giải nén ======
            btn_frame = tk.Frame(self.root, bg="#f2f2f2")
            btn_frame.pack(pady=10)

            tk.Button(btn_frame, text="🗜 Mã hóa", command=self.encode_file, bg="#b3ffd9", width=20).pack(side="left", padx=20)
            tk.Button(btn_frame, text="🧩 Giải mã", command=self.decode_file, bg="#ffcccc", width=20).pack(side="left", padx=20)

            # ====== Tabs hiển thị kết quả ======
            notebook = ttk.Notebook(self.root)
            notebook.pack(fill="both", expand=True, padx=15, pady=10)

            self.result_tab = tk.Text(notebook, wrap=tk.WORD, font=("Consolas", 11))
            self.codes_tab = tk.Text(notebook, wrap=tk.WORD, font=("Consolas", 11))

            notebook.add(self.result_tab, text="📊 Kết Quả")
            notebook.add(self.codes_tab, text="💡 Bảng Mã Huffman")

        def choose_file(self):
            filetype = self.file_type.get()
            if filetype == "text":
                filetypes = [("Text files", "*.txt")]
            elif filetype == "image":
                filetypes = [("Image files", "*.png *.jpg *.bmp")]
            elif filetype == "audio":
                filetypes = [("Audio files", "*.wav *.mp3")]
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
            try:
                if filetype == "text":
                    bits, code_table, stats = text_module.encode(path)
                elif filetype == "image":
                    bits, code_table, stats = image_module.encode(path)
                elif filetype == "audio":
                    bits, code_table, stats = audio_module.encode(path)
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
            huff_path = filedialog.askopenfilename(filetypes=[("Huffman Encoded Files", "*.huff")])
            if not huff_path:
                return

            filetype = self.file_type.get()
            try:
                if filetype == "text":
                    out_path = text_module.decode(huff_path)
                elif filetype == "image":
                    out_path = image_module.decode(huff_path)
                elif filetype == "audio":
                    out_path = audio_module.decode(huff_path)
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
