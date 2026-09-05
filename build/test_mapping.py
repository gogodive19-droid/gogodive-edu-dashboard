# -*- coding: utf-8 -*-
"""정규화 규칙·파이프라인 검증.  실행: python build/test_mapping.py  (pytest 도 가능)"""
import glob
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mapping import NO_VENUE, UnmappedClassName, parse_class_name  # noqa: E402
import build  # noqa: E402

CASES = {
    "(초급1강) 잠실 종합운동장": ("초급", "초급 1강", "잠실 종합운동장"),
    "(초급 1강) 시흥 파라다이브": ("초급", "초급 1강", "시흥 파라다이브"),
    "(용인 딥스) 초급2강": ("초급", "초급 2강", "용인 딥스테이션"),
    "(용입 딥스) 중급/마스터 연습반": ("딥풀 자율연습반", "딥풀 자율연습반", "용인 딥스테이션"),
    "(시흥 파라) 중급/마스터 자율연습반": ("딥풀 자율연습반", "딥풀 자율연습반", "시흥 파라다이브"),
    "(자율연습반) 잠실 종합운동장": ("자율연습반", "자율연습반", "잠실 종합운동장"),
    "(자율연습반) 용인 딥스테이션": ("자율연습반", "자율연습반", "용인 딥스테이션"),
    "(중급 연습반)부산 북항마리나": ("자율연습반", "자율연습반", "부산 북항마리나"),
    "(스쿠버｜연습반)오산 TSN": ("스쿠버", "스쿠버 연습반", "오산 TSN"),
    "(용인 딥스테이션) (중급1강 렁스트레칭, 스테틱)": ("중급", "중급 1강 (렁스트레칭·스테틱)", "용인 딥스테이션"),
    "(시흥 파라) (중급1강 렁스트레징, 스테틱)": ("중급", "중급 1강 (렁스트레칭·스테틱)", "시흥 파라다이브"),
    "(가평 K26) (중급 3강 프리폴)": ("중급", "중급 3강 (중성부력·프리폴)", "가평 K26"),
    "(시흥 파라) (마스터 부이 운용법)": ("마스터", "마스터 5강 (부이 운용법)", "시흥 파라다이브"),
    "(용인 딥스) (마스터 부이 연습반)": ("딥풀 자율연습반", "딥풀 자율연습반", "용인 딥스테이션"),
    "(시흥 파라) 마스터": ("마스터", "마스터 (기타)", "시흥 파라다이브"),
    "(시흥 파라) (마스터 EFR)": ("마스터", "마스터 EFR", "시흥 파라다이브"),
    "(용인 딥스) 초급 3강(AIDA)": ("초급", "초급 3강(AIDA)", "용인 딥스테이션"),
    "(부천 MS) 초급 2강": ("초급", "초급 2강", "부천 MS잠수풀"),
    "(코칭반) 오산TSN": ("코칭반", "코칭반", "오산 TSN"),
    "(코칭반) 잠실 종합운동장": ("코칭반", "코칭반", "잠실 종합운동장"),
    "(용인 딥스) 코칭반": ("딥풀 코칭반", "딥풀 코칭반", "용인 딥스테이션"),
    "(시흥 파라) 코칭반": ("딥풀 코칭반", "딥풀 코칭반", "시흥 파라다이브"),
    "(가평 K26) 코칭반": ("딥풀 코칭반", "딥풀 코칭반", "가평 K26"),
    # 초급 상품 파일의 코칭반은 딥풀 강습장에서 열려도 일반 코칭반
    "(코칭반) 시흥 파라다이브": ("코칭반", "코칭반", "시흥 파라다이브"),
    "(코칭반) 용인 딥스테이션": ("코칭반", "코칭반", "용인 딥스테이션"),
    "(대학생 | 코칭반) 잠실 올림픽공원": ("대학생", "대학생 코칭반", "잠실 올림픽공원"),
    "(연습반) 오산 TSN 오산입니다": ("자율연습반", "자율연습반", "오산 TSN"),
    "(연습반) 잠실 올림픽공원**": ("자율연습반", "자율연습반", "잠실 올림픽공원"),
    "(베이직) 머메이드 오산TSN": ("머메이드", "베이직 머메이드", "오산 TSN"),
    "(어드밴스 머메이드 2강) 용인 딥스테이션": ("머메이드", "어드밴스 머메이드 2강", "용인 딥스테이션"),
    "(스쿠버｜오픈워터 1강/체험)잠실 종합운동장": ("스쿠버", "스쿠버 오픈워터 1강/체험", "잠실 종합운동장"),
    "(스쿠버 | 오픈워터1강/체험) 잠실 올림픽공원": ("스쿠버", "스쿠버 오픈워터 1강/체험", "잠실 올림픽공원"),
    "(스쿠버｜오픈워터 1강)시흥 파라다이브": ("스쿠버", "스쿠버 오픈워터 1강/체험", "시흥 파라다이브"),
    "(스쿠버 | 어드벤스)용인 딥스테이션": ("스쿠버", "스쿠버 어드밴스", "용인 딥스테이션"),
    "(스쿠버) 레스큐": ("스쿠버", "스쿠버 레스큐", NO_VENUE),
    "(스쿠버) EFR": ("스쿠버", "스쿠버 EFR", NO_VENUE),
    "(스쿠버 ｜ 스페셜티) 핀킥부수기": ("스쿠버", "스쿠버 스페셜티", NO_VENUE),
    "(모두 3강)대전 알프스다이빙 / 180분 / 4명": ("모두", "모두 3강", "대전 알프스다이빙"),
    "(모두 1강) DIT서면풀장": ("모두", "모두 1강", "DIT 서면풀장"),
    "(키즈 원데이 체험)  시흥 파라다이브": ("키즈", "키즈 원데이 체험", "시흥 파라다이브"),
    "(키즈 프리다이버 코스 4강) K26": ("키즈", "키즈 프리다이버 코스 4강", "가평 K26"),
    "(대학생 | 초급 1강) 잠실 올림픽공원": ("대학생", "대학생 초급 1강", "잠실 올림픽공원"),
    "(시흥 파라) 딥 트레이닝 코스 4-5강": ("트레이닝", "딥 트레이닝 코스 4-5강", "시흥 파라다이브"),
    "(시흥 파라) 딥 트레이닝 코스 연습반": ("트레이닝", "딥 트레이닝 연습반", "시흥 파라다이브"),
    "(초급1강) 두류수영장": ("초급", "초급 1강", "두류수영장"),
    "(코칭반)부천 MS 다이빙풀": ("코칭반", "코칭반", "부천 MS잠수풀"),
}


