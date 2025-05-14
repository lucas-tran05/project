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

    def process_file():
        file = filepath.get()
        data_type = type_option.get()
        operation = root_option.get()

        if not file or not data_type or not operation:
            messagebox.showerror("Thiếu thông tin", "Hãy điền đủ các lựa chọn và file")
            return

        if data_type == "Audio":
            if operation == "Mã hóa":
                output, table, og, cp, code_table = audio_module.compress(file)
                show_code_table(code_table)
                messagebox.showinfo("Nén xong", f"Đã lưu: {output}\nDung lượng: {og} -> {cp}")
            else:
                output, table = audio_module.decompress(file)
                messagebox.showinfo("Giải nén xong", f"Đã lưu: {output}")

        elif data_type == "Text":
            if operation == "Mã hóa":
                code_table = text_module.compress(file)
                show_code_table(code_table)
            else:
                text_module.decompress(file)

        elif data_type == "Image":
            if operation == "Mã hóa":
                code_table = image_module.compress(file)
                show_code_table(code_table)
            else:
                image_module.decompress(file)

    # === UI ===
    window = tk.Tk()
    window.title("Máy mã hóa giải mã tổng hợp by Cường đẹp trai")

    # Cột trái: tuỳ chọn
    frame_left = tk.Frame(window, padx=10, pady=10)
    frame_left.grid(row=0, column=0, sticky="n")

    tk.Label(frame_left, text="Option root:").pack(anchor="w")
    root_option = ttk.Combobox(frame_left, values=["Mã hóa", "Giải mã"])
    root_option.pack(fill="x")

    tk.Label(frame_left, text="Option next:").pack(anchor="w", pady=(10, 0))
    type_option = ttk.Combobox(frame_left, values=["Text", "Image", "Audio"])
    type_option.pack(fill="x")

    tk.Label(frame_left, text="File input:").pack(anchor="w", pady=(10, 0))
    filepath = tk.StringVar()
    tk.Entry(frame_left, textvariable=filepath, width=30).pack()
    tk.Button(frame_left, text="Browse", command=choose_file).pack(pady=5)

    tk.Button(frame_left, text="Thực hiện", command=process_file).pack(pady=(20, 0))

    # Cột phải: khung xử lý
    frame_right = tk.Frame(window, padx=10, pady=10)
    frame_right.grid(row=0, column=1)

    # Ô 1: nhập dữ liệu
    frame_top = tk.LabelFrame(frame_right, text="1. Nhập dữ liệu")
    frame_top.pack(fill="both", expand=True)

    input_label = tk.Label(frame_top, text="Chọn file hoặc nhập text tùy theo loại dữ liệu")
    input_label.pack()

    # Ô 2: kết quả
    frame_bottom = tk.LabelFrame(frame_right, text="2. Kết quả")
    frame_bottom.pack(fill="both", expand=True, pady=10)

    tk.Label(frame_bottom, text="(Hiển thị bảng mã sau khi mã hóa)").pack()

    btn_frame = tk.Frame(frame_bottom)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Tải file .huff", command=lambda: messagebox.showinfo("TODO", "Chức năng chưa làm")).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Xem bit mã hóa", command=lambda: messagebox.showinfo("TODO", "Chức năng chưa làm")).pack(side="left", padx=5)

    window.mainloop()
