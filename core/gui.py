import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from modules import audio_module, text_module, image_module

def launch_main_gui():
    def choose_file():
        filepath.set(filedialog.askopenfilename())

    def show_code_table(code_table):
        window = tk.Toplevel()
        window.title("Bảng mã Huffman")

        text_widget = tk.Text(window, width=60, height=25)
        text_widget.pack(padx=10, pady=10)

        for byte, code in code_table.items():
            try:
                char = byte.decode('utf-8')
                line = f"{repr(char)} ({byte})  =>  {code}\n"
            except:
                line = f"{byte}  =>  {code}\n"
            text_widget.insert(tk.END, line)

        text_widget.config(state=tk.DISABLED)

    def compress():
        file = filepath.get()
        mode = option.get()
        if not file:
            messagebox.showerror("Lỗi", "Chưa chọn file!")
            return

        if mode == "Audio":
            output_path, table_path, original_size, compressed_size, code_table = audio_module.compress(file)
            show_code_table(code_table)
            messagebox.showinfo(
                "Thành công",
                f"Nén thành công!\nGốc: {original_size} bytes\nNén: {compressed_size} bytes\nLưu: {output_path}"
            )
        elif mode == "Text":
            text_module.compress(file)
        elif mode == "Image":
            image_module.compress(file)
        else:
            messagebox.showwarning("Thông báo", "Chưa chọn chế độ")

    def decompress():
        file = filepath.get()
        mode = option.get()
        if not file:
            messagebox.showerror("Lỗi", "Chưa chọn file!")
            return

        if mode == "Audio":
            output_path, code_table = audio_module.decompress(file)
            messagebox.showinfo("Thành công", f"Giải nén thành công!\nLưu: {output_path}")
        elif mode == "Text":
            text_module.decompress(file)
        elif mode == "Image":
            image_module.decompress(file)
        else:
            messagebox.showwarning("Thông báo", "Chưa chọn chế độ")

    root = tk.Tk()
    root.title("Bộ mã hóa tổng hợp by Cường đẹp trai")

    tk.Label(root, text="Chọn chế độ:").grid(row=0, column=0, padx=10, pady=5)
    option = ttk.Combobox(root, values=["Audio", "Text", "Image"])
    option.grid(row=0, column=1)

    tk.Label(root, text="Đường dẫn file:").grid(row=1, column=0, padx=10, pady=5)
    filepath = tk.StringVar()
    tk.Entry(root, textvariable=filepath, width=40).grid(row=1, column=1)
    tk.Button(root, text="Browse", command=choose_file).grid(row=1, column=2)

    tk.Button(root, text="Nén", command=compress).grid(row=2, column=0, pady=10)
    tk.Button(root, text="Giải nén", command=decompress).grid(row=2, column=1)

    root.mainloop()
