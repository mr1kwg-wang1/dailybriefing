"""왕기 대시보드 발송 스크립트 - dashboard.txt 내용을 텔레그램으로 전송"""
import os
import requests

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

with open("dashboard.txt", encoding="utf-8") as f:
    text = f.read().strip()

if not text:
    text = "왕기대시보드: 오늘자 dashboard.txt가 비어 있습니다."

for i in range(0, len(text), 4000):
    chunk = text[i:i + 4000]
    resp = requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": CHAT_ID, "text": chunk},
        timeout=10,
    )
    resp.raise_for_status()

print("발송 완료")
