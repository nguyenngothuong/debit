# Ứng dụng Theo dõi Nợ

Đây là một ứng dụng web được xây dựng bằng Streamlit để theo dõi và quản lý các khoản nợ. Ứng dụng sử dụng API của Lark Suite để lưu trữ và truy xuất dữ liệu.

## Tính năng

- Tra cứu nợ: Người dùng có thể nhập số điện thoại để xem thông tin nợ của họ.
- Dashboard: Hiển thị biểu đồ tổng quan về các khoản nợ theo tháng.
- Đăng nhập Admin: Quản trị viên có thể đăng nhập để xem tất cả các khoản nợ.

## Cài đặt

1. Clone repository này về máy của bạn.
2. Cài đặt các thư viện cần thiết bằng cách chạy lệnh:
   ```
   pip install -r requirements.txt
   ```

3. Tạo một file `.streamlit/secrets.toml` và thêm các thông tin cấu hình cần thiết:
   ```
   LARK_APP_ID = "your_app_id"
   LARK_APP_SECRET = "your_app_secret"
   BASE_ID = "your_base_id"
   CONFIG_TABLE_ID = "your_config_table_id"
   DEBT_TABLE_ID = "your_debt_table_id"
   ADMIN_USERNAME = "admin_username"
   ADMIN_PASSWORD = "admin_password"
   ```

## Sử dụng

Để chạy ứng dụng, sử dụng lệnh sau:
