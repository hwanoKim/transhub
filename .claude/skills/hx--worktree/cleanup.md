# 워크트리 정리 가이드

## 완료 후 정리 순서

### 1. 워크트리에서 최종 커밋

```bash
cd <worktree-folder>
git add .
git commit -m "feat: 완료"
```

### 2. 메인에서 머지

```bash
cd <project-root>
git merge {branch-name}
```

머지 충돌 시:
```bash
# 충돌 파일 수정 후
git add .
git commit -m "merge: {branch-name} 머지"
```

### 3. 워크트리 제거

```bash
git worktree remove ../{worktree-folder}
```

강제 제거 (uncommitted 변경 있을 때):
```bash
git worktree remove --force ../{worktree-folder}
```

### 4. 브랜치 삭제

```bash
git branch -d {branch-name}
```

강제 삭제 (머지 안 됐을 때):
```bash
git branch -D {branch-name}
```

### 5. Task 완료 처리

```bash
# task 문서를 completed로 이동 (프로젝트별 task 관리 방식에 따름)
```

## 전체 정리 명령어 (예시)

```bash
cd <project-root>

# 머지
git merge textual-cli

# 워크트리 제거
git worktree remove ../project-textual

# 브랜치 삭제
git branch -d textual-cli

# 확인
git worktree list
git branch
```

## 정리 확인

```bash
# 워크트리 목록 (하나만 있어야 함)
git worktree list

# 브랜치 목록 (feature 브랜치 없어야 함)
git branch

# 폴더 확인 (워크트리 폴더 없어야 함)
ls ../
```

## 작업 취소 (머지 안 하고 삭제)

작업 폐기 시:
```bash
cd <project-root>

# 워크트리 강제 제거
git worktree remove --force ../{worktree-folder}

# 브랜치 강제 삭제
git branch -D {branch-name}
```

## 로컬 폴더 정리

`git worktree remove`가 실패하거나 폴더가 남아있을 때:

### 폴더 삭제 시도

```bash
rm -rf ../{worktree-folder}
```

### 파일 사용 중 에러

```
rm: cannot remove 'logs/app.log': Device or resource busy
```

이 에러가 발생하면:

1. **사용자에게 알림**: "워크트리 폴더에 사용 중인 파일이 있어 삭제할 수 없습니다"
2. **안내 메시지**:
   - Windows 탐색기에서 직접 삭제
   - 또는 터미널/프로세스 종료 후 재시도
3. **삭제할 폴더 경로 명시**

### git worktree 연결 해제 확인

```bash
git worktree list
```

- 목록에 없으면 git 연결은 해제됨
- 폴더만 남은 것이므로 안전하게 삭제 가능

## 주의사항

1. **머지 먼저**: 워크트리 제거 전 머지 완료
2. **커밋 확인**: uncommitted 변경 있으면 경고
3. **폴더 잔존**: 워크트리 제거해도 빈 폴더 남을 수 있음 (수동 삭제)
4. **로그파일 잠금**: 앱 실행 중이면 로그파일 삭제 불가
5. **venv 공유**: 워크트리는 메인의 `.venv` 사용 (워크트리 삭제해도 venv는 메인에 있음)
