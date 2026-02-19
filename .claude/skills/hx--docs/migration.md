# 기존 문서 마이그레이션

**적용일**: 2026-01-23

이 문서는 기존 프로젝트의 docs 구조를 새 표준 구조로 마이그레이션할 때 참조합니다.

## 마이그레이션 원칙

1. **기존 내용 존중** - 내용 수정 최소화
2. **점진적 이동** - 한 번에 전체 이동하지 않음
3. **사용자 승인** - 구조 변경은 반드시 확인 후 진행
4. **링크 유지** - 이동 시 기존 링크 깨지지 않도록

## 구조 매핑

### 기존 → 새 구조

| 기존 위치 | 새 위치 | 비고 |
|-----------|---------|------|
| `dev-env/` | `dev-guides/` | 폴더명 변경 |
| `guides/` | `dev-guides/` | 병합 |
| `architecture/` | `architecture/` | 유지 |
| `components/` | `components/` | 유지 |
| `references/research/` | `references/research/` | 유지 |
| `references/discussions/` | `references/discussions/` | 유지 |
| `references/sandbox/` | `references/sandbox/` | 유지 |
| `references/licenses/` | `references/licenses/` | 프로젝트별 유지 |

## 마이그레이션 절차

### 1. 현황 파악

```bash
# 기존 docs 구조 확인
find .docs -type f -name "*.md" | head -50
```

### 2. 불일치 감지

현재 구조가 표준과 다른 경우:

```
[구조 불일치 감지]

현재 구조:
.docs/
├── dev-env/          ← dev-guides/로 권장
├── guides/           ← dev-guides/로 병합 권장
└── references/

권장 구조:
.docs/
├── dev-guides/       ← dev-env + guides 통합
└── references/

마이그레이션 진행하시겠습니까?
1. 전체 마이그레이션
2. 개별 파일씩
3. 나중에
```

### 3. 파일 이동

```markdown
## 이동 예정 파일

| 현재 | 이동 후 | 상태 |
|------|---------|------|
| dev-env/overview.md | dev-guides/overview.md | 대기 |
| dev-env/vscode/ | dev-guides/vscode/ | 대기 |

진행하시겠습니까? (Y/N)
```

### 4. 브레드크럼 마이그레이션

레거시 브레드크럼(상단/하단 반복)을 `breadcrumb:` 메타데이터 형식으로 일괄 변환.

**스크립트 실행:**

```bash
node "${CLAUDE_PLUGIN_ROOT}/skills/docs/scripts/migrate-breadcrumb.js" .docs
```

**변환 규칙:**
1. `# Title` 직후의 `[[...]] > ...` 라인 → `breadcrumb: [[...]] > ...` (마지막 segment 제거)
2. 하단의 동일 브레드크럼 라인 + 인접 `---` 구분선 제거
3. breadcrumb 없는 문서(index.md 등)는 스킵
4. 이미 `breadcrumb:` 있는 문서는 스킵

**수동 수정** (파일 이동 후):

```markdown
# Before
breadcrumb: [[index|Project]] > [[dev-env-index|Dev Env]]

# After
breadcrumb: [[index|Project]] > [[dev-guides-index|Dev Guides]]
```

### 5. 인덱스 업데이트

- 기존 인덱스 파일명 변경 (dev-env-index → dev-guides-index)
- 루트 index.md 링크 업데이트

## 특수 케이스

### licenses 폴더

DCC 프로젝트의 `references/licenses/`는 프로젝트 특성상 유지:

```
references/
├── research/
├── discussions/
├── sandbox/
└── licenses/        # DCC 전용, 유지
```

### 주제별 research 폴더

기존 주제별 폴더 (claude-code/, motion-generation/ 등)는 유지하되, 새 문서는 월별 폴더 우선:

```
research/
├── ref-research-index.md
├── 202601/                 # 새 문서는 월별
├── claude-code/            # 기존 주제별 유지
└── motion-generation/      # 기존 주제별 유지
```

## 마이그레이션 체크리스트

- [ ] 기존 구조 파악
- [ ] 불일치 항목 목록 작성
- [ ] 사용자에게 마이그레이션 안내
- [ ] 승인 받은 항목만 이동
- [ ] 브레드크럼 업데이트
- [ ] 인덱스 업데이트
- [ ] 링크 검증
