import streamlit as st
import requests
import json
from datetime import datetime, timedelta
import logging
import pandas as pd
import plotly.graph_objects as go
import re

# Cấu hình logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Hàm để lấy token
def get_tenant_access_token():
    url = "https://open.larksuite.com/open-apis/auth/v3/tenant_access_token/internal"
    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }
    data = {
        "app_id": st.secrets["LARK_APP_ID"],
        "app_secret": st.secrets["LARK_APP_SECRET"]
    }
    logger.info("Đang gửi yêu cầu lấy token")
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        logger.info("Đã nhận phản hồi từ yêu cầu lấy token")
        return response.json()["tenant_access_token"]
    except Exception as e:
        logger.error(f"Lỗi khi lấy token: {str(e)}")
        raise Exception(f"Không thể lấy token: {str(e)}")

# Hàm để tìm kiếm dữ liệu từ Lark Suite
def search_lark_data(table_id, filter_string=None, page_size=500):
    url = f"https://open.larksuite.com/open-apis/bitable/v1/apps/{st.secrets['BASE_ID']}/tables/{table_id}/records/search?page_size={page_size}"
    headers = {
        "Authorization": f"Bearer {get_tenant_access_token()}",
        "Content-Type": "application/json"
    }
    payload = {}
    if filter_string:
        payload = json.loads(filter_string)
    
    logger.info(f"Gửi yêu cầu đến URL: {url}")
    logger.info(f"Headers: {headers}")
    logger.info(f"Payload: {json.dumps(payload)}")
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        logger.info(f"Mã trạng thái phản hồi: {response.status_code}")
        logger.info(f"Nội dung phản hồi: {response.text}")
        
        data = response.json()
        if "code" in data and data["code"] != 0:
            logger.error(f"Lỗi API: {data}")
            raise Exception(f"Lỗi API: {data['msg']}")
        
        return data.get("data", {}).get("items", [])
    except requests.exceptions.RequestException as e:
        logger.error(f"Lỗi yêu cầu: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Lỗi: {str(e)}")
        raise

# Hàm để lấy thông tin người nợ từ số điện thoại
def get_debtor_info(phone_number):
    filter = {
        "filter": {
            "conjunction": "and",
            "conditions": [
                {
                    "field_name": "phone",
                    "operator": "contains",
                    "value": [phone_number]
                }
            ]
        }
    }
    logger.info(f"Đang tìm kiếm thông tin người nợ cho số điện thoại: {phone_number}")
    config_data = search_lark_data(st.secrets["CONFIG_TABLE_ID"], json.dumps(filter))
    if config_data:
        logger.info(f"Đã tìm thấy thông tin người nợ cho số điện thoại: {phone_number}")
        return config_data[0]["fields"].get("Người nợ"), config_data[0]["fields"].get("Người nợ")
    logger.info(f"Không tìm thấy thông tin người nợ cho số điện thoại: {phone_number}")
    return None, None

# Hàm để lấy thông tin nợ
def get_debt_info(debtor_code):
    filter = {
        "filter": {
            "conjunction": "and",
            "conditions": [
                {
                    "field_name": "Người nợ",
                    "operator": "contains",
                    "value": [debtor_code]
                }
            ]
        }
    }
    logger.info(f"Đang tìm kiếm thông tin nợ cho người nợ: {debtor_code}")
    debt_data = search_lark_data(st.secrets["DEBT_TABLE_ID"], json.dumps(filter))
    debt_details = []
    for item in debt_data:
        fields = item["fields"]
        ten_khoan_no = ' '.join([item.get('text', '') for item in fields.get("Tên khoản nợ", [])]) if isinstance(fields.get("Tên khoản nợ"), list) else fields.get("Tên khoản nợ", "")
        ghi_chu_khoan_no = ' '.join([item.get('text', '') for item in fields.get("Ghi chú khoản nợ", [])]) if isinstance(fields.get("Ghi chú khoản nợ"), list) else fields.get("Ghi chú khoản nợ", "")
        
        debt_details.append({
            "Tên khoản nợ": ten_khoan_no,
            "Ngày ghi nợ": datetime.fromtimestamp(fields.get("Ngày ghi nợ", 0)/1000).strftime('%d/%m/%Y') if fields.get("Ngày ghi nợ") else "Không có",
            "Thời gian phát sinh": datetime.fromtimestamp(fields.get("Thời phát phát sinh của khoản nợ", 0)/1000).strftime('%d/%m/%Y %H:%M:%S') if fields.get("Thời phát phát sinh của khoản nợ") else "Không có",
            "Số tiền": float(fields.get("Số tiền ghi nợ", 0)),
            "Nội dung": ghi_chu_khoan_no,
            "Trạng thái": "Đã trả" if fields.get("Đã trả", False) else "Chưa trả"
        })
    logger.info(f"Đã tìm thấy {len(debt_details)} khoản nợ cho người nợ: {debtor_code}")
    return debt_details

