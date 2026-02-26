# Databricks 開発ガイド

このドキュメントは、Databricksを使用したジョブ開発に必要な知識をまとめた引き継ぎ資料です。

## 1. 技術スタック

| 項目 | 技術 |
|------|------|
| データプラットフォーム | Databricks |
| IaC | Terraform |
| 言語 | Python 3.10+, SQL (直書き推奨) |
| パッケージ管理 | uv |
| タスクランナー | Task (go-task) |
| テスト | pytest, pytest-cov |
| Linter/Formatter | ruff |
| 型チェック | mypy |

## 2. Databricksの基本概念

### 2.1 コンピュートタイプ

| タイプ | 特徴 | 用途 |
|--------|------|------|
| サーバーレス | クラスタ管理不要、低コスト、VPC接続不可 | Delta Lake操作、パブリックAPI |
| クラシック (プロビジョンド) | 手動設定、VPC接続可能 | PostgreSQL、OpenSearch等へのアクセス |

```hcl
# サーバーレス: new_cluster を指定しない
task {
  task_key = "serverless_task"
  notebook_task { ... }
  # new_cluster なし
}

# クラシック: new_cluster を指定
task {
  task_key = "classic_task"
  notebook_task { ... }
  new_cluster {
    node_type_id = "i3.xlarge"
    num_workers  = 0  # シングルノード
  }
}
```

### 2.2 Databricks Secrets

機密情報（DB接続情報等）はSecretsで管理します。

```python
# Pythonでの取得方法
dbutils = get_dbutils()
host = dbutils.secrets.get("scope_name", "host")
password = dbutils.secrets.get("scope_name", "password")
```

**スコープ命名規則**: `{env}_opensearch`, `{env}_snpf_postgres` など

### 2.3 Databricksカタログ

PostgreSQLへのアクセスはカタログ経由で行います。

| 環境 | カタログ名 |
|------|-----------|
| dev | `dev_snpf` |
| stg | `stg_snpf` |
| prd | `prd_snpf` |

```python
# 使用例
env = "dev"
query = f"SELECT * FROM {env}_snpf.public.data_companies LIMIT 5"
df = spark.sql(query)
```

## 3. Terraform ジョブ設定

### 3.1 基本構造

```
terraform/
├── module/
│   ├── variables.tf       # 変数定義
│   └── databricks_job.tf  # ジョブ定義
└── envs/
    ├── dev/
    │   ├── main.tf        # モジュール呼び出し (env = "dev")
    │   ├── variables.tf
    │   ├── providers.tf
    │   └── backend.tf
    └── stg/
        └── (同様)
```

### 3.2 主要設定項目

```hcl
resource "databricks_job" "example" {
  # ジョブ名
  name = "job-name-${var.env}"

  # 最大同時実行数
  max_concurrent_runs = 1

  # 実行ユーザー（サービスプリンシパル）
  run_as {
    service_principal_name = "e22e080f-69c6-4126-a961-b917cb8db97a"
  }

  # スケジュール（Quartz cron形式）
  schedule {
    quartz_cron_expression = "0 0 * * * ?"  # 毎時0分
    timezone_id            = "Asia/Tokyo"
  }

  # Slack通知
  webhook_notifications {
    on_start   { id = var.notification_destination_id }
    on_success { id = var.notification_destination_id }
    on_failure { id = var.notification_destination_id }
  }

  # Git連携
  git_source {
    url      = var.git_source_url
    provider = "gitHub"
    branch   = var.git_source_branch
  }

  # タスク定義
  task {
    task_key = "task_name"
    notebook_task {
      notebook_path = "src/path/to/runner"
      source        = "GIT"
      base_parameters = {
        env = var.env
      }
    }
    # ライブラリ追加
    library {
      pypi { package = "package-name" }
    }
  }
}

# 権限設定
resource "databricks_permissions" "job_permissions" {
  job_id = databricks_job.example.id

  access_control {
    service_principal_name = "e22e080f-69c6-4126-a961-b917cb8db97a"
    permission_level       = "IS_OWNER"
  }
  access_control {
    group_name       = "sn_3ggysc_admin"
    permission_level = "CAN_MANAGE"
  }
}
```

### 3.3 環境変数の渡し方

```hcl
# 方法1: base_parameters（ノートブックパラメータ）
notebook_task {
  base_parameters = {
    env = var.env
  }
}

# 方法2: spark_env_vars（環境変数）
new_cluster {
  spark_env_vars = {
    MY_ENV_VAR = "value"
  }
}
```

### 3.4 環境制限の実装

```hcl
variable "env" {
  type = string
  validation {
    condition     = contains(["dev", "stg"], var.env)  # prdを除外
    error_message = "env must be dev or stg. PRD is NOT allowed."
  }
}
```

## 4. Pythonコード（ノートブック）

