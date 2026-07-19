# -*- coding: utf-8 -*-
"""HWP 5.0 텍스트 추출 (olefile + zlib). 사용: python extract_hwp.py <파일.hwp> [출력.txt]"""
import sys, io, zlib, struct
import olefile

HWPTAG_PARA_TEXT = 0x10 + 51  # 67

def iter_records(data):
    pos, n = 0, len(data)
    while pos + 4 <= n:
        (hdr,) = struct.unpack_from("<I", data, pos)
        tag = hdr & 0x3FF
        size = (hdr >> 20) & 0xFFF
        pos += 4
        if size == 0xFFF:
            (size,) = struct.unpack_from("<I", data, pos)
            pos += 4
        yield tag, data[pos:pos + size]
        pos += size

def para_text(payload):
    # UTF-16LE; 제어문자(코드 0~31)는 종류별로 8/16바이트 등 추가 데이터 보유
    out = []
    i, n = 0, len(payload)
    while i + 2 <= n:
        (ch,) = struct.unpack_from("<H", payload, i)
        if ch == 0 or ch == 13:      # null / 문단 끝
            i += 2
        elif ch in (1, 2, 3, 11, 12, 14, 15, 16, 17, 18, 21, 22, 23):
            i += 16                   # 확장/인라인 제어: 16바이트
        elif ch in (4, 5, 6, 7, 8, 19, 20):
            i += 16
        elif ch == 9:                 # 탭
            out.append("\t"); i += 16
        elif ch == 10:                # 줄바꿈
            out.append("\n"); i += 2
        elif ch in (24, 25, 26, 27, 28, 29, 30, 31):
            i += 2
        else:
            out.append(chr(ch)); i += 2
    return "".join(out)

def extract(path):
    ole = olefile.OleFileIO(path)
    sections = sorted(
        (e for e in ole.listdir() if e[0] == "BodyText"),
        key=lambda e: int(e[1].replace("Section", "")),
    )
    paras = []
    for entry in sections:
        raw = ole.openstream(entry).read()
        try:
            data = zlib.decompress(raw, -15)
        except zlib.error:
            data = raw
        for tag, payload in iter_records(data):
            if tag == HWPTAG_PARA_TEXT:
                t = para_text(payload)
                if t.strip():
                    paras.append(t)
    ole.close()
    return paras

if __name__ == "__main__":
    src = sys.argv[1]
    paras = extract(src)
    text = "\n".join(paras)
    if len(sys.argv) > 2:
        with io.open(sys.argv[2], "w", encoding="utf-8") as f:
            f.write(text)
        print(f"OK: {len(paras)} paragraphs -> {sys.argv[2]}")
    else:
        sys.stdout.buffer.write(text.encode("utf-8"))
