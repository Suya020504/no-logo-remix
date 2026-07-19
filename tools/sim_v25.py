# -*- coding: utf-8 -*-
"""임의 문안(JSON)을 hwp 사본에 이관해 분량 실측.
사용: python sim_v25.py <문안.json> [출력태그]
JSON 구조: {"title": str, "summary": str, "b5": [문단...], "b6": [문단...], "b7": [문단...]}
b6 안의 "__BANNER__" 항목은 배너 자리(빈 줄 7개 = 40mm)로 치환됨.
"""
import sys, io, os, json, shutil, tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pyhwpx import Hwp

SRC = r"C:\Users\HAPPY\Desktop\전시산업\「2026 전시산업 대학생 경진대회」 참가신청 서류_AI명시추가.hwp"
FOOTS = [
    "주1) 한국전시산업진흥회, 「2024년 전시산업통계조사 결과」(국가승인통계). 2024년 개최 736건, 참관객 9,530,953명. 참관객은 국적·유형(바이어/일반)별로만 집계됨. akei.or.kr",
    "주2) 엠브레인 트렌드모니터, 「2024 팝업스토어 방문 경험 및 인식 조사」(전국 만 19~59세 1,000명, 2024.12.). 방문 경험률 81.4%(2023년 75.6%), 인지도 20대 71.2%·30대 60.0%, '체험형 팝업스토어 확대 희망' 동의율 73.0%. trendmonitor.co.kr",
    "주3) 뉴시스(2026.3.20.) 및 불교일보(2026.4.8.), 서울국제불교박람회 사무국 발표 보도. 사전등록 2023년 11,187명 → 2026년 44,365명, 총 방문 약 25만 명 중 20~30대 73%.",
    "주4) 뉴스핌(2022.7.25.), 서울교통공사 발표 보도. 2019년 모바일 스탬프 투어 시행 성과.",
]


def replace_cell(hwp, anchor, new_paras):
    hwp.MoveDocBegin()
    if not hwp.find(anchor):
        raise RuntimeError(f"anchor not found: {anchor[:20]}")
    hwp.Run("Cancel")
    hwp.Run("SelectAll")
    hwp.Run("Delete")
    for i, p in enumerate(new_paras):
        if i:
            hwp.Run("BreakPara")
        if p:
            hwp.insert_text(p)


def main(json_path, tag="v25"):
    spec = json.load(io.open(json_path, encoding="utf-8"))
    b6 = []
    for p in spec["b6"]:
        if p == "__BANNER__":
            b6.extend([""] * 7)     # 배너 40mm 근사
        else:
            b6.append(p)
    dst = os.path.join(tempfile.gettempdir(), f"sim_{tag}.hwp")
    shutil.copy2(SRC, dst)
    hwp = Hwp(new=True, visible=False)
    try:
        hwp.open(dst)
        replace_cell(hwp, "NO LOGO REMIX", [spec["title"]])
        replace_cell(hwp, "브랜드를 가린 기술을 직접 고르고", [spec["summary"]])
        replace_cell(hwp, "전시장에 들어선 2030에게", spec["b5"])
        replace_cell(hwp, "사전 단계", b6)
        replace_cell(hwp, "2030 관람객은 기업의 설명을", spec["b7"])
        n_gso = 0
        for ctrl in list(hwp.ctrl_list):
            if getattr(ctrl, "CtrlID", "") == "gso":
                hwp.delete_ctrl(ctrl); n_gso += 1
        # 각주 4개(9pt 근사) — B7 끝에
        hwp.MoveDocEnd
        last = spec["b7"][-1]
        hwp.MoveDocBegin()
        if not hwp.find(last[-20:]):
            raise RuntimeError("B7 끝 문단을 찾지 못함")
        hwp.Run("Cancel"); hwp.Run("MoveParaEnd")
        try:
            hwp.set_font(Height=9)
        except Exception:
            pass
        for f in FOOTS:
            hwp.Run("BreakPara"); hwp.insert_text(f)
        hwp.save()
        print(f"총 쪽수: {hwp.PageCount}")
        for label, text in [("기획서 끝(AI명시)", "팀이 직접 수행하였음"),
                            ("동의서 시작", "개인정보 수집, 이용 및 처리업무 위탁 동의서")]:
            hwp.MoveDocBegin()
            if hwp.find(text):
                ki = hwp.KeyIndicator()
                print(f"{label}: {ki[3]}쪽 {ki[5]}줄")
        body = "".join(spec["b5"] + [p for p in spec["b6"] if p != "__BANNER__"] + spec["b7"])
        print(f"본문 공백제거: {len(body.replace(' ', '').replace(chr(10), ''))}자")
        print(f"저장: {dst}")
        print("판정: 기획서 끝이 5쪽 안이면 3쪽 충족 / 6쪽 안이면 4쪽")
    finally:
        hwp.quit()


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "v25")
