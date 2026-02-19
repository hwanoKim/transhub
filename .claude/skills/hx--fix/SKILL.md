---
name: hx--fix
description: .docs 문서 검사/수정. 깨진 링크, 브레드크럼 오류 탐지. "문서 검사해줘", "깨진 링크 찾아줘", "브레드크럼 수정해줘" 등에 PROACTIVELY 사용.
---

# fix 스킬

.docs 폴더의 문서들을 규칙에 맞게 검사하고 수정합니다.

## 캐시 위치

```
~/Documents/temp/docs-cache/{프로젝트명}/
├── .docs-index.json        # 파일 해시 인덱스
└── .docs-check-result.json # 검사 결과
```

## 스크립트 실행

**반드시 스크립트를 사용하여 검사합니다. 직접 Glob/Grep 금지.**

```bash
python "${CLAUDE_PLUGIN_ROOT}/skills/fix/scripts/docs_indexer.py" --check
```

| 옵션 | 설명 |
|------|------|
| `--rebuild` | 전체 인덱스 재생성 |
| `--update` | 증분 업데이트 |
| `--check` | 깨진 링크 탐지 (추천) |

## 워크플로우

### 인덱스 없을 때

```
캐시에 .docs-index.json 없음?
    ↓
스크립트 --rebuild 실행
    → 전체 파일 스캔 → 해시 저장
```

### 일반 검사

```
[Step 1] 스크립트 --check 실행
    ↓
[Step 2] .docs-check-result.json 읽기
    → 깨진 링크 없음 → "모든 링크 정상" 출력 후 종료
    → 깨진 링크 있음 → Step 3으로
    ↓
[Step 3] broken_links의 source_path만 Read
    → 토큰 최소화
    ↓
[Step 4] Edit으로 수정
    ↓
[Step 5] 스크립트 --update 실행
    ↓
[Step 6] 결과 보고
```

## 상세 문서

| 문서 | 설명 |
|------|------|
| [check.md](check.md) | 검사 실행 워크플로우 |
| [fix.md](fix.md) | 수정 워크플로우 |

## 오탐 처리

### 무시해야 할 케이스

| 유형 | 예시 | 이유 |
|------|------|------|
| 코드 블록 내 | `[["time", "value"]]` | Python 리스트 등 |
| 이미지 파일 | `[[image.jpg]]` | .md 아님 |
| 예시 텍스트 | `[[파일명]]`, `[[링크]]` | 플레이스홀더 |
| 외부 링크 | `[[http://...]]` | URL |

## 금지 사항

1. **직접 Glob/Grep 금지** - 스크립트가 검사 담당
2. **파일 전체 읽기 금지** - context 기반 최소 읽기
3. **추측 수정 금지** - 확실하지 않으면 사용자에게 질문

## 출력 형식

```markdown
## /docs:fix 완료

### 수정 사항

| 파일 | 수정 내용 |
|------|-----------|
| index.md | 깨진 링크 수정: [[old]] → [[new]] |

### 경고 (수동 확인 필요)

- [ ] `aaa.md`: 대상 파일 불명확
```
