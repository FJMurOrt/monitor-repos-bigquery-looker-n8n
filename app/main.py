import os
import requests
from datetime import datetime, timezone
from dotenv import load_dotenv
from google.cloud import bigquery

bigquery_en_gcp = bigquery.Client()
ID_DE_LA_TABLA = "southern-field-472712-j3.monitor_mis_repos_github.actividad"

load_dotenv()

TOKEN_PARA_ACCEDER_A_GITHUB = os.getenv("GITHUB_TOKEN")
MI_USUARIO_EN_GITHUB = "FJMurOrt"

encabezados = {
    "Authorization": f"token {TOKEN_PARA_ACCEDER_A_GITHUB}"
}

def obtener_lista_de_repos():
    url = f"https://api.github.com/users/{MI_USUARIO_EN_GITHUB}/repos"
    respuesta = requests.get(url, headers=encabezados)
    return respuesta.json()

def obtener_ultimo_commit(nombre_del_repo):
    url = f"https://api.github.com/repos/{MI_USUARIO_EN_GITHUB}/{nombre_del_repo}/commits"
    respuesta = requests.get(url, headers=encabezados, params={"per_page": 1})
    commits = respuesta.json()
    if commits and isinstance(commits, list) and len(commits) > 0:
        return commits[0]["commit"]["author"]["date"]
    return None

def obtener_numero_de_issues_abiertas(nombre_del_repo):
    url = f"https://api.github.com/repos/{MI_USUARIO_EN_GITHUB}/{nombre_del_repo}"
    respuesta = requests.get(url, headers=encabezados)
    return respuesta.json().get("open_issues_count", 0)

def guardar_en_bigquery(filas):
    errores = bigquery_en_gcp.insert_rows_json(ID_DE_LA_TABLA, filas)
    if errores:
        print(f"Errores al insertar en BigQuery: {errores}")
    else:
        print(f"Se insertaron {len(filas)} filas en BigQuery.")

if __name__ == "__main__":
    lista_de_repos = obtener_lista_de_repos()
    filas_para_insertar = []

    for cada_repo in lista_de_repos:
        nombre_del_repo = cada_repo["name"]
        ultimo_commit = obtener_ultimo_commit(nombre_del_repo)
        issues_abiertas = obtener_numero_de_issues_abiertas(nombre_del_repo)

        fila = {
            "nombre_del_repo": nombre_del_repo,
            "ultimo_commit": ultimo_commit,
            "numero_de_commits_recientes": None,
            "issues_abiertas": issues_abiertas,
            "fecha_de_la_comprobacion": datetime.now(timezone.utc).isoformat()
        }
        filas_para_insertar.append(fila)
        print(f"{nombre_del_repo} | último commit: {ultimo_commit} | issues abiertas: {issues_abiertas}")

    guardar_en_bigquery(filas_para_insertar)