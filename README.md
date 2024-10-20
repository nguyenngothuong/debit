# Ứng dụng Theo dõi Nợ

Đây là một ứng dụng web được xây dựng bằng Streamlit để theo dõi và quản lý các khoản nợ. Ứng dụng sử dụng API của Lark Suite để lưu trữ và truy xuất dữ liệu.

## Tính năng

1. **Tra cứu nợ**:
   - Người dùng có thể nhập số điện thoại để xem thông tin nợ của họ.
   - Hiển thị chi tiết các khoản nợ bao gồm tên khoản nợ, ngày ghi nợ, số tiền và trạng thái.
   - Tính tổng số tiền còn lại phải trả.
   - Lọc khoản nợ theo trạng thái (Tất cả, Đã trả, Chưa trả).

2. **Dashboard**:
   - Hiển thị biểu đồ cột tổng quan về các khoản nợ theo tháng.
   - Phân biệt giữa "Nợ tôi" và "Tôi nợ" trên biểu đồ.

3. **Đăng nhập Admin**:
   - Quản trị viên có thể đăng nhập để xem tất cả các khoản nợ.
   - Hiển thị danh sách đầy đủ các khoản nợ với khả năng lọc theo trạng thái.
   - Tính tổng số tiền còn lại phải trả cho tất cả các khoản nợ.

## Yêu cầu hệ thống

- Python 3.7+
- Streamlit
- Requests
- Plotly
- Pandas

## Cài đặt

1. Clone repository này về máy của bạn:
   ```
   git clone https://github.com/your-username/debt-tracking-app.git
   cd debt-tracking-app
   ```

2. Cài đặt các thư viện cần thiết:
   ```
   pip install -r requirements.txt
   ```

3. Tạo file `.streamlit/secrets.toml` và thêm các thông tin cấu hình cần thiết:
   ```toml
   LARK_APP_ID = "your_lark_app_id"
   LARK_APP_SECRET = "your_lark_app_secret"
   BASE_ID = "your_base_id"
   DEBT_TABLE_ID = "your_debt_table_id"
   DEBT_VIEW_ID = "your_debt_view_id"
   CONFIG_TABLE_ID = "your_config_table_id"
   ADMIN_USERNAME = "admin"
   ADMIN_PASSWORD = "your_admin_password"
   ```

## Sử dụng

1. Chạy ứng dụng:
   ```
   streamlit run app.py
   ```

2. Mở trình duyệt web và truy cập địa chỉ được hiển thị trong terminal (thường là http://localhost:8501).

3. Sử dụng các tính năng của ứng dụng:
   - **Tra cứu nợ**: Nhập số điện thoại để xem thông tin nợ.
   - **Dashboard**: Xem biểu đồ tổng quan về các khoản nợ theo tháng.
   - **Đăng nhập Admin**: Sử dụng tên đăng nhập và mật khẩu được cấu hình trong `secrets.toml` để truy cập trang quản lý.

## Cấu trúc dự án

- `app.py`: File chính chứa mã nguồn của ứng dụng Streamlit.
- `requirements.txt`: Danh sách các thư viện Python cần thiết.
- `.streamlit/secrets.toml`: File chứa các thông tin cấu hình nhạy cảm (không được đưa lên GitHub).
- `README.md`: File này, chứa thông tin về dự án.

## Bảo mật

- Thông tin đăng nhập admin và các khóa API được lưu trong file `secrets.toml` và không nên được chia sẻ công khai.
- Đảm bảo rằng file `secrets.toml` đã được thêm vào `.gitignore` để tránh vô tình đẩy lên kho lưu trữ công khai.

## Xử lý lỗi và Ghi log

- Ứng dụng sử dụng module `logging` để ghi lại các hoạt động và lỗi.
- Kiểm tra console hoặc file log để xem thông tin chi tiết về các lỗi có thể xảy ra.

## Đóng góp

Nếu bạn muốn đóng góp cho dự án này, vui lòng tạo một pull request hoặc mở một issue để thảo luận về các thay đổi bạn muốn thực hiện.

## Liên hệ

Nếu bạn có bất kỳ câu hỏi hoặc góp ý nào, vui lòng liên hệ qua email: your.email@example.com

## Giấy phép

Dự án này được phân phối dưới giấy phép MIT. Xem file `LICENSE` để biết thêm chi tiết.
