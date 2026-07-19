# -*- coding: utf-8 -*-
"""v2.4 문안을 hwp 사본에 이관해 조판 분량을 실측하는 시뮬레이터.
사용: python sim_layout.py full|cut
  full = v2.4 전문 + 각주 4개(9pt 시도) + 배너 45mm(8줄)
  cut  = 압축 후보 ①~⑥ 적용 + 배너 40mm(7줄)
측정 기준: 기획서가 5쪽 안에 끝나야 3쪽 규정 충족(3~5쪽).
※ 서식(굵게 등)은 재현하지 않음 — 분량 측정 전용. 제출본 아님.
"""
import sys, io, os, re, shutil, tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pyhwpx import Hwp

SRC = r"C:\Users\HAPPY\Desktop\전시산업\「2026 전시산업 대학생 경진대회」 참가신청 서류_AI명시추가.hwp"
V24 = r"C:\Users\HAPPY\Desktop\전시산업\기획서_양식필드별_최종문안_v2.md"

CUTS = [
    ("문단1", " 무엇을 보러 왔는지, 왜 여기 있어야 하는지 알기 어렵다.", ""),
    ("문단6", " 전시 마스코트는 사전 홍보부터 결과물 카드까지 일관되게 등장시켜 캠페인의 시각적 통일성을 만든다.", ""),
    ("문단9", "특히 중소기업에는 브랜드가 아닌 기술로 첫 평가를 받는 무대가 되며, ", ""),
    ("문단10", " 운영 과정에서 축적되는 기술카드·프롬프트 템플릿·마스코트 등의 자산은 이후 전시에 재사용할 수 있다.", ""),
    ("문단10", " 예컨대 본 전략을 송도컨벤시아 개최 전시에 적용하면, 참여 결과물과 해시태그가 인천·송도 방문 콘텐츠로 확산되어 지역 관광 마케팅과의 연계도 기대할 수 있다.", ""),
]
CAPTION_CUT = "실제 배포·구동 중인 웹 프로토타입(좌 QR)과 마스코트 디자인북(우 QR)을 시연 가능한 상태로 제출합니다."


def load_v24():
    md = io.open(V24, encoding="utf-8").read()
    title = "NO LOGO REMIX — 브랜드는 숨기고, 기술을 발견하다"
    summary = re.search(r"## \[요 약\][^\n]*\n\n(.+?)\n\n---", md, re.S).group(1).strip()
    body_md = re.search(r"## \[기획내용\][^\n]*\n\n(.+?)\n## \[핵심 키워드", md, re.S).group(1)
    blocks = []  # (kind, text) kind: para|banner|caption
    for para in body_md.split("\n\n"):
        para = para.strip()
        if not para:
            continue
        if para.startswith("【"):
            # 배너 지시 줄 — 캡션이 같은 블록에 붙어 있으면 분리
            blocks.append(("banner", ""))
            m = re.search(r"캡션: \*(.+?)\*", para, re.S)
            if m:
                blocks.append(("caption", m.group(1).strip()))
            continue
        if para.startswith("캡션:"):
            blocks.append(("caption", para.replace("캡션:", "").strip().strip("*")))
            continue
        if para.startswith("**") and para.endswith("**"):
            blocks.append(("para", para.strip("*")))
            continue
        para = "\n".join(l for l in para.splitlines() if not l.strip().startswith("【"))
        blocks.append(("para", re.sub(r"\[주[1-4]\]", "", para)))
    foots = []
    for n in range(1, 5):
        m = re.search(r"\*\*\[주%d\]\*\* (.+?)(?=\n\n)" % n, md, re.S)
        foots.append(f"주{n}) " + m.group(1).strip())
    return title, summary, blocks, foots


def replace_cell(hwp, anchor, new_paras):
    """anchor 텍스트가 있는 셀 내용을 통째로 교체. new_paras: 문자열 리스트(문단 단위)."""
    hwp.MoveDocBegin()
    if not hwp.find(anchor):
        raise RuntimeError(f"anchor not found: {anchor[:20]}")
    hwp.Run("Cancel")          # 찾기 선택 해제(캐럿은 셀 안)
    hwp.Run("SelectAll")       # 셀 안에서는 셀 내용만 선택됨
    hwp.Run("Delete")
    for i, p in enumerate(new_paras):
        if i:
            hwp.Run("BreakPara")
        if p:
            hwp.insert_text(p)


