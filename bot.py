import discord
import aiohttp
import re
import os
from datetime import datetime, timezone, timedelta
from discord.ext import commands

# ===== 설정 =====
DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]  # Railway 환경변수에서 읽음
KAKAO_CHANNEL_URL = "https://pf.kakao.com/_xfWxfCxj"
# ================

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


async def get_lunch_image_url() -> str | None:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "ko-KR,ko;q=0.9",
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(KAKAO_CHANNEL_URL, headers=headers) as resp:
            if resp.status != 200:
                print(f"[경고] 페이지 응답 코드: {resp.status}")
                return None
            html = await resp.text()

    patterns = [
        r'<meta\s+property="og:image"\s+content="([^"]+)"',
        r'<meta\s+content="([^"]+)"\s+property="og:image"',
        r'<meta\s+name="twitter:image"\s+content="([^"]+)"',
        r'(https?://[^\s"\']+kakaocdn\.net[^\s"\']+(?:img_[a-z]+|img)\.jpg)',
    ]

    img_url = None
    for pattern in patterns:
        match = re.search(pattern, html)
        if match:
            img_url = match.group(1)
            break

    if not img_url:
        return None

    original_url = re.sub(r"/img_[a-z]+\.jpg", "/img.jpg", img_url)
    return original_url


@bot.event
async def on_ready():
    print(f"✅ 봇 로그인 완료: {bot.user} (ID: {bot.user.id})")
    print("!점심 명령어를 대기 중입니다...")


@bot.command(name="점심")
async def lunch(ctx: commands.Context):
    KST = timezone(timedelta(hours=9))
    now = datetime.now(KST)
    now_total_min = now.hour * 60 + now.minute

    # 오전 10시 이전 → 업로드 전
    if now_total_min < 10 * 60:
        remaining_min = (10 * 60) - now_total_min
        await ctx.send(
            f"⏰ 아직 메뉴 업로드 전이에요!\n"
            f"더좋은밥상은 보통 **오전 10시**에 오늘의 메뉴를 올려요.\n"
            f"> 현재 시각: **{now.strftime('%H:%M')}** — {remaining_min // 60}시간 {remaining_min % 60}분 후에 다시 시도해보세요 🙏"
        )
        return

    # 13시 30분 이후 → 영업 종료
    if now_total_min >= 13 * 60 + 30:
        await ctx.send(
            f"🔒 오늘 영업이 종료됐어요!\n"
            f"더좋은밥상 운영시간은 **~13:30**까지예요.\n"
            f"> 현재 시각: **{now.strftime('%H:%M')}** — 내일 점심도 기대해주세요 😄"
        )
        return

    async with ctx.typing():
        try:
            url = await get_lunch_image_url()
        except aiohttp.ClientConnectorError:
            await ctx.send("❌ 네트워크 오류로 카카오 채널에 접근할 수 없어요.")
            return
        except Exception as e:
            await ctx.send(f"❌ 오류 발생: `{e}`")
            return

    if not url:
        await ctx.send(
            "😢 오늘의 메뉴 이미지를 찾지 못했어요.\n"
            "아직 업로드 전이거나(보통 **오전 10시** 이후) 페이지 구조가 바뀌었을 수 있어요."
        )
        return

    embed = discord.Embed(
        title="🍱 오늘의 점심 메뉴",
        description="📍 더좋은밥상 (대륭17차 구내식당)",
        color=discord.Color.orange(),
    )
    embed.set_image(url=url)
    embed.set_footer(text="출처: 카카오톡 채널 @더좋은밥상 | !점심으로 언제든 호출하세요")
    await ctx.send(embed=embed)


bot.run(DISCORD_TOKEN)
