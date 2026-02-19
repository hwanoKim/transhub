---
name: hx--command-writing
description: Claude Code 커맨드(슬래시 명령어)를 작성하거나 수정할 때 사용합니다. "커맨드 만들어줘", "슬래시 명령어 작성해줘" 요청에 트리거.
---

# Command Writing Guide

커맨드(슬래시 명령어)를 만들거나 수정하기 전에 반드시 이 가이드를 따르시오.

**공식 문서**: https://code.claude.com/docs/en/slash-commands

## 커맨드 위치

| 스코프 | 위치 | 용도 |
|--------|------|------|
| 프로젝트 | `.claude/commands/<name>.md` | 프로젝트 전용 |
| 개인 | `~/.claude/commands/<name>.md` | 모든 프로젝트에서 사용 |
| 플러그인 | `<plugin>/commands/<name>.md` | 플러그인 배포용 |

- 파일명이 커맨드 이름이 됨 (예: `review.md` → `/review`)
- 하위 폴더 가능 (예: `commands/frontend/component.md` → `/component`)

상세 가이드는 [command-guide.md](command-guide.md) 참조.

## 필수 체크리스트

1. **부작용이 있는 커맨드**는 반드시 `disable-model-invocation: true` 설정
2. **description**은 명확하게 작성 (Claude가 자동 호출 판단에 사용)
3. **allowed-tools**로 필요한 도구만 허용
4. SKILL.md와 commands/*.md는 동일하게 동작함 (Skills가 더 많은 기능 지원)
