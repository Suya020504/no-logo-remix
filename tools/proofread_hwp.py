# -*- coding: utf-8 -*-
"""hwp 조판본을 v2.4 문안과 대조 교정.
사용: python proofread_hwp.py <파일.hwp>
검사: 필드별 문안 일치(퍼지), 각주 4개, AI 활용 명시, [주N]·[__]·【】 잔존물
"""
import sys, io, os, re, difflib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from extract_hwp import extract

V24 = r"C:\Users\HAPPY\Desktop\전시산업\기획서_양식필드별_최종문안_v2.md"

QMAP = {0x2018: "'", 0x2019: "'", 0x201C: '"', 0x201D: '"',
        0x2013: "—", 0x2212: "-", 0x00B7: "·"}

def norm(s):
    s = re.sub(r"\[주[1-4]\]", "", s)            # 각주 마커는 hwp 각주로 대체됨
    s = s.translate(QMAP)
    s = re.sub(r"\s+", " ", s)
    return s.strip()

def load_expected():
    with io.open(V24, encoding="utf-8") as f:
        md = f.read()
    exp = []  # (label, text)
    exp.append(("주제", "전시회, 2030 세대의 핫플이 되다"))
    exp.append(("팀명", "연수와 아이들"))
    exp.append(("제목", "NO LOGO REMIX — 브랜드는 숨기고, 기술을 발견하다"))
    m = re.search(r"## \[요 약\][^\n]*\n\n(.+?)\n\n---", md, re.S)
    exp.append(("요약", m.group(1).strip()))
    body = re.search(r"## \[기획내용\][^\n]*\n\n(.+?)\n## \[핵심 키워드", md, re.S).group(1)
    i = 0
    for para in body.split("\n\n"):
        para = para.strip()
        if not para or para.startswith("【"):
            continue
        if para.startswith("**") and para.endswith("**"):   # 추진방안/기대효과 소제목
            exp.append((f"소제목:{para.strip('*')}", para.strip("*")))
            continue
        if para.startswith("캡션:"):
            exp.append(("배너 캡션", para.replace("캡션:", "").strip().strip("*")))
            continue
        # 편집지시 줄이 문단에 붙은 경우 제거
        para = "\n".join(l for l in para.splitlines() if not l.strip().startswith("【"))
        i += 1
        exp.append((f"기획내용 문단{i}", para))
    exp.append(("핵심 키워드", "블라인드 발견 / AI 리믹스 / 관심 데이터"))
    m = re.search(r"※ 생성형 AI 활용 범위:.+?(?=\n\n)", md, re.S)
    exp.append(("AI 활용 명시", m.group(0).strip()))
    for n in range(1, 5):
        m = re.search(r"\*\*\[주%d\]\*\* (.+?)(?=\n\n)" % n, md, re.S)
        exp.append((f"각주{n}", m.group(1).strip()))
    return exp

def main(path):
    paras = [norm(p) for p in extract(path)]
    paras = [p for p in paras if p]
    joined = " ".join(paras)
    exp = load_expected()
    print(f"=== 교정 리포트: {path}")
    print(f"=== 추출 문단 수: {len(paras)}\n")
    ok = miss =近 = 0
    for label, text in exp:
        t = norm(text)
        # 키워드는 hwp에서 3개 별도 문단일 수 있음 → 통합 텍스트에서 확인
        if label == "핵심 키워드":
            parts = [norm(x) for x in text.split("/")]
            found = all(p in joined for p in parts)
            print(("[OK] " if found else "[누락] ") + label)
            ok += found; miss += (not found)
            continue
        best_r, best_p = 0.0, ""
        for p in paras:
            r = difflib.SequenceMatcher(None, t, p).ratio()
            if r > best_r:
                best_r, best_p = r, p
        if best_r >= 0.985 or t in joined:
            print(f"[OK] {label}")
            ok += 1
        elif best_r >= 0.80:
            近 += 1
            print(f"[유사 {best_r:.0%}] {label} — 차이 확인 필요:")
            sm = difflib.SequenceMatcher(None, t, best_p)
            for tag, i1, i2, j1, j2 in sm.get_opcodes():
                if tag == "replace":
                    print(f"    문안'{t[i1:i2]}' ↔ hwp'{best_p[j1:j2]}'")
                elif tag == "delete":
                    print(f"    hwp에 없음: '{t[i1:i2]}'")
                elif tag == "insert":
                    print(f"    hwp에 추가됨: '{best_p[j1:j2]}'")
        else:
            miss += 1
            print(f"[누락 {best_r:.0%}] {label}")
    print(f"\n=== 합계: OK {ok} / 유사 {近} / 누락 {miss} (총 {len(exp)})")
    # 잔존물 검사
    raw = " ".join(extract(path))
    for pat, why in [(r"\[주[1-4]\]", "[주N] 마커 잔존 — hwp 각주 삽입 후 텍스트 삭제 필요"),
                     (r"\[__\]", "미기입 빈칸 [__] 잔존"),
                     (r"【[^】]*】", "편집지시 【】 잔존 — 지면에서 삭제 필요")]:
        found = re.findall(pat, raw)
        if found:
            print(f"[경고] {why}: {found[:5]}")
    print("\n※ 3쪽 초과 여부는 텍스트 추출로 판단 불가 — 한글 COM 페이지 수 확인 또는 육안 확인 필요")

if __name__ == "__main__":
    main(sys.argv[1])
