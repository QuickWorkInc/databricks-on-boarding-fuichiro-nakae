resource "databricks_job" "main" {
  name                = "databricks-on-boarding-fuichiro-nakae-${var.env}"
  max_concurrent_runs = 1

  run_as {
    service_principal_name = var.service_principal_name
  }

  schedule {
    quartz_cron_expression = "0 0 * * * ?"
    timezone_id            = "Asia/Tokyo"
  }

  dynamic "webhook_notifications" {
    for_each = var.notification_destination_id != "" ? [1] : []
    content {
      on_start {
        id = var.notification_destination_id
      }
      on_success {
        id = var.notification_destination_id
      }
      on_failure {
        id = var.notification_destination_id
      }
    }
  }

  git_source {
    url      = var.git_source_url
    provider = "gitHub"
    branch   = var.git_source_branch
  }

  # Task 1: Playwright Scraping (Provisioned)
  task {
    task_key = "playwright_scraping"

    notebook_task {
      notebook_path = "src/task1_playwright_scraping/runner"
      source        = "GIT"
      base_parameters = {
        env = var.env
      }
    }

    library {
      pypi {
        package = "playwright"
      }
    }

    library {
      pypi {
        package = "nest-asyncio"
      }
    }

    new_cluster {
      spark_version = "15.4.x-scala2.12"
      node_type_id  = "i3.xlarge"
      num_workers   = 0

      spark_conf = {
        "spark.databricks.cluster.profile" = "singleNode"
        "spark.master"                     = "local[*]"
      }

      custom_tags = {
        "ResourceClass" = "SingleNode"
      }
    }
  }

  # Task 2: DB Fetch (Provisioned/Classic)
  task {
    task_key = "db_fetch"

    depends_on {
      task_key = "playwright_scraping"
    }

    notebook_task {
      notebook_path = "src/task2_db_fetch/runner"
      source        = "GIT"
      base_parameters = {
        env = var.env
      }
    }

    new_cluster {
      spark_version      = "15.4.x-scala2.12"
      node_type_id       = "i3.xlarge"
      num_workers        = 0
      data_security_mode = "SINGLE_USER"

      spark_conf = {
        "spark.databricks.cluster.profile" = "singleNode"
        "spark.master"                     = "local[*]"
      }

      custom_tags = {
        "ResourceClass" = "SingleNode"
      }
    }
  }
}

resource "databricks_permissions" "job_permissions" {
  job_id = databricks_job.main.id

  access_control {
    service_principal_name = var.service_principal_name
    permission_level       = "IS_OWNER"
  }

  access_control {
    group_name       = "sn_3ggysc_admin"
    permission_level = "CAN_MANAGE"
  }
}
