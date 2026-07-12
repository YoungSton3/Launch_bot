# 🍱 점심봇 설정 가이드

## 1. Python 설치 확인
Python 3.11 이상이 필요합니다.
```
python --version
```

## 2. 패키지 설치
```
pip install -r requirements.txt
```

## 3. 디스코드 봇 토큰 발급
1. https://discord.com/developers/applications 접속
2. **New Application** 클릭 → 이름 입력
3. 좌측 **Bot** 메뉴 → **Add Bot**
4. **Token** 섹션에서 **Reset Token** → 토큰 복사
   - ⚠️ OAuth2 메뉴의 "클라이언트 시크릿(Client Secret)"이 아니라, 반드시 **Bot 메뉴의 Token**입니다.
5. 아래 권한(Privileged Gateway Intents) 모두 활성화:
   - ✅ MESSAGE CONTENT INTENT
6. **OAuth2 → URL Generator**에서:
   - Scopes: `bot`
   - Bot Permissions: `Send Messages`, `Embed Links`, `Read Message History`
   - 생성된 URL로 봇을 서버에 초대

## 4. 토큰 설정
`bot.py`는 토큰을 코드에 직접 넣지 않고 환경변수 `DISCORD_TOKEN`에서 읽습니다. 참고용으로 `.env.example` 파일에 어떤 값이 필요한지 적어뒀습니다 (`.env`는 `.gitignore`에 등록되어 있어 실제 토큰 파일은 커밋되지 않습니다).

**로컬에서 실행할 때:**
```
# Windows PowerShell
$env:DISCORD_TOKEN = "복사한_토큰"

# macOS / Linux
export DISCORD_TOKEN="복사한_토큰"
```
> 참고: 현재 `bot.py`는 `.env` 파일을 자동으로 읽지 않습니다. `.env` 파일을 만들어 자동 로드하고 싶다면 `python-dotenv` 패키지 추가가 필요합니다 (원하시면 설정해드릴 수 있어요).

**Railway에 배포할 때:**
1. Railway 프로젝트 → 실제로 봇이 실행되는 서비스 선택
2. **Variables** 탭 → `DISCORD_TOKEN` 키로 토큰 값 등록
3. 값 저장 후 자동 재배포가 안 되면 **Deployments** 탭에서 수동 Redeploy

## 5. 봇 실행
```
python bot.py
```
Railway 배포 시에는 `Procfile`(`worker: python bot.py`)을 통해 자동 실행됩니다.

## 사용법
디스코드 채팅창에서:
```
!점심
```
→ 오늘의 점심 메뉴 이미지가 나타납니다!
- 운영시간은 평일 **오전 9시 30분 ~ 오후 1시 30분**이며, 그 외 시간에는 안내 메시지가 나갑니다.

또한 평일 매일 **낮 12시 50분**에 지정된 채널로 자동 점심 인사 메시지가 발송됩니다 (주말은 스킵). 채널은 `bot.py`의 `LUNCH_GREETING_CHANNEL_ID`에서 변경할 수 있습니다.

## 참고
- 메뉴 이미지는 보통 **오전 10시** 이후에 업로드됩니다.
- 로컬에서 직접 실행할 경우, 봇을 PC를 끄지 않는 한 계속 실행됩니다. 상시 실행을 원하면 Railway 등 호스팅 서비스에 배포하세요.
