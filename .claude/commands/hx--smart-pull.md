---
description: 원격 저장소에서 변경 사항을 안전하게 가져오고 현재 상태를 분석합니다
disable-model-invocation: true
allowed-tools: Bash(git:*)
---

# Smart Pull

원격 저장소에서 변경 사항을 안전하게 가져옵니다. 현재 상태를 분석하고 필요한 안내를 제공합니다.

## 실행 절차

### 1. 현재 상태 분석

다음 명령어들을 **병렬로** 실행하여 상태 파악:

```bash
git status                           # 로컬 변경 사항
git stash list                       # stash 목록
git log --oneline -5                 # 최근 로컬 커밋
git fetch origin                     # 원격 최신화
```

### 2. 원격과 비교

fetch 후 실행:

```bash
git log HEAD..origin/main --oneline    # 받을 커밋 목록
git log origin/main..HEAD --oneline    # 푸시 안 된 로컬 커밋
```

### 3. 상태별 처리

#### Case A: 로컬 변경 없음 + 원격에 새 커밋 있음
- `git pull origin main` 실행
- 받은 커밋 요약 출력

#### Case B: 로컬에 커밋되지 않은 변경 있음
- 경고 메시지 출력
- 선택지 제안:
  1. `git stash` 후 pull, 다시 `git stash pop`
  2. 먼저 커밋 후 pull
  3. 변경 사항 확인만

#### Case C: 푸시 안 된 로컬 커밋 있음 + 원격에도 새 커밋 있음
- 충돌 가능성 안내
- 선택지 제안:
  1. `git pull --rebase` (권장 - 깔끔한 히스토리)
  2. `git pull` (머지 커밋 생성)
  3. 상황만 확인

#### Case D: 이미 최신 상태
- "이미 최신 상태입니다" 안내
- 최근 커밋 몇 개 보여주기

### 4. Pull 후 안내

성공 시:
- 받은 커밋 수와 요약
- 변경된 파일 목록
- stash가 있었다면 pop 여부 확인

## 출력 형식

```
Pull 상태 분석
------------------------------

현재 브랜치: main
로컬 상태: [깨끗함 / 변경 있음 (N개 파일)]

원격 상태:
  - 받을 커밋: N개
  - 푸시 안 된 커밋: N개

[상황에 따른 안내 메시지]
------------------------------
```

## 안전 규칙

- 강제 명령 사용 금지 (`--force`, `--hard` 등)
- 충돌 발생 시 자동 해결하지 않고 사용자에게 안내
- stash 사용 시 항상 pop 여부 확인
