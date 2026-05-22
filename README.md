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
5. 아래 권한(Privileged Gateway Intents) 모두 활성화:
   - ✅ MESSAGE CONTENT INTENT
6. **OAuth2 → URL Generator**에서:
   - Scopes: `bot`
   - Bot Permissions: `Send Messages`, `Embed Links`, `Read Message History`
   - 생성된 URL로 봇을 서버에 초대

## 4. 토큰 설정
`bot.py` 파일을 열어 아래 줄 수정:
```python
DISCORD_TOKEN = "여기에_디스코드_봇_토큰_입력"
```
복사한 토큰으로 교체합니다.

## 5. 봇 실행
```
python bot.py
```

## 사용법
디스코드 채팅창에서:
```
!점심
```
→ 오늘의 점심 메뉴 이미지가 나타납니다!

## 참고
- 메뉴 이미지는 보통 **오전 10시** 이후에 업로드됩니다.
- 10시 이전에 호출하면 전날 메뉴가 나올 수 있습니다.
- 봇을 PC를 끄지 않는 한 계속 실행됩니다 (백그라운드 실행 원하면 별도 안내 가능).
