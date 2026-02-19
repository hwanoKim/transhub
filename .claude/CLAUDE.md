# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Transhub는 다양한 자동 번역 작업을 위한 프로젝트입니다:
- 영상에 자동으로 한글 자막 삽입
- PPT를 번역하여 한글 문서 생성
- 기타 자동 번역/로컬라이제이션 워크플로우

**언어**: Python
**원격 리포지토리**: https://github.com/hwanoKim/transhub

## Repository Structure

```
transhub/
├── .claude/          # Claude Code 설정 (에이전트, 커맨드, 룰, 스킬)
│   └── skills/
│       └── video-subtitle/   # 비디오 자막 생성 스킬
├── .serena/          # Serena MCP 언어 서버 설정
├── .tickets/         # 티켓 기반 작업 관리 (칸반)
│   ├── active/       # 활성 티켓
│   ├── closed/       # 완료 티켓 아카이브
│   └── config.yaml   # 클래스/상태 정의
├── .venv/            # Python 가상환경
└── requirements.txt  # Python 의존성
```

## Python Virtual Environment

프로젝트 전체에서 하나의 가상환경(`.venv`)을 사용합니다. 기능별로 분리하지 않습니다.

- **위치**: 프로젝트 루트 `.venv/`
- **활성화**: `source .venv/Scripts/activate` (Windows git bash)
- **Python 실행**: `.venv/Scripts/python` (venv 활성화 없이 직접 실행 가능)
- **패키지 설치**: `.venv/Scripts/pip install <패키지>`
- **의존성 추적**: `requirements.txt` — 새 패키지 설치 후 반드시 업데이트
- 스킬/커맨드에서 Python 스크립트 실행 시 반드시 `.venv/Scripts/python` 사용

## Ticket System

이 프로젝트는 `.tickets/` 기반 칸반 시스템으로 작업을 관리합니다.

- **코드 변경 전 반드시 티켓 확인/생성**
- 새 티켓은 `backlog` 상태로 생성, 사용자 지시 시 진행
- 클래스별 워크플로우는 `.claude/rules/class-rules.md` 참조

## Serena MCP

Serena 언어 서버가 활성화되어 있습니다. 심볼 단위 코드 탐색/수정에 활용합니다.
세션 시작 시 프로젝트 활성화 필요: `activate_project(".")`
