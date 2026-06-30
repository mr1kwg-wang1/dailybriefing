"""
왕기 대시보드 - 매일 아침 브리핑 자동 발송 스크립트
환율, 날씨(단양/양평), 중동 뉴스 요약을 텔레그램으로 전송
"""

import os
import requests
from datetime import datetime, timezone, timedelta

# ── 환경변수 (GitHub Secrets에서 주입됨) ──
BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

KST = timezone(timedelta(hours=9))


def get_exchange_rate():
    """환율 KRW/USD 조회"""
    try:
        r = requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=10)
        data = r.json()
        krw = round(data["rates"]["KRW"])
        return f"{krw:,}원"
    except Exception as e:
        return f"조회 실패 ({e})"


def get_weather(lat, lon, name):
    """날씨 조회 (Open-Meteo)"""
    try:
        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            f"&current=temperature_2m,weathercode,windspeed_10m"
            f"&timezone=Asia/Seoul"
        )
        r = requests.get(url, timeout=10)
        data = r.json()
        temp = round(data["current"]["temperature_2m"])
        code = data["current"]["weathercode"]
        wind = round(data["current"]["windspeed_10m"])

        wmap = {
            0: "맑음 ☀", 1: "대체로 맑음 🌤", 2: "구름 조금 ⛅", 3: "흐림 ☁",
            45: "안개 🌫", 48: "안개 🌫", 51: "이슬비 🌦", 61: "비 🌧",
            63: "비 🌧", 65: "폭우 🌧", 71: "눈 🌨", 80: "소나기 🌦", 95: "뇌우 ⛈",
        }
        desc = wmap.get(code, "확인 필요")
        return f"{name} {temp}°C · {desc} · 풍속 {wind}km/h"
    except Exception as e:
        return f"{name} 조회 실패 ({e})"


def get_news_summary():
    """
    중동 뉴스 헤드라인 수집 (Claude API 미사용 - 헤드라인 원문 정리만)
    """
    headlines = []
    try:
        import feedparser
        feeds = [
            "https://news.google.com/rss/search?q=%ED%98%B8%EB%A5%B4%EB%AC%B4%EC%A6%88&hl=ko&gl=KR&ceid=KR:ko",
            "https://news.google.com/rss/search?q=%EC%9D%B4%EB%9E%80+%EC%9C%A0%EA%B0%80&hl=ko&gl=KR&ceid=KR:ko",
        ]
        for feed_url in feeds:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:3]:
                headlines.append(entry.title)
    except Exception as e:
        return f"뉴스 수집 실패: {e}"

    if not headlines:
        return "수집된 헤드라인 없음"

    # 헤드라인 원문을 그대로 정리해서 전달 (최대 5개)
    lines = "\n".join(f"• {h}" for h in headlines[:5])
    return lines


def build_message():
    now = datetime.now(KST)
    date_str = now.strftime("%Y.%m.%d (%a) %H:%M")

    fx = get_exchange_rate()
    weather_danyang = get_weather(36.9847, 128.3659, "단양")
    weather_yangpyeong = get_weather(37.4915, 127.6147, "양평")
    news = get_news_summary()

    message = f"""📋 왕기 브리핑 | {date_str}

💱 환율 KRW/USD
{fx}

🌤 날씨
{weather_danyang}
{weather_yangpyeong}

📰 중동 뉴스 헤드라인
{news}

━━━━━━━━━━━━━
🔗 대시보드: https://mr1kwg-wang1.github.io/-/"""

    return message


def send_telegram(text):
    """텔레그램으로 메시지 발송"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    resp = requests.post(
        url,
        json={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"},
        timeout=10,
    )
    resp.raise_for_status()
    print("텔레그램 발송 완료:", resp.json().get("ok"))


if __name__ == "__main__":
    msg = build_message()
    print(msg)  # GitHub Actions 로그에도 출력 (디버깅용)
    send_telegram(msg)
