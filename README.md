# databricks-on-boarding-fuichiro-nakae

Databricksオンボーディングプロジェクト

## 概要

このプロジェクトは以下の2つのタスクを実行するDatabricksジョブです:

1. **Task 1: Playwright Scraping** (サーバーレス)
   - Playwrightを使用したWebスクレイピング

2. **Task 2: DB Fetch** (プロビジョンド)
   - Databricksカタログからのデータ取得

## ディレクトリ構造

```
.
├── src/
│   ├── task1_playwright_scraping/
│   │   └── runner.py
│   └── task2_db_fetch/
│       └── runner.py
├── tests/
│   ├── test_task1.py
│   └── test_task2.py
├── terraform/
│   ├── module/
│   │   ├── variables.tf
│   │   ├── databricks_job.tf
│   │   └── outputs.tf
│   └── envs/
│       ├── dev/
│       └── stg/
├── Taskfile.yaml
├── pyproject.toml
└── CLAUDE.md
```

## セットアップ

### 必要なツール

```bash
# Task (go-task)
brew install go-task/tap/go-task

# uv (Pythonパッケージ管理)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Terraform
brew install terraform

# Databricks CLI
brew install databricks/tap/databricks
```

### 依存関係インストール

```bash
uv sync --all-extras
```

### Databricks CLI認証

```bash
databricks configure
# Host: https://dbc-e50a6f45-d1a5.cloud.databricks.com
# Token: (Personal Access Tokenを入力)
```

## 使用方法

### コード品質チェック

```bash
# フォーマット
task fmt

# フォーマットチェック
task fmt-check

# Lint + 型チェック
task check

# テスト
task test
```

### Terraformデプロイ

```bash
# dev環境
task terraform-plan-dev
task terraform-apply-dev

# stg環境
task terraform-plan-stg
task terraform-apply-stg

# 構文チェック
task terraform-test
```

## 環境

| 環境 | 説明 |
|------|------|
| dev | 開発環境 |
| stg | ステージング環境 |

**注意**: PRD環境は使用禁止です（Terraformのvalidationで制限）

## Slack通知設定

1. Slackチャンネルを作成
2. Slack AppでIncoming Webhook URLを取得
3. Databricks UIでNotification Destinationを作成
4. 発行されたIDを `terraform/envs/{env}/variables.tf` の `notification_destination_id` に設定
