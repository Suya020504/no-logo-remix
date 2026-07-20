# 기획서 배너용 QR 3종 생성 — 캐릭터 / 서비스 소개 / 설명부록 (+배너 합성본)
# 사용: python 도구/make_qr3.py  → 디자인/새 폴더/ 에 PNG 저장 후 pyzbar로 디코딩 자검
import qrcode
from qrcode.constants import ERROR_CORRECT_H
from pyzbar.pyzbar import decode
from PIL import Image, ImageDraw, ImageFont
import os

BASE = "https://onboarding-web-one-rose.vercel.app"
OUT = r"C:\Users\HAPPY\Desktop\전시산업\디자인\새 폴더"
TARGETS = [
    ("NOLOGOREMIX_QR_캐릭터.png",     "캐릭터",     BASE + "/mixi.html"),
    ("NOLOGOREMIX_QR_서비스소개.png", "서비스 소개", BASE + "/pitch.html"),
    ("NOLOGOREMIX_QR_설명부록.png",   "설명부록",   BASE + "/docs.html"),
]

# 1) 개별 QR
for fname, label, url in TARGETS:
    qr = qrcode.QRCode(error_correction=ERROR_CORRECT_H, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    path = os.path.join(OUT, fname)
    img.save(path)
    got = decode(Image.open(path))
    ok = got and got[0].data.decode() == url
    print(("OK  " if ok else "FAIL"), fname, img.size, "->", url)

# 1-b) 개별 QR '카드' — QR + 라벨 + 사이트 주소가 한 장에 (기획서·배너 삽입용 완성본)
CQS = 720          # 카드 내 QR 크기
CW, CH = 880, 1060
f_clbl = ImageFont.truetype(r"C:\Windows\Fonts\malgunbd.ttf", 84)
f_curl = ImageFont.truetype(r"C:\Windows\Fonts\malgun.ttf", 30)
PURPLE, INK2 = (67, 56, 242), (98, 100, 108)  # noqa
for fname, label, url in TARGETS:
    card = Image.new("RGB", (CW, CH), "white")
    cd = ImageDraw.Draw(card)
    q = Image.open(os.path.join(OUT, fname)).resize((CQS, CQS), Image.NEAREST)
    card.paste(q, ((CW - CQS) // 2, 60))
    tw = cd.textlength(label, font=f_clbl)
    cd.text(((CW - tw) / 2, 60 + CQS + 40), label, font=f_clbl, fill=PURPLE)
    u = url.replace("https://", "")
    uw = cd.textlength(u, font=f_curl)
    cd.text(((CW - uw) / 2, 60 + CQS + 40 + 108), u, font=f_curl, fill=INK2)
    cpath = os.path.join(OUT, fname.replace("QR_", "QR카드_"))
    card.save(cpath)
    got = decode(card)
    ok = got and got[0].data.decode() == url
    print(("OK  " if ok else "FAIL"), os.path.basename(cpath), card.size)

# 2) 배너 합성본 (3칸 + 라벨 + URL)
QS, GAP, MG, LBL_H = 720, 300, 220, 150
W = MG * 2 + QS * 3 + GAP * 2
H = 160 + QS + 40 + LBL_H + 60
banner = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(banner)
f_lbl = ImageFont.truetype(r"C:\Windows\Fonts\malgunbd.ttf", 92)
f_url = ImageFont.truetype(r"C:\Windows\Fonts\malgun.ttf", 34)
PURPLE, INK2 = (67, 56, 242), (98, 100, 108)  # noqa
for i, (fname, label, url) in enumerate(TARGETS):
    q = Image.open(os.path.join(OUT, fname)).resize((QS, QS), Image.NEAREST)
    x = MG + i * (QS + GAP)
    banner.paste(q, (x, 160))
    tw = d.textlength(label, font=f_lbl)
    d.text((x + (QS - tw) / 2, 160 + QS + 46), label, font=f_lbl, fill=PURPLE)
    u = url.replace("https://", "")
    uw = d.textlength(u, font=f_url)
    d.text((x + (QS - uw) / 2, 160 + QS + 46 + 108), u, font=f_url, fill=INK2)
bp = os.path.join(OUT, "NOLOGOREMIX_QR_배너3종.png")
banner.save(bp)
print("banner saved:", bp, banner.size)
for i, (fname, label, url) in enumerate(TARGETS):
    x = MG + i * (QS + GAP)
    got = decode(banner.crop((x, 160, x + QS, 160 + QS)))
    print("banner-check", label, "->", got[0].data.decode() if got else "DECODE FAIL")
