# 고고다이브 강습 현황 대시보드

예약 시스템에서 내려받은 "통계분석_그룹수업" 엑셀을 강사별 · 수업종류별 · 강습장별로 월 단위 분석하는 대시보드입니다.

- 대시보드: https://gogodive19-droid.github.io/gogodive-edu-dashboard/ (비밀번호는 노션 허브 페이지에)
- 설계 문서: [docs/superpowers/specs/2026-09-05-edu-dashboard-design.md](docs/superpowers/specs/2026-09-05-edu-dashboard-design.md)

## 매달 자료 반영하는 법

1. 예약 시스템에서 그 달의 "통계분석 > 그룹수업" 엑셀 3개를 내려받습니다.
2. 파일을 `data/raw/` 폴더에 넣습니다. 이름은 자유이지만 `2026-09_1.xlsx` 처럼 월을 붙이면 찾기 쉽습니다.
   이미 있는 파일은 지우지 마세요. 전체 기간 파일이 함께 있어야 합니다.
3. PowerShell에서 아래를 실행합니다. 비밀번호를 물어보면 대시보드 비밀번호를 입력합니다.

```powershell
.\publish.ps1
```

이 명령 하나가 검사 → 집계 → 암호화 → 깃허브 업로드까지 합니다. 1~2분 뒤 대시보드에 새 달이 보입니다.

Claude Code를 쓰는 경우에는 엑셀 3개를 건네며 "9월 자료 반영해줘"라고만 하면 됩니다.

### 새로운 수업명이 생겼을 때

빌드가 이런 메시지와 함께 멈추면 규칙에 없는 수업명이 생긴 것입니다.

```
!! 규칙에 없는 수업명 1종 — build/mapping.py 에 규칙을 추가하세요:
       3  (프리다이빙 특강) 잠실 종합운동장
```

`build/mapping.py` 의 `CLASS_RULES` 나 `VENUE_KEYS` 에 한 줄을 추가하면 됩니다. 어떤 대분류로 넣을지만 정하면 되고, 나머지는 Claude에게 맡겨도 됩니다.

## 숫자 규칙

| 항목 | 규칙 |
|---|---|
| 인원 | `출석` 컬럼. 결석은 뺍니다 |
| 0명 수업 | 횟수·인원에 넣지 않고 "0명 개설" 참고 숫자로만 보여줍니다 |
| 중복 | 같은 수업일시·강사·수업명이 여러 줄이면 출석이 가장 적은 한 줄만 셉니다 |
| 프리다이빙 이론 [LIVE] | 제외 |
| 인원 구간 | 1~10명 각각, 11명 이상은 한 칸 |
| 수업종류 | 대분류 13개(초급·중급·마스터·연습반·코칭반·딥풀 코칭반·체험·머메이드·트레이닝·스쿠버·키즈·모두·대학생), 세부 52개 |
| 딥풀 코칭반 | 용인 딥스테이션·시흥 파라다이브·가평 K26에서 열린 코칭반은 표기와 상관없이 "딥풀 코칭반"으로 따로 셉니다 |
| 강습장 | 21곳. 약칭·오타(용인 딥스, 용입 딥스, 시흥 파라, K26, 부천 MS 등)는 정식 이름으로 합칩니다 |

## 폴더

```
data/raw/        원본 엑셀 (깃허브에 올라가지 않음)
build/mapping.py 수업명 → 수업종류·강습장 규칙
build/build.py   엑셀 → dist/index.html
build/test_mapping.py  규칙 검사  (python build/test_mapping.py)
src/template.html      화면
dist/            평문 결과 (깃허브에 올라가지 않음)
index.html       암호화된 결과 — 깃허브 페이지가 보여주는 파일
publish.ps1      검사 → 집계 → 암호화 → 업로드
```

## 직접 단계별로 하고 싶을 때

```powershell
python build/test_mapping.py      # 규칙 검사
python build/build.py             # dist/index.html 생성
$env:STATICRYPT_PASSWORD = "비밀번호"
npx -y staticrypt@3.5.4 dist/index.html -d . --short --remember 30 --config false
git add -A; git commit -m "데이터 2026-09 까지 반영"; git push
```
