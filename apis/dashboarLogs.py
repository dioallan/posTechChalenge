import streamlit as st
import pandas as pd
import json

st.title("Dashboard de Logs da API Flask")

# Caminho do arquivo de log
LOG_FILE = "logsExecucao.json"

# Lê os logs
with open(LOG_FILE) as f:
    logs = [json.loads(line) for line in f if line.strip()]

df = pd.DataFrame(logs)

# Exibe contagem por endpoint
st.header("Requisições por endpoint")
st.dataframe(df.groupby(['method', 'path', 'status']
                        ).size().reset_index(name='count'))

# Exibe latência média por endpoint
st.header("Latência média por endpoint")
st.dataframe(df.groupby(['method', 'path'])['duration'].mean().reset_index())
