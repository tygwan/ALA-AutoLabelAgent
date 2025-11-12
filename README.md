# ALA Project Wrapper

이 저장소는 핵심 실행 코드를 `ALA/` 디렉토리로 정리했습니다. 실사용자는 아래 단계를 따르면 됩니다.

## 빠른 시작

```bash
git clone https://github.com/tygwan/ALA-AutoLabelAgent.git
cd ALA-AutoLabelAgent/ALA
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
./install_project.sh  # 옵션, 환경에 맞춰 실행
python scripts/01_data_preparation/main_launcher.py --category test_category --plot --preprocess
```

자세한 사용법은 `ALA/README.md`와 `ALA/docs/` 문서를 참고하세요.
