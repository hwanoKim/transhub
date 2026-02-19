# Claude Code Plugin Development Guide

플러그인을 만들거나 수정하기 전에 반드시 이 가이드를 따르시오.

**공식 문서**: https://code.claude.com/docs/en/plugins

---

## 목차

1. [플러그인 구조](#플러그인-구조)
2. [plugin.json 매니페스트](#pluginjson-매니페스트)
3. [플러그인 컴포넌트](#플러그인-컴포넌트)
4. [플러그인 설치 및 관리](#플러그인-설치-및-관리)
5. [플러그인 자동 업데이트](#플러그인-자동-업데이트)
6. [마켓플레이스](#마켓플레이스)
7. [환경 변수](#환경-변수)

---

## 플러그인 구조

### 기본 디렉토리 레이아웃

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json          # 필수: 플러그인 매니페스트
├── commands/                # 사용자 실행 명령어 (.md 파일)
├── skills/                  # 모델 자동 호출 스킬
│   └── skill-name/
│       └── SKILL.md
├── agents/                  # 서브에이전트 정의
├── hooks/                   # 이벤트 핸들러
│   └── hooks.json
├── .mcp.json               # MCP 서버 설정
└── .lsp.json               # LSP 서버 설정
```

**중요**: `.claude-plugin/` 디렉토리 안에는 오직 `plugin.json`만 위치합니다. 다른 모든 디렉토리는 플러그인 루트에 위치해야 합니다.

### 지원되지 않는 컴포넌트

플러그인에서는 다음 디렉토리가 **지원되지 않습니다**:

| 디렉토리 | 대안 |
|----------|------|
| `rules/` | Skills의 SKILL.md에 지침 포함 |
| `tasks/` | Skills 또는 Agents로 대체 |
| `.claude/CLAUDE.md` | Skills에 지침 분산 |

**해결 방법**: 프로젝트 규칙(rules)이나 메모리(CLAUDE.md)에 있던 지침은 Skills의 SKILL.md 파일 내에 통합하거나, 관련 Agent 정의에 포함시켜야 합니다.

---

## plugin.json 매니페스트

### 필수 필드

```json
{
  "name": "plugin-name",
  "description": "플러그인에 대한 간단한 설명",
  "version": "1.0.0"
}
```

| 필드 | 타입 | 설명 |
|------|------|------|
| `name` | string | 고유 식별자 (kebab-case, 공백 없음) |
| `description` | string | 플러그인 매니저에서 표시되는 설명 |
| `version` | string | 시맨틱 버전 (예: 1.0.0) |

### 선택적 메타데이터 필드

```json
{
  "author": {
    "name": "작성자 이름",
    "email": "email@example.com",
    "url": "https://github.com/author"
  },
  "homepage": "https://docs.example.com/plugin",
  "repository": "https://github.com/author/plugin",
  "license": "MIT",
  "keywords": ["keyword1", "keyword2"]
}
```

### 컴포넌트 경로 필드

**중요**: `commands/`, `agents/`, `skills/` 디렉토리는 **자동으로 발견**됩니다. `plugin.json`에 명시할 필요가 없습니다.

```json
{
  "hooks": "./hooks/hooks.json"
}
```

| 필드 | 타입 | 설명 |
|------|------|------|
| `hooks` | string | 훅 설정 파일 경로 (유일하게 명시 필요) |

**자동 발견되는 컴포넌트** (이것만 지원됨):

| 디렉토리/파일 | 설명 |
|--------------|------|
| `commands/` | 명령어 파일 (.md) |
| `skills/` | 스킬 디렉토리 (SKILL.md 포함) |
| `agents/` | 에이전트 파일 (.md) |
| `hooks/` | hooks.json 이벤트 핸들러 |
| `.mcp.json` | MCP 서버 설정 |
| `.lsp.json` | LSP 서버 설정 |

**⚠️ 지원되지 않음**: `rules/`, `tasks/`, `.claude/CLAUDE.md` 등 프로젝트 레벨 메모리 구조는 플러그인에서 작동하지 않습니다.

---

## 플러그인 컴포넌트

### Skills (스킬)

**위치**: `skills/<skill-name>/SKILL.md`

```markdown
---
name: skill-name
description: 이 스킬이 언제 사용되는지 설명
allowed-tools: Bash, Read, Grep
disable-model-invocation: false
---

# 스킬 제목

스킬의 상세 지침...
```

**호출**: `/plugin-name:skill-name` 또는 자동 호출

### Commands (명령어)

**위치**: `commands/<command-name>.md`

```markdown
---
description: 명령어에 대한 설명
---

명령어 실행 시 수행할 작업...
$ARGUMENTS를 통해 사용자 입력을 받을 수 있습니다.
```

**호출**: `/plugin-name:command-name [인자]`

### Agents (에이전트)

**위치**: `agents/<agent-name>.md`

```markdown
---
description: 이 에이전트가 전문화된 분야
capabilities: ["task1", "task2"]
---

# 에이전트 이름

상세한 에이전트 설명 및 지침...
```

### Hooks (훅)

**위치**: `hooks/hooks.json`

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "npm run lint:fix $FILE"
          }
        ]
      }
    ]
  }
}
```

**사용 가능한 이벤트**:

| 이벤트 | 설명 |
|--------|------|
| `PreToolUse` | 도구 사용 전 |
| `PostToolUse` | 도구 사용 후 |
| `PostToolUseFailure` | 도구 실패 후 |
| `UserPromptSubmit` | 사용자 프롬프트 제출 시 |
| `SessionStart` | 세션 시작 시 |
| `SessionEnd` | 세션 종료 시 |
| `Stop` | 에이전트 중지 시 |
| `SubagentStart` | 서브에이전트 시작 시 |
| `SubagentStop` | 서브에이전트 중지 시 |
| `PreCompact` | 컨텍스트 압축 전 |
| `Notification` | 알림 발생 시 |

**훅 타입**: `command` (쉘 명령어), `prompt` (Claude에게 전달), `agent` (에이전트 실행)

### MCP Servers

**위치**: `.mcp.json`

```json
{
  "mcpServers": {
    "server-name": {
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/servers/server.js"],
      "env": {
        "API_KEY": "${API_KEY}"
      }
    }
  }
}
```

### LSP Servers

**위치**: `.lsp.json`

```json
{
  "go": {
    "command": "gopls",
    "args": ["serve"],
    "extensionToLanguage": {
      ".go": "go"
    }
  }
}
```

---

## 플러그인 설치 및 관리

### 설치 스코프

| 스코프 | 설정 파일 | 용도 |
|--------|----------|------|
| `user` | `~/.claude/settings.json` | 모든 프로젝트에서 사용 (기본값) |
| `project` | `.claude/settings.json` | 팀 공유 (Git에 포함) |
| `local` | `.claude/.settings.local.json` | 프로젝트 전용 (gitignore) |

### CLI 명령어

```bash
# 마켓플레이스 추가
/plugin marketplace add user/repo
/plugin marketplace add user/repo#branch   # 특정 브랜치

# 플러그인 설치
claude plugin install <plugin> [--scope user|project|local]
/plugin install <plugin-name>@<marketplace-name>

# 플러그인 제거/활성화/비활성화
claude plugin uninstall <plugin>
claude plugin enable <plugin>
claude plugin disable <plugin>

# 플러그인 업데이트
claude plugin update <plugin>

# 로컬 테스트
claude --plugin-dir ./my-plugin
```

---

## 플러그인 자동 업데이트

**모든 hwano의 플러그인은 반드시 자동 업데이트 기능을 포함해야 합니다.**

### 설정 방법

1. `hooks/hooks.json` 파일 생성:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "claude plugin marketplace update hwano-plugins || echo \"[Warning] Plugin update failed - check network or marketplace URL\""
          }
        ]
      }
    ]
  }
}
```

2. `plugin.json`에 hooks 필드 추가:

```json
{
  "name": "plugin-name",
  "description": "...",
  "version": "1.0.0",
  "hooks": "./hooks/hooks.json"
}
```

### 동작 원리

1. 플러그인 설치 시 `plugin.json`에 정의된 훅이 함께 등록
2. Claude Code 세션 시작 시 `SessionStart` 이벤트 발생
3. 훅이 `claude plugin marketplace update` 명령 실행
4. 마켓플레이스에서 최신 버전 확인 후 자동 적용

---

## 마켓플레이스

### marketplace.json 구조

**위치**: `.claude-plugin/marketplace.json` (저장소 루트)

```json
{
  "name": "my-marketplace",
  "owner": {
    "name": "Your Name",
    "email": "email@example.com"
  },
  "metadata": {
    "description": "마켓플레이스 설명",
    "version": "1.0.0",
    "pluginRoot": "./plugins"
  },
  "plugins": [
    {
      "name": "plugin-name",
      "source": "./plugins/plugin-name",
      "description": "플러그인 설명",
      "version": "1.0.0"
    }
  ]
}
```

### 플러그인 소스 타입

**상대 경로**:
```json
{ "name": "my-plugin", "source": "./plugins/my-plugin" }
```

**GitHub 저장소**:
```json
{
  "name": "github-plugin",
  "source": { "source": "github", "repo": "owner/repo", "ref": "v2.0.0" }
}
```

**Git URL**:
```json
{
  "name": "git-plugin",
  "source": { "source": "url", "url": "https://gitlab.com/team/plugin.git", "ref": "main" }
}
```

### 비공개 저장소 인증

| 제공자 | 환경 변수 |
|--------|----------|
| GitHub | `GITHUB_TOKEN` 또는 `GH_TOKEN` |
| GitLab | `GITLAB_TOKEN` 또는 `GL_TOKEN` |
| Bitbucket | `BITBUCKET_TOKEN` |

---

## 환경 변수

| 변수 | 설명 |
|------|------|
| `${CLAUDE_PLUGIN_ROOT}` | 플러그인 디렉토리의 절대 경로 |
| `$ARGUMENTS` | 명령어에 전달된 사용자 입력 |
| `$FILE_PATH` | 훅에서 사용되는 파일 경로 |

---

## 참고 자료

- [공식 플러그인 문서](https://code.claude.com/docs/en/plugins)
- [플러그인 레퍼런스](https://code.claude.com/docs/en/plugins-reference)
- [마켓플레이스 문서](https://code.claude.com/docs/en/plugin-marketplaces)
