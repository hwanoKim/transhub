# 워크트리 설정 가이드

## 설정 명령어

```bash
# 메인 프로젝트 폴더에서 실행
cd <project-root>

# 1. 브랜치 생성
git branch {branch-name}

# 2. 워크트리 추가
git worktree add ../{worktree-folder} {branch-name}
```

## 예시

```bash
# textual-cli 작업용
git branch textual-cli
git worktree add ../project-textual textual-cli

# refactor 작업용
git branch refactor-db
git worktree add ../project-refactor refactor-db
```

## 폴더 구조 결과

```
projects/
├── my-project/           # master (메인)
├── my-project-textual/   # textual-cli 브랜치
└── my-project-refactor/  # refactor-db 브랜치
```

## 설정 확인

```bash
# 워크트리 목록 확인
git worktree list
```

출력 예시:
```
C:/projects/my-project           322cd2f [master]
C:/projects/my-project-textual   322cd2f [textual-cli]
```

## .venv 공유 (Python 프로젝트)

워크트리는 같은 Git 저장소를 공유하므로:
- `.venv/`는 메인 폴더에만 존재
- 워크트리에서 실행 시 메인의 `.venv` 사용

```bash
# 워크트리에서 실행
cd <worktree-folder>
..\<project>\.venv\Scripts\python.exe -m pytest tests/
```

## 주의사항

1. **같은 브랜치 체크아웃 불가**: 워크트리로 사용 중인 브랜치는 다른 곳에서 체크아웃 불가
2. **폴더 위치**: 반드시 `../{folder}` 형태로 상위에 생성
3. **브랜치 먼저**: `git branch` 후 `git worktree add`
