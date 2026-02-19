"""
.docs 문서 인덱서

기능:
- 전체 스캔 및 인덱스 생성/재생성
- 증분 업데이트 (해시 비교)
- 깨진 링크 탐지

사용법:
    python docs_indexer.py --rebuild   # 전체 인덱스 재생성
    python docs_indexer.py --update    # 증분 업데이트
    python docs_indexer.py --check     # 깨진 링크 탐지

캐시 저장 위치:
    ~/Documents/temp/docs-cache/{프로젝트명}/
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

# 프로젝트 루트 (cwd 기준)
ROOT = Path.cwd()
DOCS_DIR = ROOT / ".docs"

# 캐시 디렉토리: ~/Documents/temp/docs-cache/{project_name}/
CACHE_BASE = Path.home() / "Documents" / "temp" / "docs-cache"
PROJECT_NAME = ROOT.name
CACHE_DIR = CACHE_BASE / PROJECT_NAME
INDEX_FILE = CACHE_DIR / ".docs-index.json"
RESULT_FILE = CACHE_DIR / ".docs-check-result.json"

# [[Target#Section|Alias]] 또는 [[Target\|Alias]] → 'Target'만 추출
# 테이블 내 이스케이프된 파이프(\|)도 처리
LINK_PATTERN = re.compile(r"\[\[([^\]|#\\]+)(?:\\?\||#)?[^\]]*\]\]")


def ensure_cache_dir() -> None:
    """캐시 디렉토리 생성."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)


def compute_hash(file_path: Path, relative_path: str) -> str:
    """파일 경로+내용의 MD5 해시 계산. 폴더 이동도 감지."""
    with open(file_path, "rb") as f:
        content = f.read()
    # 경로 + 내용을 합쳐서 해시 (폴더 이동 감지)
    combined = relative_path.encode("utf-8") + content
    return hashlib.md5(combined).hexdigest()


def compute_content_hash(file_path: Path) -> str:
    """파일 내용만의 MD5 해시 계산. rename 감지용."""
    with open(file_path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


def extract_links(content: str) -> list[str]:
    """마크다운 내용에서 Obsidian 링크 추출."""
    return list(set(LINK_PATTERN.findall(content)))


def get_context_lines(content: str, link: str, context_size: int = 2) -> str:
    """링크가 포함된 줄과 주변 컨텍스트 반환."""
    lines = content.splitlines()
    for i, line in enumerate(lines):
        if f"[[{link}" in line:
            start = max(0, i - context_size)
            end = min(len(lines), i + context_size + 1)
            return "\n".join(lines[start:end])
    return ""


def scan_docs() -> dict[str, dict]:
    """모든 .md 파일 스캔하여 정보 수집."""
    files: dict[str, dict] = {}

    if not DOCS_DIR.exists():
        print(f"⚠️ .docs 폴더가 없습니다: {DOCS_DIR}")
        return files

    for md_file in DOCS_DIR.rglob("*.md"):
        # .으로 시작하는 파일 제외 (숨김 파일)
        if md_file.name.startswith("."):
            continue

        relative_path = md_file.relative_to(ROOT).as_posix()
        content = md_file.read_text(encoding="utf-8")

        files[md_file.name] = {
            "path": relative_path,
            "hash": compute_hash(md_file, relative_path),
            "content_hash": compute_content_hash(md_file),  # rename 감지용
            "links_to": extract_links(content),
            "linked_by": [],  # 나중에 채움
        }

    return files


def build_backlinks(files: dict[str, dict]) -> None:
    """역방향 링크(linked_by) 구축."""
    # 파일명 → 확장자 없는 이름 매핑
    name_to_file = {Path(name).stem: name for name in files}

    for filename, info in files.items():
        source_stem = Path(filename).stem
        for target in info["links_to"]:
            target_file = name_to_file.get(target)
            if target_file and target_file in files:
                if source_stem not in files[target_file]["linked_by"]:
                    files[target_file]["linked_by"].append(source_stem)


def load_index() -> dict | None:
    """기존 인덱스 로드."""
    if INDEX_FILE.exists():
        with open(INDEX_FILE, encoding="utf-8") as f:
            return json.load(f)
    return None


def save_index(index: dict) -> None:
    """인덱스 저장."""
    ensure_cache_dir()
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)


def rebuild_index() -> dict:
    """전체 인덱스 재생성."""
    print("전체 인덱스 재생성 중...")
    print(f"프로젝트: {ROOT}")
    print(f"캐시: {CACHE_DIR}")

    files = scan_docs()
    build_backlinks(files)

    index = {
        "version": "1.0",
        "project": PROJECT_NAME,
        "project_path": str(ROOT),
        "last_scan": datetime.now(timezone.utc).isoformat(),
        "files": files,
    }

    save_index(index)
    print(f"완료: {len(files)}개 파일 인덱싱됨")
    print(f"저장: {INDEX_FILE}")

    return index


