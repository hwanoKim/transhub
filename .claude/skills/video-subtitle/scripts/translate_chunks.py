"""대량 세그먼트 청크 분할/병합 유틸리티.

Usage:
    python translate_chunks.py split <transcription.json> [--chunk-size 50] [--output-dir <dir>]
    python translate_chunks.py merge <chunk_dir> <output.srt>

Subcommands:
    split   transcription.json을 청크 JSON 파일들로 분할
    merge   청크별 SRT 파일들을 하나의 최종 SRT로 병합
"""

import sys
import json
import os
import re
import argparse
from pathlib import Path


# --- 노이즈 필터링 ---

# 반복 패턴 (같은 단어/구가 3회 이상 반복)
REPETITION_PATTERN = re.compile(r"^(.{1,20}?)(?:[,.\s]+\1){2,}[,.\s]*$", re.IGNORECASE)

# 의미 없는 감탄사/추임새만으로 구성된 세그먼트
NOISE_WORDS = {
    "hey", "oh", "ah", "uh", "um", "hm", "hmm", "huh",
    "ha", "haha", "wow", "ooh", "aah", "eh", "mhm",
    "oui", "non", "ouais",  # 프랑스어 추임새
}


def is_noise_segment(text: str) -> bool:
    """노이즈 세그먼트 여부 판별."""
    cleaned = text.strip().strip(".,!?").strip()
    if not cleaned:
        return True

    # 단어 분리 후 모두 노이즈 단어인지 확인
    words = re.findall(r"[a-zA-ZÀ-ÿ]+", cleaned.lower())
    if words and all(w in NOISE_WORDS for w in words):
        return True

    # 같은 구절 반복 패턴 ("Hey, hey, hey", "Oh, oh, oh")
    if REPETITION_PATTERN.match(cleaned):
        return True

    return False


# --- split 서브커맨드 ---

def cmd_split(args):
    input_path = Path(args.transcription_json)
    if not input_path.exists():
        print(f"Error: 파일을 찾을 수 없습니다: {input_path}", file=sys.stderr)
        sys.exit(1)

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    segments = data.get("segments", [])
    language = data.get("language", "unknown")
    source = data.get("source", "")
    total = len(segments)

    # 노이즈 필터링
    filtered = [s for s in segments if not is_noise_segment(s["text"])]
    noise_count = total - len(filtered)

    # 출력 디렉토리
    if args.output_dir:
        output_dir = Path(args.output_dir)
    else:
        output_dir = input_path.parent / (input_path.stem.replace(".transcription", "") + "_chunks")
    output_dir.mkdir(parents=True, exist_ok=True)

    # 청크 분할
    chunk_size = args.chunk_size
    chunks = []
    for i in range(0, len(filtered), chunk_size):
        chunk_segments = filtered[i:i + chunk_size]
        chunk_num = len(chunks) + 1
        chunk_file = output_dir / f"chunk_{chunk_num:03d}.json"

        chunk_data = {
            "source": source,
            "language": language,
            "chunk": chunk_num,
            "total_chunks": -1,  # 아래에서 업데이트
            "segments": chunk_segments,
        }
        chunks.append((chunk_file, chunk_data))

    # total_chunks 업데이트 후 저장
    total_chunks = len(chunks)
    for chunk_file, chunk_data in chunks:
        chunk_data["total_chunks"] = total_chunks
        with open(chunk_file, "w", encoding="utf-8") as f:
            json.dump(chunk_data, f, ensure_ascii=False, indent=2)

    # 매니페스트 저장
    manifest = {
        "source": source,
        "language": language,
        "total_segments": total,
        "noise_filtered": noise_count,
        "active_segments": len(filtered),
        "chunk_size": chunk_size,
        "total_chunks": total_chunks,
        "chunks": [
            {
                "chunk": i + 1,
                "file": chunks[i][0].name,
                "segments": len(chunks[i][1]["segments"]),
                "start_index": chunks[i][1]["segments"][0]["index"],
                "end_index": chunks[i][1]["segments"][-1]["index"],
            }
            for i in range(total_chunks)
        ],
    }
    manifest_path = output_dir / "manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    # 결과 출력
    print(f"Split complete!")
    print(f"  Source: {source}")
    print(f"  Language: {language}")
    print(f"  Total segments: {total}")
    print(f"  Noise filtered: {noise_count}")
    print(f"  Active segments: {len(filtered)}")
    print(f"  Chunks: {total_chunks} (size: {chunk_size})")
    print(f"  Output: {output_dir}")


