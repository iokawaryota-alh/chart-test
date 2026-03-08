# テストフォルダ構成

`test/` 配下は、目的別に次の2系統へ分割しています。

役割の定義は `ROLES.md` を参照してください。

## 1. DevTest（教材・フロント回帰）

- パス: `test/DevTest/`
- 対象: Playwright + pytest のUI回帰テスト、手動チェック資料
- 想定: 学習・レビュー用途のため、基本は画面を見ながら実行（headed）

代表ファイル:
- `test/DevTest/test_frontend.py`
- `test/DevTest/README.md`
- `test/DevTest/REGRESSION-UI-CHECKLIST.md`

推奨実行コマンド（headed）:

```powershell
pytest test/DevTest -v --headed --screenshot=only-on-failure --video=retain-on-failure --tracing=retain-on-failure
```

## 2. Other（補助スクリプト）

- パス: `test/Other/`
- 対象: API確認用の補助スクリプト（pytestの自動収集対象外）

代表ファイル:
- `test/Other/api_leverage_check.py`
- `test/Other/db_api_check.py`

実行例:

```powershell
python test/Other/api_leverage_check.py
python test/Other/db_api_check.py
```

## 補足

- CIや高速実行時のみ headless を使い、教材用途では headed を優先する運用を推奨します。
