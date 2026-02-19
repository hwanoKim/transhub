# 프로젝트 개요

breadcrumb: [[index|Transhub]] > [[architecture-index|Architecture]]

## 기능

| 기능 | 설명 | 상태 |
|------|------|------|
| 비디오 자막 생성 | 영상에서 자동으로 한글 자막(SRT) 생성 | 구현 완료 |
| PPT 번역 | PPT를 번역하여 한글 문서 생성 | 예정 |

## 디렉토리 구조

```
transhub/
├── .claude/                          # Claude Code 설정
│   ├── commands/                     # 슬래시 커맨드 정의
│   ├── rules/                        # 프로젝트 룰 (티켓, 워크플로우)
│   └── skills/                       # 스킬 정의
│       └── video-subtitle/           # 비디오 자막 생성 스킬
│           ├── SKILL.md              # 파이프라인 정의 (진입점)
│           └── scripts/
│               ├── transcribe.py     # 음성 추출 + STT
│               └── translate_chunks.py  # 청크 분할/병합
├── .docs/                            # 프로젝트 문서
├── .serena/                          # Serena MCP 언어 서버 설정
├── .tickets/                         # 티켓 기반 작업 관리 (칸반)
│   ├── active/                       # 활성 티켓
│   ├── closed/                       # 완료 티켓 아카이브
│   └── config.yaml                   # 클래스/상태 정의
├── .venv/                            # Python 가상환경
└── requirements.txt                  # Python 의존성
```

## 외부 의존성

| 의존성 | 용도 | 설치 |
|--------|------|------|
| **ffmpeg** | 비디오에서 오디오 추출 | 시스템 설치 필요 |
| **openai-whisper** | 음성 인식 (STT) | `pip install openai-whisper` |
| **Claude Code** | 번역 엔진 (서브에이전트 오케스트레이션) | CLI 도구 |

## 관련 문서

| 문서 | 설명 |
|------|------|
| [[arch-subtitle-pipeline]] | 비디오 자막 파이프라인 상세 |