# --- merge 서브커맨드 ---

def parse_srt_timestamp(ts: str) -> float:
    """SRT 타임스탬프 → 초 변환. 예: '00:02:05,340' → 125.34"""
    match = re.match(r"(\d{2}):(\d{2}):(\d{2}),(\d{3})", ts.strip())
    if not match:
        raise ValueError(f"Invalid SRT timestamp: {ts}")
    h, m, s, ms = match.groups()
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000


def format_srt_timestamp(seconds: float) -> str:
    """초 → SRT 타임스탬프 변환. 예: 125.34 → '00:02:05,340'"""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int(round((seconds - int(seconds)) * 1000))
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def parse_srt_file(path: Path) -> list[dict]:
    """SRT 파일 파싱 → [{index, start, end, text}, ...]"""
    content = path.read_text(encoding="utf-8").strip()
    if not content:
        return []

    entries = []
    blocks = re.split(r"\n\n+", content)
    for block in blocks:
        lines = block.strip().split("\n")
        if len(lines) < 3:
            continue
        # 첫 줄: 인덱스, 둘째 줄: 타임스탬프, 나머지: 텍스트
        ts_match = re.match(
            r"(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})",
            lines[1],
        )
        if not ts_match:
            continue
        entries.append({
            "start": parse_srt_timestamp(ts_match.group(1)),
            "end": parse_srt_timestamp(ts_match.group(2)),
            "text": "\n".join(lines[2:]),
        })
    return entries


def cmd_merge(args):
    chunk_dir = Path(args.chunk_dir)
    output_path = Path(args.output_srt)

    if not chunk_dir.exists():
        print(f"Error: 디렉토리를 찾을 수 없습니다: {chunk_dir}", file=sys.stderr)
        sys.exit(1)

    # 청크 SRT 파일 수집 (chunk_001.srt, chunk_002.srt, ...)
    srt_files = sorted(chunk_dir.glob("chunk_*.srt"))
    if not srt_files:
        print(f"Error: {chunk_dir}에 chunk_*.srt 파일이 없습니다.", file=sys.stderr)
        sys.exit(1)

    # 모든 청크 SRT 파싱 + 병합
    all_entries = []
    for srt_file in srt_files:
        entries = parse_srt_file(srt_file)
        all_entries.extend(entries)

    # 타임스탬프 순 정렬
    all_entries.sort(key=lambda e: e["start"])

    # 최종 SRT 작성 (인덱스 재번호)
    lines = []
    for i, entry in enumerate(all_entries, 1):
        start_ts = format_srt_timestamp(entry["start"])
        end_ts = format_srt_timestamp(entry["end"])
        lines.append(f"{i}")
        lines.append(f"{start_ts} --> {end_ts}")
        lines.append(entry["text"])
        lines.append("")

    output_path.write_text("\n".join(lines), encoding="utf-8")

    print(f"Merge complete!")
    print(f"  Chunks merged: {len(srt_files)}")
    print(f"  Total entries: {len(all_entries)}")
    print(f"  Output: {output_path}")


# --- CLI ---

def main():
    parser = argparse.ArgumentParser(description="대량 세그먼트 청크 분할/병합 유틸리티")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # split
    sp_split = subparsers.add_parser("split", help="transcription.json → 청크 JSON 분할")
    sp_split.add_argument("transcription_json", help="transcription.json 경로")
    sp_split.add_argument("--chunk-size", type=int, default=50, help="청크당 세그먼트 수 (기본: 50)")
    sp_split.add_argument("--output-dir", help="출력 디렉토리 (기본: <비디오명>_chunks/)")

    # merge
    sp_merge = subparsers.add_parser("merge", help="청크 SRT → 최종 SRT 병합")
    sp_merge.add_argument("chunk_dir", help="청크 디렉토리 경로")
    sp_merge.add_argument("output_srt", help="출력 SRT 파일 경로")

    args = parser.parse_args()

    if args.command == "split":
        cmd_split(args)
    elif args.command == "merge":
        cmd_merge(args)


if __name__ == "__main__":
    main()
