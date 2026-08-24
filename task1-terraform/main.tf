# Name: Ujjwal [Last Name]
# Contact: [Email / LinkedIn / GitHub]

terraform {
  required_version = ">= 1.5.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# -----------------------------------------------------------------------------
# 1. PROJECT LEVEL AUDIT CONFIG
# -----------------------------------------------------------------------------
resource "google_project_iam_audit_config" "project_audit_logs" {
  project = var.project_id
  service = "allServices"

  audit_log_config {
    log_type = "DATA_READ"
  }
  audit_log_config {
    log_type = "DATA_WRITE"
  }
}

# -----------------------------------------------------------------------------
# 2. GCS RAW LANDING (D0)
# -----------------------------------------------------------------------------
resource "google_storage_bucket" "d0_raw_landing" {
  name                        = var.bucket_name
  location                    = var.region
  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }

  encryption {
    default_kms_key_name = var.kms_key_id
  }

  lifecycle_rule {
    action {
      type          = "SetStorageClass"
      storage_class = "NEARLINE"
    }
    condition {
      age = 30
    }
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 365
    }
  }

  labels = {
    environment = "staging"
    managed_by  = "terraform"
  }
}

resource "google_storage_bucket_iam_member" "pipeline_sa_bucket_creator" {
  bucket = google_storage_bucket.d0_raw_landing.name
  role   = "roles/storage.objectCreator"
  member = "serviceAccount:${var.pipeline_sa_email}"
}

# -----------------------------------------------------------------------------
# 3. BIGQUERY STAGED ENFORCED (D1)
# -----------------------------------------------------------------------------
resource "google_bigquery_dataset" "d1_staged_enforced" {
  dataset_id                  = var.bq_dataset_id
  project                     = var.project_id
  location                    = var.region
  default_table_expiration_ms = 7776000000 # 90 days in milliseconds
  delete_contents_on_destroy  = false

  labels = {
    environment = "staging"
    managed_by  = "terraform"
  }
}

resource "google_bigquery_dataset_iam_member" "pipeline_sa_bq_editor" {
  dataset_id = google_bigquery_dataset.d1_staged_enforced.dataset_id
  project    = var.project_id
  role       = "roles/bigquery.dataEditor"
  member     = "serviceAccount:${var.pipeline_sa_email}"
}

# -----------------------------------------------------------------------------
# 4. BIGQUERY TABLE WITH ROW-LEVEL SECURITY (RLS)
# -----------------------------------------------------------------------------
resource "google_bigquery_table" "student_records" {
  dataset_id = google_bigquery_dataset.d1_staged_enforced.dataset_id
  table_id   = "student_records"

  schema = <<EOF
[
  {
    "name": "student_id",
    "type": "STRING",
    "mode": "REQUIRED"
  },
  {
    "name": "region",
    "type": "STRING",
    "mode": "REQUIRED"
  },
  {
    "name": "student_data",
    "type": "STRING",
    "mode": "NULLABLE"
  }
]
EOF

  labels = {
    environment = "staging"
    managed_by  = "terraform"
  }
}

resource "google_bigquery_row_access_policy" "region_policy" {
  project    = var.project_id
  dataset_id = google_bigquery_dataset.d1_staged_enforced.dataset_id
  table_id   = google_bigquery_table.student_records.table_id
  policy_id  = "restrict_by_region_session_user"

  filter_predicate = "region = SESSION_USER()"
}
