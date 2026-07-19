# -*- coding: utf-8 -*-
"""hwp 파트별 시작 쪽 + 총 쪽수. 사용: python pagemap_hwp.py <파일.hwp>"""
import sys, shutil, os, tempfile
from pyhwpx import Hwp

src = sys.argv[1]
tmp = os.path.join(tempfile.gettempdir(), "pagemap_" + os.path.basename(src))
shutil.copy2(src, tmp)
markers = [
    ("참가신청서", "참가팀명"),
    ("기획서 시작", "블라인드 발견"),   # 핵심 키워드(기획서 마지막 표)로도 확인
    ("기획서 첫 문단", "전시장에 들어선 2030에게"),
    ("동의서 시작", "개인정보 수집, 이용 및 처리업무 위탁 동의서"),
]
hwp = Hwp(new=True, visible=False)
try:
    hwp.open(tmp)
    print(f"총 쪽수: {hwp.PageCount}")
    for label, text in markers:
        hwp.MoveDocBegin()
        if hwp.find(text):
            print(f"{label} ('{text[:12]}...'): {hwp.current_page}쪽")
        else:
            print(f"{label}: 못 찾음")
finally:
    hwp.quit()
    try: os.remove(tmp)
    except OSError: pass
