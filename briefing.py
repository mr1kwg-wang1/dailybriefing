"""왕기 대시보드 발송 스크립트 - dashboard.txt 내용을 텔레그램으로 전송"""
import os
import re
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

import requests

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

KST = ZoneInfo("Asia/Seoul")


def send(message: str) -> None:
    for i in range(0, len(message), 4000):
        chunk = message[i:i + 4000]
        resp = requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={"chat_id": CHAT_ID, "text": chunk},
            timeout=10,
        )
        resp.raise_for_status()


with open("dashboard.txt", encoding="utf-8") as f:
    text = f.read().strip()

if not text:
    send("⚠️ 왕기대시보드: 오늘자 dashboard.txt가 비어 있습니다. 콘텐츠 생성 단계를 확인하세요.")
    sys.exit(1)

# dashboard.txt는 외부 생성 단계(cron-job.org 트리거 + PAT 커밋)가 매일 새로 써야 한다.
# 그 단계가 실패하면 어제 파일이 그대로 남아, 검증 없이는 "어제 브리핑"이 오늘 것처럼 발송된다.
today = datetime.now(KST).date()
match = re.search(r"(\d{4})년\s*(\d{1,2})월\s*(\d{1,2})일", text)
if match:
    doc_date = datetime(int(match.group(1)), int(match.group(2)), int(match.group(3))).date()
    if doc_date != today:
        send(
            "⚠️ 왕기대시보드: dashboard.txt 날짜({})가 오늘({})과 다릅니다. "
            "콘텐츠 생성 트리거가 실패했을 수 있으니 확인하세요.".format(doc_date, today)
        )
        sys.exit(1)
else:
    send("⚠️ 왕기대시보드: dashboard.txt에서 날짜를 찾지 못했습니다. 파일 형식을 확인하세요.")
    sys.exit(1)

send(text)
print("발송 완료")
