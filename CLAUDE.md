# 왕기 대시보드 (dailybriefing 저장소)

이 저장소는 두 개의 서로 다른, 독립적인 용도로 쓰이고 있습니다. 헷갈리기 쉬우니 먼저 이 구분부터 읽으세요.

## 1. index.html — 실시간 개인 대시보드 (계속 사용 중)

GitHub Pages(`pages-build-deployment` 워크플로)로 서빙되는 웹페이지. 시계, KRW/USD 환율, 단양·양평 날씨, 부동산(죽전 벽산블루밍 4단지) 메모, 골프 일정 메모, 미국·국내 증시 카드로 구성. 메모는 브라우저 localStorage에 저장되므로 기기 간 동기화는 안 됨.

## 2. 매일 아침 텔레그램 브리핑 — 실제 발송은 이 저장소를 거치지 않음

**진짜 자동화는 claude.ai의 클라우드 루틴("왕기 대시보드 - 오늘브리핑 자동생성", routine 상세: https://claude.ai/code/routines/trig_0144aVVteiajJz8vgrFprn6X)입니다.** 매일 06:50 KST(cron `50 21 * * *` UTC)에 실행되어, Gmail·Google Calendar를 확인하고 웹 검색으로 뉴스·시세를 모아 브리핑을 작성한 뒤, **Telegram Bot API를 직접 호출해서(chat_id `8500699667`) 발송**합니다. GitHub 커밋이나 push를 전혀 하지 않습니다.

이 루틴이 이렇게 GitHub를 안 거치는 이유: 클라우드 실행 환경(Environment "Default", `env_015FnvcrGMxGGRPFdHf9SVWF`)의 네트워크 정책이 기본값("신뢰됨")일 때 `api.github.com`과 `api.telegram.org` 둘 다 차단되어, git push/GitHub Contents API/GitHub MCP 도구가 전부 403으로 실패했습니다. Environment 설정에서 네트워크 액세스를 **"전체"**로 바꾼 뒤에야 텔레그램 직접 발송이 성공했습니다. (Environment 설정 위치: claude.ai/code 하단 입력창의 "Default" 버튼 → 톱니바퀴 아이콘 → 네트워크 액세스.)

### 이 저장소 안의 dashboard.txt / briefing.py / .github/workflows/daily_briefing.yml — 정리 예정, 지금은 무시

과거에는 이 세 파일이 실제 발송 파이프라인이었습니다(사용자가 매일 아침 claude.ai 채팅으로 dashboard.txt를 작성 → 커밋 → GitHub Actions가 텔레그램 발송). 지금은 위의 클라우드 루틴이 이 역할을 완전히 대체했습니다.

- `dashboard.txt`는 여전히 (별도 경로로) 매일 갱신되고 있지만, 위 클라우드 루틴과는 **무관**합니다.
- `briefing.py`는 2026-07-17에 dashboard.txt 내용을 보내는 대신 "Claude에서 오늘브리핑을 입력하세요"라는 고정 안내 메시지를 보내도록 바뀌었습니다. **이 안내 메시지는 이제 의미가 없습니다** (클라우드 루틴이 이미 자동으로 다 하기 때문) — 무시해도 되고, 사용자가 추후 이 파일들(`dashboard.txt`, `briefing.py`, `.github/workflows/daily_briefing.yml`)을 정리(삭제)할 예정입니다.

### 정리 대기 중인 항목 (아직 실행 안 됨)

- `dashboard-content-writer` fine-grained PAT — 더 이상 안 씀, 폐기 권장
- cron-job.org의 "Daily Briefing Trigger" 크론 잡 — `daily_briefing.yml`의 workflow_dispatch를 호출하던 것, 더 이상 필요 없음
- 위 세 파일(dashboard.txt/briefing.py/daily_briefing.yml) 자체

이 저장소에서 작업할 때는 **"브리핑을 고치자" = 클라우드 루틴을 고치는 것**이지, 이 저장소의 Python/YAML을 고치는 게 아님을 기억하세요.
