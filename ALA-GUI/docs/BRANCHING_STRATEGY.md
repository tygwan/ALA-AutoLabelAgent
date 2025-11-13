# Git Branching Strategy - ALA-GUI

**Version**: 1.0
**Last Updated**: 2025-11-13
**Project Phase**: M2 (GUI Layer Development)

---

## Overview

ALA-GUI 프로젝트는 **Feature Branch Workflow**를 사용하여 마일스톤 기반 개발을 진행합니다.

### 핵심 원칙
- ✅ **main 브랜치는 항상 안정적인 상태 유지** (모든 테스트 통과)
- ✅ **각 마일스톤(M1, M2, M3 ...)은 독립적인 feature 브랜치에서 개발**
- ✅ **완료된 마일스톤은 release 브랜치로 보존**
- ✅ **모든 병합은 테스트 통과 후에만 진행**

---

## Branch Types

### 1. main (메인 브랜치)
- **목적**: 프로덕션 준비 완료 코드
- **보호 수준**: 🔒 Protected (직접 푸시 금지)
- **병합 조건**:
  - 모든 테스트 통과 (pytest)
  - 코드 리뷰 완료 (self-review for solo dev)
  - TDD 사이클 완료 (RED → GREEN → REFACTOR)

**규칙**:
```bash
# ❌ 절대 금지
git checkout main
git commit -m "..."  # main에 직접 커밋 금지!

# ✅ 올바른 방법
git checkout feature/m2-gui
git commit -m "..."
# ... 작업 완료 후 ...
git checkout main
git merge feature/m2-gui  # 병합만 허용
```

### 2. feature/* (기능 브랜치)
- **목적**: 새로운 기능 개발 (마일스톤 단위)
- **네이밍**: `feature/m{N}-{description}`
- **수명**: 마일스톤 시작 ~ 완료
- **베이스**: main

**예시**:
```bash
feature/m1-foundation     # M1: 기반 구조
feature/m2-gui            # M2: GUI 레이어 (현재)
feature/m3-models         # M3: 모델 통합
feature/m4-annotation     # M4: 어노테이션 도구
```

**워크플로우**:
```bash
# 1. 브랜치 생성
git checkout main
git checkout -b feature/m2-gui

# 2. TDD 사이클 진행
# RED → GREEN → REFACTOR → COMMIT
git commit -m "feat(ui): add MainWindow"
git commit -m "test(ui): add MainWindow tests"

# 3. 완료 후 병합
git checkout main
git merge feature/m2-gui
git tag v0.2.0
git push origin main --tags
```

### 3. release/* (릴리즈 브랜치)
- **목적**: 완료된 마일스톤 보존
- **네이밍**: `release/m{N}-{description}`
- **수명**: 영구 (삭제 금지)
- **베이스**: 마일스톤 완료 시점의 main

**예시**:
```bash
release/m1-foundation ✅  # v0.1.0 (182 tests passing)
release/m2-gui            # v0.2.0 (예정)
release/m3-models         # v0.3.0 (예정)
```

**생성 방법**:
```bash
# M1 완료 후
git checkout main
git tag -a v0.1.0 -m "Release: M1 Foundation"
git checkout -b release/m1-foundation
git push origin release/m1-foundation
git push origin --tags
```

### 4. hotfix/* (긴급 수정 브랜치)
- **목적**: 프로덕션 긴급 버그 수정
- **네이밍**: `hotfix/{issue-description}`
- **수명**: 수정 완료 후 삭제
- **베이스**: main

**워크플로우**:
```bash
# 1. 긴급 버그 발견
git checkout main
git checkout -b hotfix/critical-serialization-bug

# 2. 버그 수정
git commit -m "fix(model): fix Project serialization bug"

# 3. 병합 (main + 현재 작업 중인 feature)
git checkout main
git merge hotfix/critical-serialization-bug
git checkout feature/m2-gui
git merge hotfix/critical-serialization-bug

# 4. 정리
git branch -d hotfix/critical-serialization-bug
```

---

## Current Branch Structure

```
main (v0.1.0) ← 안정 버전
 │
 ├─ release/m1-foundation (v0.1.0) ✅ 보존
 │   └─ 596bb99 feat(models): add core data models
 │   └─ 6681393 feat(core): add ProjectManager
 │   └─ 74d3037 feat(system): add error handling, config, logging
 │   └─ 218d1b4 feat(utils): add image, file, path utilities
 │   └─ dd02d86 feat(m1): complete M1 with integration
 │   └─ 6cf7ea4 docs(m1): mark M1 tasks complete
 │   └─ 690776f chore: update gitignore
 │
 └─ feature/m2-gui ← 현재 작업 중 🔄
     └─ (M2 개발 진행 중...)
```

---

## Workflow Examples

### M2 개발 시작 (현재)

```bash
# ✅ 이미 완료됨
git checkout -b feature/m2-gui
# 현재 이 브랜치에서 작업 중

# M2 개발 진행
git commit -m "feat(ui): add MainWindow structure"
git commit -m "test(ui): add MainWindow tests"
git commit -m "feat(ui): add ImageCanvas widget"
# ... TDD 사이클 계속 ...

# M2 완료 시
git checkout main
git merge feature/m2-gui
git tag -a v0.2.0 -m "Release: M2 GUI Layer"
git checkout -b release/m2-gui
git push origin main release/m2-gui --tags
```

### 버그 발견 시