### 4.1 基本構造

```python
# Databricks notebook source

# パラメータ取得
dbutils.widgets.text("env", "dev")
env = dbutils.widgets.get("env")

# 処理実行
def main():
    catalog = f"{env}_snpf"
    query = f"SELECT * FROM {catalog}.public.table_name LIMIT 10"
    df = spark.sql(query)
    df.show()
    print("Completed successfully.")

main()
```

### 4.2 SQL直書きの推奨

```python
# ✅ 推奨: SQL直書き
query = f"""
SELECT corporate_number, company_name
FROM {env}_snpf.public.data_companies
WHERE updated_at >= '2024-01-01'
"""
df = spark.sql(query)

# ❌ 非推奨: SQLAlchemy ORM
# session.query(DataCompanies).filter(...)
```

## 5. Taskfile.yaml

```yaml
version: '3'

tasks:
  # フォーマット
  fmt:
    desc: コードを自動フォーマット
    cmds:
      - uv run ruff format ./src
      - terraform -chdir=terraform fmt -recursive

  fmt-check:
    desc: フォーマットをチェック
    cmds:
      - uv run ruff format --check ./src
      - terraform -chdir=terraform fmt -check -recursive

  # Lint + 型チェック
  check:
    desc: コード品質チェック
    cmds:
      - uv run ruff check ./src
      - uv run mypy src/

  # テスト
  test:
    desc: カバレッジ付きテスト
    cmds:
      - uv run pytest tests/ -v --cov=src

  # Terraformテスト
  terraform-test:
    desc: Terraform構文チェック
    cmds:
      - task: terraform-fmt-check
      - task: terraform-validate-dev
      - task: terraform-validate-stg

  terraform-fmt-check:
    desc: Terraformフォーマットチェック
    cmds:
      - terraform -chdir=terraform fmt -check -recursive

  terraform-validate-dev:
    desc: dev環境の構文チェック
    dir: terraform/envs/dev
    cmds:
      - terraform init -backend=false
      - terraform validate

  terraform-validate-stg:
    desc: stg環境の構文チェック
    dir: terraform/envs/stg
    cmds:
      - terraform init -backend=false
      - terraform validate

  # デプロイ
  terraform-plan-dev:
    desc: dev環境のplan確認
    dir: terraform/envs/dev
    cmds:
      - terraform init
      - terraform plan

  terraform-apply-dev:
    desc: dev環境にデプロイ
    dir: terraform/envs/dev
    cmds:
      - terraform init
      - terraform apply

  terraform-plan-stg:
    desc: stg環境のplan確認
    dir: terraform/envs/stg
    cmds:
      - terraform init
      - terraform plan

  terraform-apply-stg:
    desc: stg環境にデプロイ
    dir: terraform/envs/stg
    cmds:
      - terraform init
      - terraform apply
```

## 6. Slack通知設定

### 6.1 通知先の作成手順

1. Slackでチャンネル作成（例: `#onboarding-fuichiro-nakae`）
2. Slack App設定でIncoming Webhook URLを取得
3. Databricks UI → Settings → Notifications → Add destination
4. Slackを選択、Webhook URLを入力
5. 発行されたIDをTerraformで使用

### 6.2 Terraformでの設定

```hcl
# envs/dev/main.tf
module "job" {
  source                      = "../../module"
  notification_destination_id = "発行されたID"
}
```

## 7. ローカル開発環境

### 7.1 必要なツール

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

### 7.2 Databricks CLI認証

```bash
databricks configure
# Host: https://dbc-e50a6f45-d1a5.cloud.databricks.com
# Token: (Personal Access Tokenを入力)
```

### 7.3 依存関係インストール

```bash
uv sync --all-extras
```

## 8. よく使うコマンド

| コマンド | 説明 |
|---------|------|
| `task fmt` | コード自動フォーマット |
| `task fmt-check` | フォーマットチェック |
| `task check` | lint + 型チェック |
| `task test` | カバレッジ付きテスト |
| `task terraform-test` | Terraform構文チェック |
| `task terraform-plan-dev` | dev環境のplan確認 |
| `task terraform-apply-dev` | dev環境にデプロイ |

## 9. 参考リンク

- [Databricks Documentation](https://docs.databricks.com/)
- [Terraform Databricks Provider](https://registry.terraform.io/providers/databricks/databricks/latest/docs)
- [Databricks Slack Integration](https://docs.databricks.com/aws/ja/ai-bi/admin/slack-subscriptions)

## 10. 注意事項

| 項目 | 注意 |
|------|------|
| PRD環境 | 絶対に使用しない（validation で制限済み） |
| データ変更 | SELECT のみ、INSERT/UPDATE/DELETE は禁止 |
| SQL | SQLAlchemy等を使わず直書き |
| コミットメッセージ | 日本語で記述 |