def test_cases():
    for raw, want in CASES.items():
        got = parse_class_name(raw)
        assert tuple(got) == want, "%r → %r (기대 %r)" % (raw, tuple(got), want)


def test_excluded():
    assert parse_class_name("프리다이빙 이론 [LIVE]") is None


def test_unmapped_raises():
    try:
        parse_class_name("(알수없음) 어딘가")
    except UnmappedClassName:
        return
    raise AssertionError("UnmappedClassName 이 나야 함")


def _raw_paths():
    return sorted(glob.glob(os.path.join(build.RAW_DIR, "*.xlsx")))


def test_full_files():
    paths = _raw_paths()
    if not paths:
        print("  (data/raw 없음 → 전체 파일 검증 건너뜀)")
        return
    raw = build.load_raw_rows(paths)
    rows, removed = build.dedupe(raw)
    records, excluded, unmapped = build.normalize(rows)
    assert not unmapped, "규칙에 없는 수업명: %s" % dict(unmapped)
    # 2024-01~2026-08 초기 3개 파일 기준 수치 (이후 월이 추가되면 행수만 >= 로 확인)
    assert len(raw) >= 31318
    if len(raw) == 31318:
        assert removed == 58, removed
        assert excluded == 191, excluded
        assert len(records) == 31318 - 58 - 191, len(records)
        bigs = Counter(r["b"] for r in records)
        # 코칭반 4208 - 중복 1 = 4207 → 딥풀 상품 파일 표기 1117 + 일반 3090
        assert bigs["딥풀 코칭반"] == 1117, bigs["딥풀 코칭반"]
        assert bigs["코칭반"] == 3090, bigs["코칭반"]
        # 연습반 계열: 딥풀 상품 표기 2190, 일반 4734 - 중복 44 = 4690
        assert bigs["딥풀 자율연습반"] == 2190, bigs["딥풀 자율연습반"]
        assert bigs["자율연습반"] == 4690, bigs["자율연습반"]
        assert "연습반" not in bigs
        assert bigs["체험"] == 839 and bigs["모두"] == 610 and bigs["키즈"] == 244
        venues = {r["v"] for r in records}
        assert len(venues) == 21, sorted(venues)
    # 중복 규칙: 낮은 인원이 남는다
    key = ("2026-08-12 18:30", "임현섭", "(자율연습반) 잠실 종합운동장")
    low = [n for dt, i, name, n in rows if (dt, i, name) == key]
    assert low == [2], low


def test_aggregate_roundtrip():
    paths = _raw_paths()
    if not paths:
        return
    rows, _ = build.dedupe(build.load_raw_rows(paths))
    records, _, _ = build.normalize(rows)
    data = build.aggregate(records, paths)
    assert sum(c[5] for c in data["cells"]) == len(records)
    total_people = sum(c[4] * c[5] for c in data["cells"])
    assert total_people == sum(r["n"] for r in records)
    assert data["bigs"][0] == "초급"


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    fails = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print("ok   ", name)
            except AssertionError as e:
                fails += 1
                print("FAIL ", name, "-", e)
    sys.exit(1 if fails else 0)
