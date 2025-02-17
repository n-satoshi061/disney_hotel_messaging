import os
from dotenv import load_dotenv
import requests
from datetime import datetime, timedelta

# .env ファイルから環境変数を読み込む
load_dotenv()

# 環境変数から LINE Notify トークンを取得する
line_notify_token = os.getenv("LINE_NOTIFY_TOKEN")

# Calculate the date two months from today
two_months_from_now = datetime.now() + timedelta(days=60)
use_date = two_months_from_now.strftime("%Y%m%d")

# Function to format date
def format_date(date):
    dt = datetime.strptime(date, "%Y%m%d")
    return dt.strftime("%Y年%-m月%-d日")

formatted_date = format_date(use_date)

# Define the URL and headers for the request
url = "https://reserve.tokyodisneyresort.jp/hotel/api/queryHotelPriceStock/"
headers = {
    "User-Agent": "PostmanRuntime/7.38.0",
}

# Define the hotel codes and names
hotels = {
    "HOTDHSCL0005N": "ディズニーランドホテル",
    "HOFSHBST0001N": "ファンタジースプリングスホテル",
    "HODAHTTN0004N": "ディズニーアンバサダーホテル",
    "HODHMCTG0001N": "ホテルミラコスタ",
    "HOTSHSQR0001N": "トイ・ストーリーホテル"
}

# Define the form-data payload template
payload_template = {
    "useDate": use_date,
    "stayingDays": 1,
    "adultNum": 2,
    "childNum": 0,
    "roomsNum": 1,
    "stockQueryType": 3,
    "rrc3005ProcessingType": "update",
}

# Function to send notification
def send_line_notify(message):
    url = "https://notify-api.line.me/api/notify"
    headers = {
        "Authorization": f"Bearer {line_notify_token}"
    }
    data = {
        "message": message
    }
    response = requests.post(url, headers=headers, data=data)
    return response.status_code

# Function to check hotel availability
def check_hotel_availability():
    for commodityCD, hotel_name in hotels.items():
        # ペイロードの設定
        payload = payload_template.copy()
        payload["commodityCD"] = commodityCD
        
        try:
            # リクエストの送信
            response = requests.post(url, headers=headers, data=payload)
            response.raise_for_status()
            response_json = response.json()
        except requests.exceptions.RequestException as e:
            print(f"リクエストエラー: {e}")
            continue
        except ValueError:
            print("レスポンスがJSONではありませんでした。")
            continue
        
        # 空き状況の確認
        if "remainStockNum" in response.text:
            message = f"{hotel_name} ({formatted_date}) に空きがあります！"
            send_line_notify(message)
            print(message)
        else:
            message = f"{hotel_name} ({formatted_date}) に空きがありません。"
            print(message)

if __name__ == "__main__":
    check_hotel_availability()