def main(mode):
    title, summary, blocks, foots = load_v24()
    banner_lines = 8 if mode == "full" else 7   # 45mm≈8줄, 40mm≈7줄 (10pt·160% 기준)

    if mode == "cut":
        applied = 0
        new_blocks = []
        for kind, text in blocks:
            if kind == "caption":
                new_blocks.append((kind, CAPTION_CUT)); applied += 1; continue
            for _, old, new in CUTS:
                if old in text:
                    text = text.replace(old, new); applied += 1
            new_blocks.append((kind, text))
        blocks = new_blocks
        print(f"압축 적용: {applied}건 (기대 6건 = 문장 5 + 캡션 1)")
        if applied != 6:
            print("!! 경고: 압축 적용 건수가 기대와 다름 — 문안 문자열 확인 필요")

    dst = os.path.join(tempfile.gettempdir(), f"sim_{mode}.hwp")
    shutil.copy2(SRC, dst)
    hwp = Hwp(new=True, visible=False)
    try:
        hwp.open(dst)
        # 1) 제목 (문서 앞에서 첫 매치 = 제목 셀)
        replace_cell(hwp, "NO LOGO REMIX", [title])
        # 2) 요약
        replace_cell(hwp, "브랜드를 가린 기술을 직접 고르고", [summary])
        # 3) 기획내용은 3개 셀로 분할되어 있음: B5(도입~아이디어) / B6(추진방안 본문) / B7(기대효과 본문)
        #    '추진방안'·'기대효과' 소제목은 라벨 열(A6/A7)에 이미 있으므로 본문에 넣지 않는다.
        b5, b6, b7 = [], [], []
        bucket = b5
        for kind, text in blocks:
            if kind == "para" and text == "추진방안":
                bucket = b6; continue
            if kind == "para" and text == "기대효과":
                bucket = b7; continue
            if kind == "banner":
                bucket.extend([""] * banner_lines)   # 배너 자리 빈 줄
            else:
                bucket.append(text)
        replace_cell(hwp, "전시장에 들어선 2030에게", b5)
        # B6 교체 시 기존 각주 2개(QR 링크: '프로토타입 체험하기'/'디자인 시안 보기')의
        # 앵커가 함께 삭제됨 — 실제 이관에서도 배너가 이 QR 각주들을 대체함
        replace_cell(hwp, "사전 단계", b6)
        replace_cell(hwp, "2030 관람객은 기업의 설명을", b7)
        n_gso = 0
        for ctrl in list(hwp.ctrl_list):   # 잔여 그림 개체(QR 이미지) 제거
            if getattr(ctrl, "CtrlID", "") == "gso":
                hwp.delete_ctrl(ctrl); n_gso += 1
        print(f"그림 개체 삭제: {n_gso}개")
        # 4) 각주 4개 — 기획내용 셀 끝에 9pt로 덧붙여 지면 근사
        hwp.MoveDocBegin()
        if not hwp.find("파일럿 운영 첫날부터 곧바로 실측할 수 있다"):
            raise RuntimeError("기획내용 끝 문단을 찾지 못함")
        hwp.Run("Cancel"); hwp.Run("MoveParaEnd")
        nine_pt = False
        try:
            hwp.set_font(Height=9); nine_pt = True
        except Exception:
            pass
        for f in foots:
            hwp.Run("BreakPara"); hwp.insert_text(f)
        print(f"각주 9pt 적용: {nine_pt} (False면 10pt 근사 — 실제보다 약간 크게 측정됨)")
        hwp.save()
        # 5) 측정
        print(f"총 쪽수: {hwp.PageCount}")
        for label, text in [("기획서 시작", "전시장에 들어선 2030에게"),
                            ("기획서 끝(AI명시)", "팀이 직접 수행하였음"),
                            ("동의서 시작", "개인정보 수집, 이용 및 처리업무 위탁 동의서")]:
            hwp.MoveDocBegin()
            if hwp.find(text):
                ki = hwp.KeyIndicator()
                print(f"{label}: {ki[3]}쪽 {ki[5]}줄")
            else:
                print(f"{label}: 못 찾음")
        print(f"저장: {dst}")
        print("판정 기준: 기획서 끝이 5쪽 안이면 3쪽 규정(3~5쪽) 충족")
    finally:
        hwp.quit()


if __name__ == "__main__":
    main(sys.argv[1])