def update_index() -> dict:
    """증분 업데이트."""
    old_index = load_index()

    if old_index is None:
        print("기존 인덱스 없음. 전체 재생성합니다.")
        return rebuild_index()

    print("증분 업데이트 중...")

    # 현재 파일 스캔
    current_files = scan_docs()
    old_files = old_index.get("files", {})

    # 변경 감지
    added = []
    modified = []
    deleted = []
    renamed = []

    current_names = set(current_files.keys())
    old_names = set(old_files.keys())

    # 삭제된 파일
    for name in old_names - current_names:
        deleted.append(name)

    # 추가된 파일
    for name in current_names - old_names:
        added.append(name)

    # 수정된 파일
    for name in current_names & old_names:
        if current_files[name]["hash"] != old_files[name]["hash"]:
            modified.append(name)

    # Rename 감지: 삭제+추가 중 content_hash가 같은 쌍 (내용만 비교)
    deleted_hashes = {name: old_files[name].get("content_hash", old_files[name]["hash"]) for name in deleted}
    added_hashes = {name: current_files[name]["content_hash"] for name in added}

    for del_name, del_hash in list(deleted_hashes.items()):
        for add_name, add_hash in list(added_hashes.items()):
            if del_hash == add_hash:
                renamed.append({"from": del_name, "to": add_name})
                deleted.remove(del_name)
                added.remove(add_name)
                del deleted_hashes[del_name]
                del added_hashes[add_name]
                break

    # 역방향 링크 재구축
    build_backlinks(current_files)

    # 인덱스 업데이트
    new_index = {
        "version": "1.0",
        "project": PROJECT_NAME,
        "project_path": str(ROOT),
        "last_scan": datetime.now(timezone.utc).isoformat(),
        "files": current_files,
    }

    save_index(new_index)

    # 결과 출력
    print(f"추가: {len(added)}개")
    print(f"수정: {len(modified)}개")
    print(f"삭제: {len(deleted)}개")
    print(f"이름 변경: {len(renamed)}개")

    if renamed:
        for r in renamed:
            print(f"  {r['from']} → {r['to']}")

    return new_index


def check_links() -> dict:
    """깨진 링크 탐지."""
    index = load_index()

    if index is None:
        print("인덱스 없음. 먼저 --rebuild를 실행하세요.")
        return {"error": "no_index"}

    # 증분 업데이트 먼저 실행
    index = update_index()
    files = index.get("files", {})

    # 파일명 → 확장자 없는 이름 매핑
    existing_names = {Path(name).stem for name in files}

    # 깨진 링크 탐지
    broken_links = []
    duplicate_names = []

    # 파일명 중복 검사
    name_counts = defaultdict(list)
    for name, info in files.items():
        stem = Path(name).stem
        name_counts[stem].append(info["path"])

    for stem, paths in name_counts.items():
        if len(paths) > 1:
            duplicate_names.append({"name": stem, "paths": paths})

    # 깨진 링크 검사
    for filename, info in files.items():
        file_path = ROOT / info["path"]
        content = file_path.read_text(encoding="utf-8")

        for link in info["links_to"]:
            if link not in existing_names:
                context = get_context_lines(content, link)
                broken_links.append(
                    {
                        "source": filename,
                        "source_path": info["path"],
                        "broken_link": link,
                        "context": context,
                    }
                )

    # 결과 출력
    result = {
        "scan_time": datetime.now(timezone.utc).isoformat(),
        "project": PROJECT_NAME,
        "total_files": len(files),
        "broken_links": broken_links,
        "duplicate_names": duplicate_names,
    }

    if broken_links:
        print(f"\n⚠️ 깨진 링크 {len(broken_links)}개 발견:")
        for bl in broken_links:
            print(f"  {bl['source_path']}: [[{bl['broken_link']}]]")
    else:
        print("\n✅ 모든 링크 정상")

    if duplicate_names:
        print(f"\n⚠️ 중복 파일명 {len(duplicate_names)}개:")
        for dn in duplicate_names:
            print(f"  {dn['name']}: {dn['paths']}")

    # JSON 결과 저장
    ensure_cache_dir()
    with open(RESULT_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"\n결과 저장: {RESULT_FILE}")

    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=".docs 문서 인덱서")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--rebuild", action="store_true", help="전체 인덱스 재생성")
    group.add_argument("--update", action="store_true", help="증분 업데이트")
    group.add_argument("--check", action="store_true", help="깨진 링크 탐지")

    args = parser.parse_args()

    if args.rebuild:
        rebuild_index()
    elif args.update:
        update_index()
    elif args.check:
        check_links()


if __name__ == "__main__":
    main()
