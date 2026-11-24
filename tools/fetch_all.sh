#!/bin/sh
# 위키미디어 요청 제한을 지키며 소리 → 데이터 → 앱에 넣을 이미지 → 데이터 재생성 → 링크 검사 순서로 실행
cd "$(dirname "$0")/.." || exit 1
python3 tools/fetch_sounds.py; python3 tools/build.py && python3 tools/fetch_local.py && python3 tools/build.py && python3 tools/check_links.py --save
