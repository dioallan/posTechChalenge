import streamlit as st
import requests
import re
import pandas as pd
import json


def dashboard_prometheus():
    st.header("Métricas Prometheus")
    METRICS_URL = "http://localhost:5000/metrics"
    try:
        response = requests.get(METRICS_URL)
        metrics_text = response.text

        # Contagem de requisições por endpoint
        pattern = r'flask_http_request_total{method="(\w+)",path="([^"]+)",status="(\d+)"} (\d+)'
        matches = re.findall(pattern, metrics_text)
        st.subheader("Requisições por endpoint")
        for method, path, status, count in matches:
            st.write(f"{method} {path} (status {status}): {count}")

        # Latência média por endpoint
        pattern_latency = r'flask_http_request_duration_seconds_sum{method="(\w+)",path="([^"]+)",status="(\d+)"} ([\d\.]+)'
        pattern_count = r'flask_http_request_duration_seconds_count{method="(\w+)",path="([^"]+)",status="(\d+)"} (\d+)'
        latency_matches = re.findall(pattern_latency, metrics_text)
        count_matches = re.findall(pattern_count, metrics_text)
        st.subheader("Latência média por endpoint")
        for (m1, p1, s1, sum_latency), (m2, p2, s2, count) in zip(latency_matches, count_matches):
            if count != "0":
                avg_latency = float(sum_latency) / int(count)
                st.write(
                    f"{m1} {p1} (status {s1}): {avg_latency:.3f} segundos")
    except Exception as e:
        st.error(f"Erro ao buscar métricas: {e}")


def dashboard_logs():
    st.header("Logs Estruturados")
    LOG_FILE = "logsExecucao.json"
    try:
        with open(LOG_FILE) as f:
            logs = [json.loads(line) for line in f if line.strip()]
        df = pd.DataFrame(logs)
        st.subheader("Requisições por endpoint")
        st.dataframe(df.groupby(
            ['method', 'path', 'status']).size().reset_index(name='count'))
        st.subheader("Latência média por endpoint")
        st.dataframe(df.groupby(['method', 'path'])[
                     'duration'].mean().reset_index())
    except Exception as e:
        st.error(f"Erro ao ler logs: {e}")


# --- Interface Unificada ---
st.title("Dashboard Unificado da API Flask")

opcao = st.sidebar.selectbox(
    "Escolha o dashboard",
    ("Métricas Prometheus", "Logs Estruturados")
)

if opcao == "Métricas Prometheus":
    dashboard_prometheus()
elif opcao == "Logs Estruturados":
    dashboard_logs()
