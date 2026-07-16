import os
import requests
from datetime import datetime, timedelta

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

WEEKDAYS = ["월", "화", "수", "목", "금", "토", "일"]

def main():
    kst = datetime.utcnow() + timedelta(hours=9)
    weekday = WEEKDAYS[kst.weekday()]
    date_str = kst.strftime(f"%Y년 %m월 %d일 ({weekday})")

    message = (
        f"🌅 왕기대시보드 | {date_str}\n\n"
        "Claude에서 오늘브리핑 을 입력하세요\n\n"
        "👉 https://claude.ai\n\n"
        "━━━━━━━━━━━━\n"
        "📅 캘린더 일정\n"
        "📧 중요 메일\n"
        "🌍 중동·호르무즈\n"
        "📈 미국·코스피 증시\n"
        "🏠 벽산블루밍 4단지\n"
        "⚽ 월드컵 결과\n"
        "━━━━━━━━━━━━"
    )

    resp = requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": CHAT_ID, "text": message},
        timeout=10,
    )
    resp.raise_for_status()
    print("발송 완료!")

if __name__ == "__main__":
    main()
