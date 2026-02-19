---
description: 변경된 파일들을 분석하여 논리적으로 그룹화한 후 각각 별도 커밋으로 푸시합니다
argument-hint: [commit message prefix]
disable-model-invocation: true
allowed-tools: Bash(git:*)
---

# Smart Commit

변경된 파일들을 분석하여 논리적으로 그룹화한 후 각각 별도 커밋으로 푸시합니다.

## 실행 절차

1. `git status`로 변경 파일 목록 확인
2. `git diff`로 각 파일의 변경 내용 분석
3. 변경 사항을 논리적 그룹으로 분류:
   - 같은 기능/모듈 관련 변경
   - 같은 유형의 변경 (버그 수정, 새 기능, 리팩토링, 문서 등)
   - 관련 파일끼리 묶기
4. 각 그룹별로:
   - `git add <해당 파일들>`
   - `git commit -m "<적절한 커밋 메시지>"`
5. 모든 커밋 완료 후 `git push`

## 커밋 메시지 규칙

```
<type>: <설명>

- 상세 내용 1
- 상세 내용 2

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Type 종류

- `feat`: 새 기능
- `fix`: 버그 수정
- `docs`: 문서 변경
- `chore`: 기타 (설정, 구조 등)
- `refactor`: 리팩토링
- `test`: 테스트

## 그룹화 기준

1. **폴더/모듈 기준**: 같은 폴더 내 파일들
2. **목적 기준**: 같은 목적의 변경 (예: docs 관련, src 관련)
3. **의존성 기준**: 서로 의존하는 변경들

## CRLF/LF 줄바꿈 변경 처리

옵시디언 등 에디터에서 파일을 열면 줄바꿈 문자가 자동 변환되어 의도치 않은 변경이 생길 수 있습니다.

### 감지 방법

`git diff --stat` 실행 시 다음 경고가 표시되면 CRLF 변경:
```
warning: LF will be replaced by CRLF in <파일명>
```

### 처리 절차

1. `git diff --stat`으로 실제 변경 내용 확인
2. 줄바꿈만 변경된 파일 식별 (변경 라인 수가 0인 파일)
3. 해당 파일들은 `git restore <파일>` 또는 `git restore <폴더>/`로 복원
4. 실제 내용이 변경된 파일만 커밋 진행

### 예시

```bash
# 상태 확인 - 줄바꿈만 바뀐 파일은 변경 라인 수가 없거나 전체 파일이 바뀜
git diff --stat
# .docs/example.md | 0     ← 줄바꿈만 변경 (복원 대상)
# src/main.py      | 5 ++- ← 실제 변경 (커밋 대상)

# 줄바꿈만 변경된 파일/폴더 복원
git restore .docs/references/
```

## 실행

사용자 확인 없이 자동으로 그룹화하고 커밋/푸시합니다.

$ARGUMENTS가 있으면 커밋 메시지 prefix로 사용합니다.
