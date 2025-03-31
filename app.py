import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Rotina PIFE", layout="wide")

st.title("📅 Controle de Rotina PIFE (Seg a Sex)")

# Gera as datas da semana atual (segunda a sexta)
hoje = datetime.today()
inicio_semana = hoje - timedelta(days=hoje.weekday())  # Segunda
datas_semana = [(inicio_semana + timedelta(days=i)) for i in range(5)]
dias_formatados = [f"{data.strftime('%A')} - {data.strftime('%d/%m/%Y')}" for data in datas_semana]
dias_chave = [data.strftime('%Y-%m-%d') for data in datas_semana]

# Mapeia os nomes bonitos para chaves internas
dia_formatado_para_chave = dict(zip(dias_formatados, dias_chave))
chave_para_formatado = dict(zip(dias_chave, dias_formatados))

# Categorias PIFE
categorias = {
    "Profissional": ["Sincronizar Agenda", "Verificar Emails", "Sanches Mentality"],
    "Intelectual": ["1 Hora de Estudo"],
    "Físico": ["Exercicio Do Dia", "Cha Gelado", "Yakult"],
    "Emocional": ["Oração da Manhã", "Café com Deus"]
}

# Inicializa os dados
if "rotina" not in st.session_state:
    st.session_state.rotina = {
        chave: {cat: [False]*len(tarefas) for cat, tarefas in categorias.items()}
        for chave in dias_chave
    }

# Sidebar
aba_formatada = st.sidebar.selectbox("Selecione o dia", dias_formatados)
aba_chave = dia_formatado_para_chave[aba_formatada]
st.header(f"✅ Tarefas de {aba_formatada}")

# Mostrar tarefas
total_tarefas = 0
tarefas_cumpridas = 0

for categoria, tarefas in categorias.items():
    st.subheader(f"{categoria}")
    for i, tarefa in enumerate(tarefas):
        checked = st.checkbox(
            f"{tarefa}",
            value=st.session_state.rotina[aba_chave][categoria][i],
            key=f"{aba_chave}_{categoria}_{i}"
        )
        st.session_state.rotina[aba_chave][categoria][i] = checked
        total_tarefas += 1
        if checked:
            tarefas_cumpridas += 1

percentual = (tarefas_cumpridas / total_tarefas) * 100 if total_tarefas else 0
st.markdown(f"### 🎯 Cumprimento do dia: **{percentual:.0f}%**")

# Resumo semanal
with st.expander("📊 Ver Resumo Semanal"):
    resumo = {"Dia": [], "Cumprimento (%)": []}
    for chave in dias_chave:
        total = sum(len(tarefas) for tarefas in st.session_state.rotina[chave].values())
        feitos = sum(
            sum(1 for feito in tarefas if feito)
            for tarefas in st.session_state.rotina[chave].values()
        )
        perc = (feitos / total) * 100 if total else 0
        resumo["Dia"].append(chave_para_formatado[chave])
        resumo["Cumprimento (%)"].append(round(perc, 1))

    df = pd.DataFrame(resumo)
    st.bar_chart(df.set_index("Dia"))
    st.dataframe(df)
