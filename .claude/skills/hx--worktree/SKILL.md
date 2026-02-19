---
name: hx--worktree
description: 워크트리 분리 작업. "워크트리 나눠서", "브랜치 분리해서", "별도 폴더에서 작업" 요청 시 사용.
---

# 워크트리 분리 작업 스킬

## 사용 시점

- "워크트리 나눠서 해줘"
- "브랜치 분리해서 작업해줘"
- "별도 폴더에서 작업해줘"
- 기존 코드와 충돌 없이 실험적 작업이 필요할 때

## 핵심 개념

```
project/              # master (메인 - 사용자가 보는 곳)
project-{feature}/    # {feature} 브랜치 (작업 폴더)
```

**사용자는 메인 폴더만 봄** - task 문서, 진행상황 모두 메인에서 관리

## 수행 절차

### 1. 워크트리 설정

```bash
cd <project-root>
git branch {branch-name}
git worktree add ../{worktree-folder} {branch-name}
```

### 2. Task 문서 생성

**메인 폴더**에 task 문서 생성 (있는 경우)

### 3. 워크트리에서 구현

**워크트리 폴더**에서 실제 코드 작업

### 4. 완료 후 정리

```bash
cd <project-root>
git merge {branch-name}
git worktree remove ../{worktree-folder}
git branch -d {branch-name}
```

## 참조 문서

| 문서 | 설명 |
|------|------|
| [[setup]] | 워크트리 설정 상세 |
| [[workflow]] | 작업 흐름 상세 |
| [[cleanup]] | 완료 후 정리 방법 |

## 핵심 규칙

| 위치 | 용도 |
|------|------|
| `project/` | task 문서 관리 (master) |
| `project-{feature}/` | 코드 작업 (feature 브랜치) |

## 금지 사항

1. 메인 폴더에서 실험적 코드 직접 수정
2. 워크트리 폴더에서 task 문서 수정
3. 머지 없이 워크트리 삭제 (작업 손실)
