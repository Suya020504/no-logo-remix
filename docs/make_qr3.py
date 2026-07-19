# 기획서 배너용 QR 3종 생성 — 기술구현 / 설명부록 / 캐릭터
# 사용: python 도구/make_qr3.py  → 디자인/새 폴더/ 에 PNG 3개 저장 후 pyzbar로 디코딩 자검
import qrcode
from pyzbar.pyzbar import decode
from PIL import Image
import os

BASE = "https://onboarding-web-one-rose.vercel.app"
OUT = r"C:\Users\HAPPY\Desktop\전시산업\디자인\새 폴더"
TARGETS = [
    ("NOLOGOREMIX_QR_기술구현.png", BASE + "/tech.html"),
    ("NOLOGOREMIX_QR_설명부록.png", BASE + "/docs.html"),
    ("NOLOGOREMIX_QR_캐릭터.png",   BASE + "/mixi.html"),
]

for fname, url in TARGETS:
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    path = os.path.join(OUT, fname)
    img.save(path)
    got = decode(Image.open(path))
    ok = got and got[0].data.decode() == url
    print(("OK  " if ok else "FAIL"), fname, img.size, "->", url)
