# 워크트리 작업 흐름

## 작업 위치 구분

| 작업 | 위치 | 브랜치 |
|------|------|--------|
| Task 문서 관리 | `project/` | master |
| 코드 구현 | `project-{feature}/` | feature |
| 테스트 실행 | `project-{feature}/` | feature |
| 진행상황 업데이트 | `project/` | master |

## 전형적인 작업 흐름

### 1. Task 문서 생성 (메인)

```bash
cd <project-root>
# task 문서 생성 (프로젝트별 task 관리 방식에 따름)
```

Task 문서에 워크트리 정보 포함:
```markdown
## 워크트리 정보

- 메인: `project/` (master)
- 작업: `project-{feature}/` ({branch-name})
```

### 2. 워크트리에서 구현

```bash
cd <worktree-folder>

# 코드 수정
# 테스트 실행

# 커밋
git add .
git commit -m "feat: ..."
```

### 3. 진행상황 업데이트 (메인)

```bash
cd <project-root>
# task 문서의 체크리스트 업데이트
```

### 4. 반복

워크트리 <-> 메인 오가며 작업

## 커밋 전략

### 워크트리에서 커밋

```bash
cd <worktree-folder>
git add .
git commit -m "feat: 기능 구현"
```

### 메인에서 커밋 (task 문서)

```bash
cd <project-root>
git add .task/
git commit -m "docs: task 진행상황 업데이트"
```

## 파일 공유

워크트리 간 공유되는 것:
- `.git/` (저장소 메타데이터)
- 원격 설정

워크트리 간 독립적인 것:
- 작업 디렉토리 (파일들)
- 브랜치 상태
- staged 파일

## 주의사항

1. **Task는 메인에서만**: 워크트리에서 task 수정하면 충돌 위험
2. **커밋 분리**: 워크트리 작업과 task 문서 커밋 분리
3. **브랜치 확인**: 작업 전 현재 브랜치 확인 (`git branch`)