# Hàm đăng nhập
def login(username, password):
    logger.info("Đang thực hiện đăng nhập")
    return username == st.secrets["ADMIN_USERNAME"] and password == st.secrets["ADMIN_PASSWORD"]

# Hàm kiểm tra số điện thoại hợp lệ
def is_valid_phone_number(phone_number):
    pattern = r'^(0|\+84)(\s|\.)?((3[2-9])|(5[689])|(7[06-9])|(8[1-689])|(9[0-46-9]))(\d)(\s|\.)?(\d{3})(\s|\.)?(\d{3})$'
    return re.match(pattern, phone_number) is not None

# Giao diện chính
def main():
    st.title("Ứng dụng Theo dõi Nợ")

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "debt_details" not in st.session_state:
        st.session_state.debt_details = None
    if "debtor_name" not in st.session_state:
        st.session_state.debtor_name = None

    if not st.session_state.logged_in:
        tab1, tab2, tab3 = st.tabs(["Tra cứu nợ", "Dashboard", "Đăng nhập Admin"])

        with tab1:
            st.header("Tra cứu nợ")
            phone_number = st.text_input("Nhập số điện thoại của bạn nhé hihi:")
            if st.button("Tra cứu"):
                if not is_valid_phone_number(phone_number):
                    st.error("Số điện thoại không hợp lệ. Vui lòng nhập lại.")
                else:
                    try:
                        logger.info(f"Đang tra cứu thông tin nợ cho số điện thoại: {phone_number}")
                        st.info(f"Đang tra cứu thông tin nợ cho số điện thoại: {phone_number}")
                        debtor_code, debtor_name = get_debtor_info(phone_number)
                        if debtor_code:
                            st.session_state.debt_details = get_debt_info(debtor_code)
                            st.session_state.debtor_name = debtor_name
                            if debtor_name:
                                st.success(f"Xin chào {debtor_name}!")
                            else:
                                st.success("Đã tìm thấy thông tin nợ.")
                            logger.info(f"Đã tìm thấy thông tin nợ cho số điện thoại: {phone_number}")
                        else:
                            st.warning("Không tìm thấy thông tin nợ cho số điện thoại này. Vui lòng kiểm tra lại số điện thoại hoặc liên hệ với quản trị viên.")
                            logger.info(f"Không tìm thấy thông tin nợ cho số điện thoại: {phone_number}")
                    except Exception as e:
                        st.error(f"Đã xảy ra lỗi: {str(e)}")
                        logger.error(f"Lỗi khi tra cứu thông tin nợ: {str(e)}", exc_info=True)

            if st.session_state.debt_details is not None:
                df = pd.DataFrame(st.session_state.debt_details)
                
                status_filter = st.selectbox("Lọc theo trạng thái:", ["Chưa trả", "Tất cả", "Đã trả"], index=0)
                if status_filter != "Tất cả":
                    df = df[df["Trạng thái"] == status_filter]
                
                total_unpaid = df[df["Trạng thái"] == "Chưa trả"]["Số tiền"].sum()
                st.metric(label="Tổng số tiền còn lại phải trả", value=f"{total_unpaid:,.0f} VNĐ")
                
                st.dataframe(df.style.format({"Số tiền": "{:,.0f} VNĐ"}))
                
                # Hiển thị mã QR và thông tin thanh toán
                if total_unpaid > 0:
                    qr_amount = int(total_unpaid)
                    qr_description = f"{st.session_state.debtor_name}%20tra%20no"
                    qr_url = f"https://img.vietqr.io/image/MB-ngothuong-print.png?amount={qr_amount}&addInfo={qr_description}"
                    st.image(qr_url, caption="Mã QR để trả nợ")
                    
                    messenger_link = "https://www.messenger.com/t/100015826450743"
                    st.markdown(f"[Nhấn vào đây để liên hệ qua Messenger]({messenger_link})", unsafe_allow_html=True)

        with tab2:
            st.header("Dashboard")
            if st.session_state.debt_details is not None:
                df = pd.DataFrame(st.session_state.debt_details)
                df['Ngày ghi nợ'] = pd.to_datetime(df['Ngày ghi nợ'], format='%d/%m/%Y')
                df['Tháng'] = df['Ngày ghi nợ'].dt.strftime('%Y/%m')
                
                # Tính tổng nợ theo tháng
                monthly_debt = df.groupby('Tháng').agg({
                    'Số tiền': lambda x: (x[x > 0].sum(), x[x < 0].abs().sum())
                }).reset_index()
                
                monthly_debt['Nợ tôi'] = monthly_debt['Số tiền'].apply(lambda x: x[0])
                monthly_debt['Tôi nợ'] = monthly_debt['Số tiền'].apply(lambda x: x[1])
                
                # Tạo biểu đồ cột
                fig = go.Figure()
                fig.add_trace(go.Bar(x=monthly_debt['Tháng'], y=monthly_debt['Nợ tôi'], name='Nợ tôi'))
                fig.add_trace(go.Bar(x=monthly_debt['Tháng'], y=monthly_debt['Tôi nợ'], name='Tôi nợ'))
                
                fig.update_layout(
                    title='Tổng số nợ theo tháng',
                    xaxis_title='Tháng',
                    yaxis_title='Tổng số tiền nợ (VNĐ)',
                    barmode='group'
                )
                
                st.plotly_chart(fig)
            else:
                st.info("Vui lòng tra cứu thông tin nợ trước khi xem dashboard.")

        with tab3:
            st.header("Đăng nhập Admin")
            username = st.text_input("Tên đăng nhập:")
            password = st.text_input("Mật khẩu:", type="password")
            if st.button("Đăng nhập"):
                if login(username, password):
                    st.session_state.logged_in = True
                    logger.info("Đăng nhập thành công")
                    st.rerun()
                else:
                    st.error("Sai tên đăng nhập hoặc mật khẩu.")
                    logger.warning("Đăng nhập thất bại")

    else:
        st.header("Trang quản lý Admin")
        if st.button("Đăng xuất"):
            st.session_state.logged_in = False
            logger.info("Đã đăng xuất")
            st.rerun()

        try:
            logger.info("Đang lấy dữ liệu nợ cho trang Admin")
            debt_data = search_lark_data(st.secrets["DEBT_TABLE_ID"])
            debt_details = []
            for item in debt_data:
                fields = item["fields"]
                debt_details.append({
                    "Tên khoản nợ": fields.get("Tên khoản nợ", [{}])[0].get("text", "") if isinstance(fields.get("Tên khoản nợ"), list) else "",
                    "Người nợ": fields.get("Người nợ", ""),
                    "Ngày ghi nợ": (datetime.fromtimestamp(fields.get("Ngày ghi nợ", 0)/1000) + timedelta(hours=7)).strftime('%d/%m/%Y') if fields.get("Ngày ghi nợ") else "Không có",
                    "Thời gian phát sinh": (datetime.fromtimestamp(fields.get("Thời phát phát sinh của khoản nợ", 0)/1000) + timedelta(hours=7)).strftime('%d/%m/%Y %H:%M:%S') if fields.get("Thời phát phát sinh của khoản nợ") else "Không có",
                    "Số tiền": float(fields.get("Số tiền ghi nợ") or 0),
                    "Nội dung": fields.get("Ghi chú khoản nợ", [{}])[0].get("text", "") if isinstance(fields.get("Ghi chú khoản nợ"), list) else "",
                    "Trạng thái": "Đã trả" if fields.get("Đã trả", False) else "Chưa trả"
                })
            df = pd.DataFrame(debt_details)
            
            status_filter = st.selectbox("Lọc theo trạng thái:", ["Chưa trả", "Tất cả", "Đã trả"], index=0)
            if status_filter != "Tất cả":
                df = df[df["Trạng thái"] == status_filter]
            
            total_unpaid = df[df["Trạng thái"] == "Chưa trả"]["Số tiền"].sum()
            st.metric(label="Tổng số tiền còn lại phải trả", value=f"{total_unpaid:,.0f} VNĐ")
            
            st.dataframe(df.style.format({"Số tiền": "{:,.0f} VNĐ"}))
            
            # Tạo biểu đồ cột nằm ngang cho tổng nợ theo người dùng
            user_debt = df[df["Trạng thái"] == "Chưa trả"].groupby("Người nợ")["Số tiền"].sum().sort_values(ascending=True)
            
            def format_amount(amount):
                if amount >= 1000000:
                    return f"{amount/1000000:.1f}M"
                elif amount >= 1000:
                    return f"{amount/1000:.0f}k"
                else:
                    return f"{amount:.0f}"
            
            fig = go.Figure(go.Bar(
                x=user_debt.values,
                y=user_debt.index,
                orientation='h',
                text=[format_amount(val) for val in user_debt.values],
                textposition='outside',
                textfont=dict(size=12),
                hoverinfo='text',
                hovertext=[f"{name}: {format_amount(val)} VNĐ" for name, val in zip(user_debt.index, user_debt.values)]
            ))
            
            fig.update_layout(
                title='Tổng nợ theo người dùng (Chưa trả)',
                xaxis_title='Tổng số tiền nợ (VNĐ)',
                yaxis_title='Người nợ',
                height=600,
                xaxis=dict(showticklabels=False)
            )
            
            st.plotly_chart(fig)
            
            logger.info("Đã hiển thị dữ liệu nợ và biểu đồ cho trang Admin")
            
        except Exception as e:
            st.error(f"Đã xảy ra lỗi khi lấy dữ liệu: {str(e)}")
            logger.error(f"Lỗi khi lấy dữ liệu cho trang Admin: {str(e)}", exc_info=True)

if __name__ == "__main__":
    main()
