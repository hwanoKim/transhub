"""비디오에서 오디오를 추출하고 whisper로 텍스트 변환.

Usage:
    python transcribe.py <video_path> [--model medium] [--output path.json]

Output:
    타임스탬프 포함 JSON 파일 (.transcription.json)
"""

import sys
import json
import subprocess
import tempfile
import os
import argparse


def extract_audio(video_path: str, audio_path: str) -> None:
    """ffmpeg로 비디오에서 오디오(WAV) 추출."""
    cmd = [
        "ffmpeg",
        "-i", video_path,
        "-vn",                   # 비디오 제거
        "-acodec", "pcm_s16le",  # PCM 16-bit
        "-ar", "16000",          # 16kHz (whisper 최적)
        "-ac", "1",              # 모노
        "-y",                    # 덮어쓰기
        audio_path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"ffmpeg error: {result.stderr}", file=sys.stderr)
        sys.exit(1)


def transcribe_audio(audio_path: str, model_name: str = "medium") -> dict:
    """whisper로 오디오를 텍스트 변환."""
    import whisper

    print(f"  Loading whisper model: {model_name}")
    model = whisper.load_model(model_name)

    print("  Transcribing...")
    result = model.transcribe(audio_path, verbose=False)
    return result


def main():
    parser = argparse.ArgumentParser(description="비디오 오디오 추출 + STT")
    parser.add_argument("video_path", help="비디오 파일 경로")
    parser.add_argument(
        "--model",
        default="medium",
        choices=["tiny", "base", "small", "medium", "large"],
        help="Whisper 모델 크기 (기본: medium)",
    )
    parser.add_argument("--output", help="출력 JSON 경로 (기본: <비디오명>.transcription.json)")
    args = parser.parse_args()

    video_path = os.path.abspath(args.video_path)

    if not os.path.exists(video_path):
        print(f"Error: 파일을 찾을 수 없습니다: {video_path}", file=sys.stderr)
        sys.exit(1)

    output_path = args.output or os.path.splitext(video_path)[0] + ".transcription.json"

    # Step 1: 오디오 추출
    print(f"[1/2] 오디오 추출: {os.path.basename(video_path)}")
    tmp_audio = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    tmp_audio.close()

    try:
        extract_audio(video_path, tmp_audio.name)

        # Step 2: STT
        print(f"[2/2] 음성 인식 (whisper {args.model})")
        result = transcribe_audio(tmp_audio.name, args.model)

        output = {
            "source": os.path.basename(video_path),
            "language": result.get("language", "unknown"),
            "segments": [
                {
                    "index": i + 1,
                    "start": round(seg["start"], 3),
                    "end": round(seg["end"], 3),
                    "text": seg["text"].strip(),
                }
                for i, seg in enumerate(result["segments"])
            ],
        }

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=2)

        print(f"\nComplete!")
        print(f"  Language: {output['language']}")
        print(f"  Segments: {len(output['segments'])}")
        print(f"  Output: {output_path}")

    finally:
        if os.path.exists(tmp_audio.name):
            os.remove(tmp_audio.name)


if __name__ == "__main__":
    main()
