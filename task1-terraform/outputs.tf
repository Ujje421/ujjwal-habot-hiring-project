# Name: Ujjwal [Last Name]
# Contact: [Email / LinkedIn / GitHub]

output "raw_landing_bucket_name" {
  description = "The name of the D0 Raw Landing bucket"
  value       = google_storage_bucket.d0_raw_landing.name
}

output "staged_enforced_dataset_id" {
  description = "The ID of the D1 Staged/Enforced BigQuery dataset"
  value       = google_bigquery_dataset.d1_staged_enforced.dataset_id
}

output "pipeline_service_account" {
  description = "The email of the pipeline service account used for IAM bindings"
  value       = var.pipeline_sa_email
}
