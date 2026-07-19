import qrcode
qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
qr.add_data("https://onboarding-web-one-rose.vercel.app/mascot.pdf")
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")
out = r"C:\Users\HAPPY\Desktop\전시산업\디자인\새 폴더\NOLOGOREMIX_마스코트QR.png"
img.save(out)
print("saved:", out, "size:", img.size)
