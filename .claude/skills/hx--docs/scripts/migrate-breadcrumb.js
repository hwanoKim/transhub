#!/usr/bin/env node
/**
 * 레거시 브레드크럼 → breadcrumb: 메타데이터 형식으로 마이그레이션
 *
 * 사용법: node scripts/migrate-breadcrumb.js <docs-root-path>
 * 예시:   node scripts/migrate-breadcrumb.js ./vscode-extension-test/.docs
 *
 * 변환 규칙:
 * 1. # Title 아래의 [[...]] > ... 라인 → breadcrumb: [[...]] > ... (마지막 segment 제거)
 * 2. 하단의 동일 브레드크럼 라인 제거
 * 3. 브레드크럼 인접 --- 구분선 제거
 * 4. breadcrumb이 없는 문서는 스킵
 */

const fs = require('fs');
const path = require('path');

const docsRoot = process.argv[2];
if (!docsRoot) {
  console.error('Usage: node scripts/migrate-breadcrumb.js <docs-root-path>');
  process.exit(1);
}

const resolvedRoot = path.resolve(docsRoot);
if (!fs.existsSync(resolvedRoot)) {
  console.error(`Directory not found: ${resolvedRoot}`);
  process.exit(1);
}

// 레거시 브레드크럼 패턴: [[...]] > ... 형태
const BREADCRUMB_PATTERN = /^\[\[.+?\]\]\s*>/;

// .md 파일 재귀 수집
function collectMdFiles(dir) {
  const results = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      results.push(...collectMdFiles(full));
    } else if (entry.name.endsWith('.md')) {
      results.push(full);
    }
  }
  return results;
}

// 마지막 segment 제거: "[[a|A]] > [[b|B]] > Current" → "[[a|A]] > [[b|B]]"
function removeLastSegment(breadcrumbLine) {
  // > 로 split하고 마지막 제거
  const parts = breadcrumbLine.split(/\s*>\s*/);
  if (parts.length <= 1) return breadcrumbLine; // segment가 1개면 그대로
  parts.pop(); // 마지막 (현재 페이지) 제거
  return parts.join(' > ');
}

function migrateFile(filePath) {
  const content = fs.readFileSync(filePath, 'utf8');
  const lines = content.split('\n');

  // 이미 breadcrumb: 메타데이터가 있으면 스킵
  if (lines.some(l => /^breadcrumb:\s*/.test(l))) {
    return { status: 'skip', reason: 'already migrated' };
  }

  // 상단 브레드크럼 찾기 (보통 line index 2, # Title 아래 빈 줄 다음)
  let topBcIdx = -1;
  for (let i = 0; i < Math.min(lines.length, 10); i++) {
    if (BREADCRUMB_PATTERN.test(lines[i].trim())) {
      topBcIdx = i;
      break;
    }
  }

  if (topBcIdx === -1) {
    return { status: 'skip', reason: 'no breadcrumb found' };
  }

  const topBcLine = lines[topBcIdx].trim();

  // 하단 브레드크럼 찾기 (파일 끝에서 역방향 탐색)
  let bottomBcIdx = -1;
  let bottomHrIdx = -1; // --- 구분선
  for (let i = lines.length - 1; i > topBcIdx; i--) {
    const trimmed = lines[i].trim();
    if (trimmed === '') continue;
    if (BREADCRUMB_PATTERN.test(trimmed)) {
      bottomBcIdx = i;
      // 위로 올라가면서 --- 찾기
      for (let j = i - 1; j > topBcIdx; j--) {
        const t = lines[j].trim();
        if (t === '') continue;
        if (t === '---') {
          bottomHrIdx = j;
        }
        break;
      }
      break;
    }
  }

  // 변환 실행
  const newLines = [];
  const bcMeta = `breadcrumb: ${removeLastSegment(topBcLine)}`;

  for (let i = 0; i < lines.length; i++) {
    // 상단 브레드크럼 → breadcrumb: 메타데이터로 교체
    if (i === topBcIdx) {
      newLines.push(bcMeta);
      continue;
    }
    // 하단 --- 제거
    if (i === bottomHrIdx) continue;
    // 하단 브레드크럼 제거
    if (i === bottomBcIdx) continue;
    // 하단 ---와 브레드크럼 사이 빈 줄 제거
    if (bottomHrIdx !== -1 && i > bottomHrIdx && i < bottomBcIdx && lines[i].trim() === '') continue;

    newLines.push(lines[i]);
  }

  // 파일 끝 정리: 불필요한 빈 줄 제거 (최대 1개 유지)
  while (newLines.length > 1 && newLines[newLines.length - 1].trim() === '' && newLines[newLines.length - 2].trim() === '') {
    newLines.pop();
  }

  const newContent = newLines.join('\n');
  if (newContent === content) {
    return { status: 'skip', reason: 'no change' };
  }

  fs.writeFileSync(filePath, newContent, 'utf8');
  return { status: 'migrated', bcMeta };
}

// 실행
const files = collectMdFiles(resolvedRoot);
let migrated = 0;
let skipped = 0;

console.log(`Scanning ${files.length} files in ${resolvedRoot}\n`);

for (const file of files) {
  const rel = path.relative(resolvedRoot, file);
  const result = migrateFile(file);

  if (result.status === 'migrated') {
    console.log(`  ✓ ${rel}`);
    console.log(`    → ${result.bcMeta}`);
    migrated++;
  } else {
    console.log(`  - ${rel} (${result.reason})`);
    skipped++;
  }
}

console.log(`\nDone: ${migrated} migrated, ${skipped} skipped`);
