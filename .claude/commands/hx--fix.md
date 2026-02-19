---
description: .docs 문서 검사/수정 - 깨진 링크, 브레드크럼 오류 탐지
argument-hint: [check|fix|rebuild]
---

# 문서 검사/수정

$ARGUMENTS

## 사용법

```
/docs:fix           # 검사 실행 (기본값)
/docs:fix check     # 검사만
/docs:fix fix       # 검사 후 수정
/docs:fix rebuild   # 인덱스 재생성
```

**스킬 참조**: 상세 워크플로우는 `fix` 스킬 참조

1. 스크립트로 검사 실행
2. 결과 파일 분석
3. 필요시 수정 진행

캐시 위치: `~/Documents/temp/docs-cache/{프로젝트명}/`
