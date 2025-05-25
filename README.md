# 🔒 Huffman Compressor GUI 

Ứng dụng mã hóa và giải mã dữ liệu sử dụng thuật toán Huffman với giao diện đồ họa thân thiện.  
Hỗ trợ các định dạng: Văn bản (.txt), Hình ảnh (.png, .jpg), Âm thanh (.wav).

---
## 🧠 Bộ môn Lí thuyết thông tin
Giảng viên: Phạm Văn Sự

---

## 🧠 Tính năng nổi bật

- ⚡ Mã hóa và giải mã văn bản, hình ảnh, âm thanh nhanh chóng.
- 🧩 Giao diện đồ họa dễ dùng với Tkinter.
- 📦 Lưu trữ dữ liệu mã hóa bằng định dạng nhị phân.
- 📊 Hiển thị thông tin thống kê và tỷ lệ nén.

---

## 👨‍👩‍👧‍👦 Thành viên nhóm

| Họ tên               | Vai trò                            |
|----------------------|--------------------------------    |
| Trần Quốc Cường      | Leader, Dev xử lý âm thanh         |
| Dương Thiên Ngân     | Dev xử lý văn bản, Dev GUI         |
| Lê Văn Duy           | Dev xử lý hình ảnh, Core Logic     |

---

## ⚙️ Cài đặt và chạy dự án

### 1️⃣ Clone project:

```bash
git clone https://github.com/your-username/project.git
cd project
```

### 2️⃣ Tạo môi trường ảo (tùy chọn nhưng khuyến nghị):

```bash
python -m venv venv
source venv/bin/activate    
venv\Scripts\activate       
```

### 3️⃣ Cài đặt thư viện cần thiết:

```bash
pip install -r requirements.txt
```

📁 **Lưu ý**: tkinter là thư viện chuẩn của Python, không cần cài đặt thêm.

### 4️⃣ Chạy chương trình:

```bash
python main.py
```
---

## 🛠 Công nghệ sử dụng

- Python 3.10+
- Tkinter (GUI)
- Pillow (Xử lý ảnh)
- Pydub hoặc librosa (Xử lý âm thanh)
- Tự cài module Huffman riêng (utils.huffman)
