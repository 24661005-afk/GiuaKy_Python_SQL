import pyodbc
import pandas as pd
import gradio as grad

# 1. Áp dụng OOP: Tạo class để quản lý CSDL
class SQLManager:
    def __init__(self):
        # Cấu hình chuỗi kết nối đến Docker container
        self.conn_str = (
            "DRIVER={ODBC Driver 18 for SQL Server};" # Hoặc Driver 17 tùy thuộc vào OS của Codespace
            "SERVER=127.0.0.1,1433;"
            "DATABASE=master;"
            "UID=sa;"
            "PWD=YourStrong@Password123;"
            "Encrypt=no;"
        )
    
    def lay_du_lieu_san_pham(self):
        try:
            conn = pyodbc.connect(self.conn_str)
            # Câu lệnh truy vấn SQL như trên bảng (select ... from ... where)
            query = "SELECT * FROM Products" 
            
            # Đọc dữ liệu trực tiếp vào Pandas DataFrame
            df = pd.read_sql(query, conn)
            conn.close()
            return df
        except Exception as e:
            # Trả về DataFrame trống kèm lỗi nếu chưa tạo bảng dữ liệu
            return pd.DataFrame({"Thông báo": [f"Chưa có dữ liệu hoặc lỗi kết nối: {e}"]})

# 2. Khởi tạo đối tượng
db = SQLManager()

# 3. Định nghĩa hàm xử lý cho giao diện Gradio
def hien_thi_man_hinh():
    df_ket_qua = db.lay_du_lieu_san_pham()
    return df_ket_qua

# 4. Thiết kế giao diện Gradio (Cấu trúc UI)
with grad.Blocks() as demo:
    grad.Markdown("# HỆ THỐNG QUẢN LÝ SẢN PHẨM - BÀI GIỮA KỲ")
    btn = grad.Button("Tải dữ liệu từ SQL Server")
    output = grad.DataFrame() # Hiển thị dạng bảng
    
    btn.click(fn=hien_thi_man_hinh, outputs=output)

# 5. Chạy ứng dụng
if __name__ == "__main__":
    # GitHub Codespaces sẽ tự động forward port và cấp cho bạn một link để xem giao diện
    demo.launch(server_name="0.0.0.0", server_port=7860)
