# 문서 구조

## 4개 분류 기준

| 폴더 | 내용 | 예시 |
|------|------|------|
| **architecture/** | 시스템 전체 설계, 데이터 흐름, 아키텍처 결정 | arch-overview, data-flow, project-structure |
| **components/** | 개별 모듈, 기능 단위 문서 | database, api, ui-components, bots |
| **dev-guides/** | 개발 환경, 워크플로우, 설정 가이드 | vscode-setup, migration, testing |
| **references/** | 리서치, 토론, 샌드박스 (고정) | research/, discussions/, sandbox/ |

## 폴더 구조 상세

```
.docs/
├── index.md                    # 루트 인덱스
│
├── architecture/               # 아키텍처
│   ├── architecture-index.md
│   ├── arch-overview.md
│   └── {topic}/                # 큰 주제는 서브폴더
│       └── {topic}-index.md
│
├── components/                 # 컴포넌트
│   ├── components-index.md
│   ├── {component}.md
│   └── {component-group}/      # 관련 컴포넌트 그룹
│       └── {group}-index.md
│
├── dev-guides/                 # 개발 가이드
│   ├── dev-guides-index.md
│   ├── {guide}.md
│   └── {topic}/                # 주제별 서브폴더
│       └── {topic}-index.md
│
└── references/                 # 참고자료 (고정 구조)
    ├── ref-index.md
    │
    ├── research/               # 리서치
    │   ├── ref-research-index.md
    │   ├── {YYYYMM}/           # 월별 폴더
    │   │   └── {YYYYMMDD}-{title}.md
    │   └── {topic}/            # 주제별 폴더 (선택)
    │       └── {topic}-index.md
    │
    ├── discussions/            # AI 토론
    │   ├── ref-discussions-index.md
    │   └── {YYYYMMDD}-{title}.md
    │
    └── sandbox/                # 실험적 아이디어
        ├── ref-sandbox-index.md
        └── {YYYYMM}/
            └── {YYYYMMDD}-{title}.md
```

## 파일명 규칙

| 종류 | 형식 | 예시 |
|------|------|------|
| 일반 문서 | `{name}.md` | `arch-overview.md` |
| 인덱스 | `{folder}-index.md` | `architecture-index.md` |
| Research | `{YYYYMMDD}-{title}.md` | `20260123-api-design.md` |
| Discussion | `{YYYYMMDD}-{title}.md` | `20260123-auth-flow.md` |

**공통 규칙:**
- 소문자, 하이픈만 사용
- **파일명 중복 절대 금지** (Obsidian은 파일명으로만 연결)
- 의미 있는 접두사로 구분 (arch-, comp-, dev- 등)

## 인덱스화 규칙

문서가 복잡해지면 **인덱스화**를 적용합니다.

### 인덱스화란?

내용이 많은 문서를 링크 허브로 전환하고, 실제 내용은 하위 문서로 분리하는 방식입니다.

### 적용 기준

| 상황 | 처리 |
|------|------|
| 단순한 문서 (50줄 미만) | 그대로 유지 |
| 복잡한 문서 (여러 섹션) | 인덱스화 적용 |

### 인덱스화 방법

1. 기존 파일명에 `-index` 서픽스 추가 (예: `backtest.md` → `backtest-index.md`)
2. 각 섹션을 별도 문서로 분리 (예: `backtest-tax.md`, `backtest-session.md`)
3. 인덱스 페이지는 **링크 테이블만** 포함
4. **상위 인덱스의 링크 업데이트** (아래 참조)

### 상위 링크 업데이트 (필수)

인덱스화 후 상위 인덱스에서 해당 문서를 가리키는 링크도 함께 업데이트해야 합니다.

**변환 규칙:**
```
# Before (일반 문서)
| [[backtest]] | 백테스팅 엔진 |

# After (인덱스화 후)
| [[backtest-index\|backtest]] | 백테스팅 엔진 |
```

**주의사항:**
- 표시 이름은 기존과 동일하게 유지 (`|backtest` 부분)
- Obsidian 테이블 안에서 파이프(`|`)는 `\|`로 이스케이프 필수

### 인덱스화 체크리스트

- [ ] 인덱스 파일 생성 (`{name}-index.md`)
- [ ] 하위 문서 분리
- [ ] 기존 파일 삭제
- [ ] **상위 인덱스 링크 업데이트** ← 누락 주의

### 인덱스 페이지 규칙

**허용:**
- 제목
- 브레드크럼 (상단/하단)
- 한 줄 설명
- 링크 테이블

**금지:**
- 원칙, 개요, 구조 설명 (별도 문서로)
- 긴 설명문
- 코드 블록
- 상세 내용

### ✅ 좋은 예시 - `portfolio-index.md` (19줄)

```markdown
# 포트폴리오

[[index|H-Board]] > 포트폴리오

## 문서

| 문서 | 설명 |
|------|------|
| [[portfolio-overview]] | 역할, 구조, 관련 문서 |
| [[portfolio-models]] | 데이터 모델 |
| [[portfolio-returns]] | 수익률 계산 |

---

[[index|H-Board]] > 포트폴리오
```

### ❌ 나쁜 예시 - `backtest.md` (159줄)

```markdown
# 백테스팅

## 역할
- 전략 백테스팅 실행...

## 세금 처리              ← 별도 문서로: backtest-tax.md
미국 주식 양도소득세...
(상세 내용 50줄)

## 세션 저장              ← 별도 문서로: backtest-session.md
백테스트 결과는...
(상세 내용 30줄)
```

## 새 문서 추가 절차

1. 적절한 폴더 선택 (4개 분류 기준 참고)
2. 고유한 파일명 확인 (중복 검사)
3. 문서 생성 (브레드크럼 포함)
4. **반드시 해당 인덱스에 링크 추가**
5. 복잡한 주제면 서브폴더 + 서브인덱스 생성
