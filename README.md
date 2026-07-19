# NO LOGO REMIX

> **브랜드는 숨기고, 기술을 발견하다** — 2026 전시산업 대학생 경진대회 출품작 · 팀 **REMIX LAB**

기업명을 가린 기술카드에서 시작해, 실제 부스 방문(QR 토큰)과 AI 창작으로 이어지는 참여형 전시 팝업.
전시 전 SNS 티저 → 전시 중 체험 → 전시 후 공유 콘텐츠 확산으로 2030 관람객 유입을 만드는 **3단 유입 마케팅 전략**입니다.

## 🌐 라이브 페이지 분류

| 분류 | URL | 설명 |
|---|---|---|
| 📱 **어플 페이지** | [/index.html](https://onboarding-web-one-rose.vercel.app/index.html) | 관람객 모바일 여정 P01~P10 전체 (온보딩→미션→블라인드→QR 인증→토큰→AI 리믹스→피드·투표→마이) · 부스 인증 데모 코드 `2026` |
| 📖 **설명 페이지** | [/pitch.html](https://onboarding-web-one-rose.vercel.app/pitch.html) | 발표 소개 — 문제·전략·여정·데모·기대효과 원페이지 |
| 🏗 **전시 기준 예상 시나리오** | [/scenario.html](https://onboarding-web-one-rose.vercel.app/scenario.html) | 실존 전시(2026 그린에너텍, 송도컨벤시아) 적용 시뮬레이션 — 관리자 미션 설계 · 가상 20부스 · 페르소나 4인 실주행 검증 |
| 🔋 **실전 모의 운영 리포트** | [/mock.html](https://onboarding-web-one-rose.vercel.app/mock.html) | 종료된 실존 전시(인터배터리 2026) 공식 디렉토리 620개사 분석 + 실기업 22개사 데이터 페르소나 6인 실주행 — 앱 실전 모드: `?exhibition=IB2026` |
| ⚙️ 기획서 QR① 기술구현 | [/tech.html](https://onboarding-web-one-rose.vercel.app/tech.html) | 심사위원용 1분 체험 코스 + 37초 시연 영상 |
| 📚 기획서 QR② 설명부록 | [/docs.html](https://onboarding-web-one-rose.vercel.app/docs.html) | 30초 요약(문제·해결·증거) + 상세 부록 목차 |
| 🤖 기획서 QR③ 캐릭터 | [/mixi.html](https://onboarding-web-one-rose.vercel.app/mixi.html) | MIXI 캐릭터 영상·네이밍·디자인 컨셉·디자인북 갤러리 |
| 🖥 현장 전광판 (S01) | [/live.html](https://onboarding-web-one-rose.vercel.app/live.html) | 1920×1080 자동 스케일 · 12초 순환 · 라이브 카운터 |
| 📊 기업 대시보드 (S02) | [/dashboard.html](https://onboarding-web-one-rose.vercel.app/dashboard.html) | 참여 퍼널·KPI 산식 (가상 예시 데이터) |
| 📕 마스코트 디자인북 | [/mascot.pdf](https://onboarding-web-one-rose.vercel.app/mascot.pdf) | 캐릭터 MIXI 최종 디자인북 경량판 (2.3MB) — 디자인: 차서빈 |

## 📁 저장소 구조

```
no-logo-remix/
├─ web/                  # 배포 웹 전체 (Vercel · 정적 사이트)
│  ├─ index.html         #   📱 어플 페이지 — 단일 파일 SPA (P01~P10, 바닐라 JS)
│  ├─ pitch.html         #   📖 설명 페이지
│  ├─ scenario.html      #   🏗 전시 기준 예상 시나리오
│  ├─ live.html          #   🖥 현장 전광판 (S01)
│  ├─ dashboard.html     #   📊 기업 대시보드 (S02)
│  ├─ mock.html          #   🔋 실전 모의 운영 리포트 (인터배터리 2026)
│  ├─ tech.html · docs.html · mixi.html  # 기획서 QR ①②③ 랜딩
│  ├─ mixi.png           #   P01 히어로 마스코트
│  ├─ mascot.pdf         #   최종 디자인북 (경량판 2.3MB)
│  └─ assets/            #   마스코트 컷 · 디자인북 갤러리 · 캐릭터/시연 영상 · 스타일 락 결과 · 실주행 캡처
├─ docs/                 # 기획 문서 (번호 순 = 제작 순서)
│  ├─ 01_기능명세서_v2.1.md            # 화면·상태·데이터 상세 명세
│  ├─ 02_기능제안서_v3.1.md            # 디자이너 전달용 기능 요구 (M/S/C)
│  ├─ 03_마케팅평가리포트.md            # 6관점 평가 (63→81점 개선 이력)
│  ├─ 04_자료조사_및_반영내역.md        # 검증된 인용 출처 + 반영 내역
│  ├─ 05_미션_전시연계_검증.md          # 미션 ↔ 실존 전시회 매핑 검증
│  ├─ 06_실사용_운영시나리오_리포트.md   # 그린에너텍 시뮬레이션 + 페르소나 4인 검증
│  ├─ 07_기획서_최종문안_v2.4.md        # 예선 기획서 문안 (hwp 이관용)
│  ├─ 08_모의전시_인터배터리_리포트.md   # 실전 모의 운영 — 620개사 분석·페르소나 6인
│  ├─ 09_예선기획서_3쪽_완성문안_v1.md   # 3쪽 압축 완성 문안
│  ├─ 10_기획서_문안_v2.5B_4쪽절충판.md  # 4쪽 절충판 문안
│  ├─ 11_분량경고_3쪽초과_대비_압축후보.md # 조판 분량 대응 가이드
│  ├─ 12_참가신청서류_검토_수정지시서_v1.md # hwp 서류 검토·수정 지시
│  ├─ 13_본선_해커톤_대비플랜.md         # 본선(송도, 8/12~14) 대비
│  └─ 14_UI_스펙_v1.md                  # 초기 UI 스펙
├─ tools/                # 제작·검증 도구 (Python)
│  ├─ extract_hwp.py / proofread_hwp.py / pagemap_hwp.py  # hwp 텍스트 추출·문안 교정·쪽수 측정
│  ├─ make_qr3.py / make_mascot_qr.py                     # QR 생성 + 디코딩 자검
│  └─ sim_layout.py / sim_v25.py                          # 지면 분량 시뮬레이션
└─ assets/qr/            # 기획서 삽입용 QR 산출물 (개별 3종 + 배너 합성본 + 구버전 2종)
```

## ⚙️ 기술 구성

- **프런트엔드**: 프레임워크 없는 단일 파일 SPA (Vanilla JS, ES5) · Pretendard · 모바일 우선 390×844
- **상태 관리**: 익명 세션 → `localStorage` (새로고침 복원, `?exhibition=` 전시 ID 파라미터)
- **배포**: Vercel 정적 호스팅 — `web/` 폴더에서 `vercel deploy --prod --yes`
- **결과 이미지**: "스타일 락" — 동일한 스튜디오 스타일(배경·받침대·조명 고정)로 사전 생성된 세트 (`web/assets/results/`)
- **분석 설계**: 이벤트 19종(`blind_card_viewed`+체류시간, `qr_verify_success`, `vote_submitted` 등) 세션 내 기록

## ✅ 검증 이력 (요약)

- 인용 통계 — 원문 페이지 이중 검증 (한국전시산업진흥회 국가승인통계·GMI·KCI·언론 보도), 미검증 자료는 표기 후 지면 인용 제외
- 미션 — 실존 전시회(인터배터리·KIMES·로보월드 등) 연계 확인
- 관람객 페르소나 4인(그린에너텍 가상) + 6인(인터배터리 실기업 데이터) — 배포 웹에서 전 여정 실주행, 발견 결함 6건 수정·재검증 (와/과 조사, 커스텀 미션 추천 변별력 등)
- 실전 모의 운영 — 인터배터리 2026 공식 디렉토리 620개사 전수 분석, 사용 22개사 전원 공식 데이터 대조
- 상세: `docs/04~08` 참조

## 👥 팀 REMIX LAB

이연수(팀장) · 김주희(기획) · 최현규(개발) · 차서빈(디자인·마스코트)

---

※ 생성형 AI 활용 범위: 회의내용 구조화·문장 교정, 프로토타입 및 마스코트 시안 제작에 활용했으며, 아이디어 도출과 최종 기획·검토는 팀이 직접 수행함.
※ 대시보드 수치는 가상 예시이며, 운영 시나리오의 참가기업·부스 구성은 가상 시뮬레이션입니다.
