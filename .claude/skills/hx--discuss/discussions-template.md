# 토론 문서 템플릿

토론 내용을 문서화할 때 사용하는 템플릿입니다.

## 문서 저장

**docs 스킬 호출하여 저장 위치 결정:**

```
.docs/references/discussions/{YYYYMMDD}-{title}.md
```

## 템플릿

```markdown
# {주제}

[[index|Project]] > [[ref-discussions-index|Discussions]] > {주제}

---

**토론일**: YYYY-MM-DD
**참여 AI**: Claude, Gemini / Claude, Codex

## 배경

{토론을 시작하게 된 맥락}

## 질문/요청

{사용자가 요청한 내용}

## 토론 내용

### Claude 분석

{Claude의 초기 분석}

### {Gemini/Codex} 의견

{다른 AI의 응답}

### 추가 논의

{필요시 추가 라운드}

## 결론

{합의점 또는 최종 결론}

## 액션 아이템

- [ ] {후속 작업 1}
- [ ] {후속 작업 2}

---

[[index|Project]] > [[ref-discussions-index|Discussions]] > {주제}
```

## 문서화 절차

1. 토론 완료 후 내용 정리
2. docs 스킬의 discussions 도메인 참조
3. 적절한 파일명 생성: `{YYYYMMDD}-{title}.md`
4. 위 템플릿으로 문서 작성
5. `ref-discussions-index.md` 업데이트

## 예시

```markdown
# API 인증 방식 검토

[[index|H-Board]] > [[ref-discussions-index|Discussions]] > API 인증 방식 검토

---

**토론일**: 2026-01-23
**참여 AI**: Claude, Gemini

## 배경

새로운 API 엔드포인트에 적용할 인증 방식 결정 필요.

## 질문/요청

JWT vs Session 기반 인증 중 어떤 것이 적합한지 검토 요청.

## 토론 내용

### Claude 분석

현재 시스템은 마이크로서비스 구조로, stateless한 JWT가 적합해 보임.

### Gemini 의견

JWT 추천. 다만 토큰 갱신 전략(refresh token)과 보안 고려사항 제시:
- Access token 만료 시간 15분 권장
- Refresh token은 HttpOnly 쿠키로 저장
- 토큰 블랙리스트 구현 고려

## 결론

JWT 방식 채택. Gemini 제안대로 refresh token 전략 적용.

## 액션 아이템

- [ ] JWT 라이브러리 선정
- [ ] Refresh token 로직 구현
- [ ] 토큰 블랙리스트 Redis 저장소 설정

---

[[index|H-Board]] > [[ref-discussions-index|Discussions]] > API 인증 방식 검토
```
