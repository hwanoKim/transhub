---
title: 자막 후처리 커맨드
class: coding
status: closed
category: video
priority: normal
tags: [video, subtitle, command, fix, post-processing]
relations:
  parent: "20260219-0704-[main]-subtitle-quality-system"
  follows: ["20260219-1448-video-subtitle-chunking-pipeline"]
---

## Goal

완성된 자막 파일을 도메인 지식 기반으로 수정하는 커맨드를 만든다. 사용자가 자막을 보다가 수정이 필요한 부분을 발견하면, 커맨드 하나로 도메인 DB를 참조하여 자막을 다듬을 수 있다.

### 사용 예시

```
/video-subtitle-fix <자막경로> <요청사항>

예:
/video-subtitle-fix c:/video.srt "hk는 영웅왕으로 통일해줘"
/video-subtitle-fix c:/video.srt "존댓말로 바꿔줘"
/video-subtitle-fix c:/video.srt "3번째 자막부터 10번째까지 다시 번역해줘"
```

### 동작 흐름

1. 자막 파일(.srt) 읽기
2. 내용에서 도메인 파악 (게임개발, 기술 회의 등)
3. 해당 도메인의 참고 자료 DB 로드
4. 사용자 요청사항 + DB 정보를 기반으로 자막 수정
5. 수정된 자막 덮어쓰기 (또는 별도 파일로 저장)

### 도메인 파악 → DB 연결

```
자막 읽기
  → 키워드/문맥 분석 → 도메인 판별
  → 참고 자료 DB 로드 (예: windless/)
  → DB에서 관련 용어/고유명사 조회
  → 요청사항 반영하여 수정
```

## Progress
- [x] 커맨드 이름/인터페이스 확정 → `video-subtitle-fix`
- [x] 커맨드 파일 작성 (`.claude/commands/video-subtitle-fix.md`)
- [x] 도메인 자동 판별 로직 (Step 3)
- [x] 참고 자료 DB 연동 (refdb YAML 스키마 반영)
- [x] staff.yaml 연동: 팀원 이름 첫 언급 시 `이름(역할)` 형식
- [x] 파이프라인 재설계: 요청 유형별 3전략 분기 (기계적 치환 / 범위 지정 / 전체 의미 수정)
      - [x] 전략 A: Grep + Python 일괄 치환 (SRT Read 불필요)
      - [x] 전략 B: 범위만 Read → Edit
      - [x] 전략 C: 규모별 분기 (≤100 직접 / 101+ 청크 병렬)
- [x] 테스트

## Attempts
| # | Method | Result | Notes |
|---|--------|--------|-------|

## Commits
- Git: `5e5dc9c` - feat: 자막 후처리 커맨드 + 참고 자료 DB

## Notes
- 참고 자료 DB(sub 티켓)가 먼저 구축되어야 완전한 기능이 가능하지만, DB 없이도 기본 수정 기능은 동작 가능
- 커맨드 이름 후보: `/video-subtitle-fix`, `/subtitle-fix`, `/video-subtitle-refine`
