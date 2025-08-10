import streamlit as st
import requests
import re

st.title("Dashboard de Métricas da API Flask")

# URL do endpoint de métricas do Flask
METRICS_URL = "http://localhost:5000/metrics"

# Busca as métricas
response = requests.get(METRICS_URL)
metrics_text = response.text

# Exemplo: extrair contagem de requisições por endpoint
pattern = r'flask_http_request_total{method="(\w+)",path="([^"]+)",status="(\d+)"} (\d+)'
matches = re.findall(pattern, metrics_text)

st.header("Requisições por endpoint")
for method, path, status, count in matches:
    st.write(f"{method} {path} (status {status}): {count}")

# Exemplo: extrair latência média (histogram)
pattern_latency = r'flask_http_request_duration_seconds_sum{method="(\w+)",path="([^"]+)",status="(\d+)"} ([\d\.]+)'
pattern_count = r'flask_http_request_duration_seconds_count{method="(\w+)",path="([^"]+)",status="(\d+)"} (\d+)'
latency_matches = re.findall(pattern_latency, metrics_text)
count_matches = re.findall(pattern_count, metrics_text)

st.header("Latência média por endpoint")
for (m1, p1, s1, sum_latency), (m2, p2, s2, count) in zip(latency_matches, count_matches):
    if count != "0":
        avg_latency = float(sum_latency) / int(count)
        st.write(f"{m1} {p1} (status {s1}): {avg_latency:.3f} segundos")
