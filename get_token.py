import requests

def get_tenant_access_token(app_id, app_secret):
    url = "https://open.larksuite.com/open-apis/auth/v3/tenant_access_token/internal"
    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }
    data = {
        "app_id": app_id,
        "app_secret": app_secret
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()["tenant_access_token"]

# Sử dụng hàm
if __name__ == "__main__":
    token = get_tenant_access_token("cli_a6ed800781389009", "jUJna3v29sKNKFIZUqTlrOUoFUd3iC0j")
    if token:
        print(f"Tenant Access Token: {token}")
    else:
        print("Không thể lấy được token.")
