terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.id_proyecto
  region  = var.region
}

resource "google_bigquery_dataset" "monitorizacion_de_mis_repos" {
  dataset_id = "monitor_mis_repos_github"
  location   = "EU"
}

resource "google_bigquery_table" "tabla_actividad_repos" {
  dataset_id = google_bigquery_dataset.monitorizacion_de_mis_repos.dataset_id
  table_id   = "actividad"
  deletion_protection = false

  schema = jsonencode([
    {
      name = "nombre_del_repo"
      type = "STRING"
      mode = "REQUIRED"
    },
    {
      name = "ultimo_commit"
      type = "TIMESTAMP"
      mode = "NULLABLE"
    },
    {
      name = "numero_de_commits_recientes"
      type = "INTEGER"
      mode = "NULLABLE"
    },
    {
      name = "issues_abiertas"
      type = "INTEGER"
      mode = "NULLABLE"
    },
    {
      name = "fecha_de_la_comprobacion"
      type = "TIMESTAMP"
      mode = "REQUIRED"
    }
  ])
}