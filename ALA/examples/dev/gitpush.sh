# safer reorg script
set -euo pipefail

echo "[0/9] 현재 브랜치 기반으로 작업 브랜치 준비 (체크아웃 충돌 회피)"
CURRENT_BRANCH="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo HEAD)"
echo " - current: ${CURRENT_BRANCH}"
# 현재 작업 트리에서 바로 작업 브랜치를 만들되, 원격 리셋은 하지 않음
git checkout -B reorg-scripts-evaluation

echo "[1/9] 평가 디렉토리 생성"
mkdir -p scripts/06_evaluation/examples

# 안전 이동 함수: 추적 여부에 따라 git mv 또는 mv 사용
move() {
  src="$1"; dest="$2"
  if [ -e "$src" ]; then
    mkdir -p "$(dirname "$dest")"
    if git ls-files --error-unmatch "$src" >/dev/null 2>&1; then
      git mv "$src" "$dest"
    else
      mv "$src" "$dest"
    fi
  else
    echo " - skip: $src"
  fi
}

# 안전 제거 함수: 추적 여부에 따라 git rm 또는 rm 사용
rm_path() {
  p="$1"
  if [ -e "$p" ]; then
    if git ls-files --error-unmatch "$p" >/dev/null 2>&1; then
      git rm -r "$p"
    else
      rm -rf "$p"
    fi
  fi
}

echo "[2/9] 루트 평가 스크립트 이동 -> scripts/06_evaluation"
for f in generate_tables_from_source.py analyze_fsl_vs_groundtruth.py analyze_fsl_vs_groundtruth_fixed.py verify_data_consistency.py; do
  move "$f" "scripts/06_evaluation/$(basename "$f")"
done

echo "[3/9] 03_classification 내 평가 스크립트 이동 -> scripts/06_evaluation"
for f in scripts/03_classification/generate_resnet_results_tables.py \
         scripts/03_classification/generate_resnet_results_tables_v2.py \
         scripts/03_classification/generate_baseline_tables.py \
         scripts/03_classification/format_baseline_results.py; do
  move "$f" "scripts/06_evaluation/$(basename "$f")"
done

echo "[4/9] 예시 산출물 이동 -> scripts/06_evaluation/examples"
for f in scripts/03_classification/table7_few_shot_overall_performance.csv \
         scripts/03_classification/table8_few_shot_classwise_performance.csv \
         scripts/03_classification/table9_few_shot_binary_metrics.csv; do
  move "$f" "scripts/06_evaluation/examples/$(basename "$f")"
done

echo "[5/9] 유틸 내 평가 스크립트 이동 -> scripts/06_evaluation"
move "scripts/06_utilities/generate_performance_report.py" "scripts/06_evaluation/generate_performance_report.py"

echo "[6/9] 불필요 폴더/자산 정리"
rm_path scripts/06_utilities
rm_path scripts/99_deprecated_debug
rm_path dashboard_static

echo "[7/9] 평가 사용법/프로젝트 문서 작성"
cat > scripts/06_evaluation/README.md <<'EOF'
# 06_evaluation

Table 7/8 및 관련 평가 스크립트.

## 사용법
- 최종 테이블 생성:
  python scripts/06_evaluation/generate_tables_from_source.py
- 대안 분석:
  python scripts/06_evaluation/analyze_fsl_vs_groundtruth.py
  python scripts/06_evaluation/analyze_fsl_vs_groundtruth_fixed.py
- 일관성 검증:
  python scripts/06_evaluation/verify_data_consistency.py
EOF

mkdir -p docs
cat > docs/README.md <<'EOF'
# Project Overview

- 01 Data Preparation: main_launcher 기반 기초 작업
- 02 Preprocessing: 전처리된 이미지를 원하는 카테고리에 직접 배치해 Support Set 준비
- 03 Classification: 배치 실험 수행
- 04 Ground Truth: 1회 분류/검증 및 정리
- 06 Evaluation: Table 7/8 평가 스크립트 및 산출물

자세한 Table 7/8 사용법은 `scripts/06_evaluation/README.md` 참고.
EOF

echo "[7.1/9] 더 이상 불필요한 문서 정리"
rm_path docs/cleanup
rm_path docs/setup
rm_path docs/readme/dashboard_README.md
rm_path docs/guides/dashboard_wireframes.md

echo "[8/9] 변경사항 커밋"
 git add -A
 git commit -m "refactor: move Table 7/8 to scripts/06_evaluation; remove utilities/debug/dashboard; update docs and usage" || true

echo "[9/9] 브랜치 푸시 및 결과 요약"
 git push -u origin reorg-scripts-evaluation
 git status -sb | cat
 git show --stat -1 | cat