```bash
# M2 작업 중 M1의 버그 발견
git checkout main
git checkout -b hotfix/fix-config-validation

# 수정 + 테스트
git commit -m "fix(config): fix validation range check"

# main에 병합
git checkout main
git merge hotfix/fix-config-validation

# 현재 작업 브랜치에도 적용
git checkout feature/m2-gui
git merge hotfix/fix-config-validation

# 정리
git branch -d hotfix/fix-config-validation
```

### M3 시작 전 준비

```bash
# M2 완료 후 M3 시작
git checkout main
git pull origin main

# M2 릴리즈 브랜치 생성
git checkout -b release/m2-gui
git push origin release/m2-gui

# M3 feature 브랜치 생성
git checkout main
git checkout -b feature/m3-models
```

---

## Version Tagging

### Semantic Versioning (SemVer)

```
v{MAJOR}.{MINOR}.{PATCH}

예시:
v0.1.0  ← M1 완료
v0.2.0  ← M2 완료
v0.3.0  ← M3 완료
v1.0.0  ← 최종 배포 (M8 완료)
```

### 태그 생성 규칙

```bash
# Annotated 태그 사용 (메시지 포함)
git tag -a v0.{N}.0 -m "Release: M{N} {Description}

- 주요 기능 1
- 주요 기능 2
- 테스트: {N}개 통과
"

# 태그 푸시
git push origin --tags
```

**예시**:
```bash
git tag -a v0.1.0 -m "Release: M1 Foundation & Core Infrastructure

- 182 tests passing (100% for non-GUI)
- Complete data models, controllers, utilities
- Comprehensive documentation
"
```

---

## Pull Request (Optional)

Solo 개발이지만, 향후 협업을 위해 PR 사용 가능:

```bash
# feature 브랜치 푸시
git push origin feature/m2-gui

# GitHub에서 PR 생성
# main ← feature/m2-gui

# Self-review 후 병합
gh pr create --title "M2: GUI Layer Development" --body "..."
gh pr merge --merge
```

---

## Branch Cleanup

### 로컬 브랜치 정리

```bash
# 병합된 feature 브랜치 삭제
git branch -d feature/m2-gui

# 강제 삭제 (미병합 브랜치)
git branch -D feature/experimental
```

### 원격 브랜치 정리

```bash
# 원격 feature 브랜치 삭제
git push origin --delete feature/m2-gui

# ⚠️ release 브랜치는 절대 삭제 금지!
```

---

## Best Practices

### ✅ Do

1. **main 보호**: main은 항상 테스트 통과 상태 유지
2. **작은 커밋**: TDD 사이클마다 커밋 (RED → GREEN → REFACTOR)
3. **명확한 메시지**: Conventional Commits 형식 사용
4. **정기적 푸시**: 작업 내용 백업 (하루 1회 이상)
5. **테스트 먼저**: 병합 전 반드시 테스트 실행
6. **릴리즈 보존**: 완료된 마일스톤은 release 브랜치로 보존

### ❌ Don't

1. **main 직접 수정**: main에 직접 커밋 금지
2. **테스트 스킵**: 테스트 실패 상태로 병합 금지
3. **거대 커밋**: 수백 줄 변경사항을 한 커밋에 포함 금지
4. **release 삭제**: release 브랜치 삭제 금지
5. **강제 푸시**: `git push --force` 사용 금지 (main, release)

---

## Troubleshooting

### 잘못된 브랜치에 커밋한 경우

```bash
# main에 실수로 커밋한 경우
git checkout main
git log --oneline -3  # 커밋 확인

# 커밋을 feature 브랜치로 이동
git checkout feature/m2-gui
git cherry-pick <commit-hash>

# main에서 커밋 제거
git checkout main
git reset --hard HEAD~1  # ⚠️ 신중히 사용
```

### 병합 충돌 해결

```bash
# 병합 시도
git merge feature/m2-gui
# CONFLICT (content): Merge conflict in src/...

# 충돌 파일 수정
code src/conflicted_file.py

# 충돌 해결 후
git add src/conflicted_file.py
git commit -m "merge: resolve conflicts in feature/m2-gui"
```

### 브랜치 동기화

```bash
# main의 최신 변경사항을 feature에 반영
git checkout feature/m2-gui
git merge main

# 또는 rebase (히스토리를 깔끔하게)
git rebase main
```

---

## Milestones & Branches Roadmap

| Milestone | Feature Branch | Release Branch | Tag | Status |
|-----------|----------------|----------------|-----|--------|
| M0: Setup | - | - | - | ✅ Complete |
| M1: Foundation | feature/m1-foundation | release/m1-foundation | v0.1.0 | ✅ Complete |
| M2: GUI Layer | feature/m2-gui | release/m2-gui | v0.2.0 | 🔄 In Progress |
| M3: Model Integration | feature/m3-models | release/m3-models | v0.3.0 | ⏳ Pending |
| M4: Annotation Tools | feature/m4-annotation | release/m4-annotation | v0.4.0 | ⏳ Pending |
| M5: Web Integration | feature/m5-web | release/m5-web | v0.5.0 | ⏳ Pending |
| M6: Pipeline | feature/m6-pipeline | release/m6-pipeline | v0.6.0 | ⏳ Pending |
| M7: Polish | feature/m7-polish | release/m7-polish | v0.7.0 | ⏳ Pending |
| M8: Deployment | feature/m8-deployment | release/m8-deployment | v1.0.0 | ⏳ Pending |

---

## References

- [Feature Branch Workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/feature-branch-workflow)
- [Semantic Versioning](https://semver.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Git Best Practices](https://git-scm.com/book/en/v2/Git-Branching-Branching-Workflows)

---

**Maintained by**: Claude (AI Developer)
**Review Status**: Ready for M2 development
**Last Sync**: 2025-11-13 13:30 KST
