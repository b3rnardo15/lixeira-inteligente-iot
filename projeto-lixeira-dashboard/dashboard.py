import streamlit as st
import pymongo
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import certifi
import requests


load_dotenv()


st.set_page_config(
    page_title="Dashboard Lixeira v4.0",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Tema customizado com paleta ecológica
def set_theme():
    """Configura o tema visual do dashboard"""
    
    # Detectar preferência do usuário
    theme_mode = st.sidebar.radio(
        "🎨 Tema",
        ["☀️ Claro", "🌙 Escuro"],
        horizontal=True
    )
    
    if theme_mode == "☀️ Claro":
        # Tema Claro - Paleta Ecológica
        st.markdown("""
            <style>
                :root {
                    --primary-color: #10b981;
                    --secondary-color: #059669;
                    --bg-color: #f8fafb;
                    --card-bg: #ffffff;
                    --text-primary: #1f2937;
                    --text-secondary: #6b7280;
                    --border-color: #e5e7eb;
                }
                
                .main {
                    background-color: #f8fafb;
                    color: #1f2937;
                }
                
                .stMetric {
                    background: linear-gradient(135deg, #ffffff 0%, #f0fdf4 100%);
                    padding: 20px !important;
                    border-radius: 12px !important;
                    border: 1px solid #d1fae5 !important;
                    box-shadow: 0 2px 8px rgba(16, 185, 129, 0.1) !important;
                }
                
                .stTabs [data-baseweb="tab-list"] {
                    background-color: #f3f4f6;
                    padding: 10px;
                    border-radius: 10px;
                }
                
                .stTabs [data-baseweb="tab"] {
                    background-color: transparent;
                    border-radius: 8px;
                    color: #6b7280;
                    font-weight: 500;
                }
                
                .stTabs [aria-selected="true"] {
                    background-color: #10b981 !important;
                    color: white !important;
                }
                
                .stButton > button {
                    background-color: #10b981;
                    color: white;
                    border-radius: 8px;
                    border: none;
                    padding: 10px 24px;
                    font-weight: 600;
                    transition: all 0.3s ease;
                }
                
                .stButton > button:hover {
                    background-color: #059669;
                    box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
                }
                
                .stTextInput > div > div > input,
                .stSelectbox > div > div > select,
                .stNumberInput > div > div > input {
                    border: 2px solid #d1fae5 !important;
                    border-radius: 8px !important;
                    padding: 10px !important;
                }
                
                .stTextInput > div > div > input:focus,
                .stSelectbox > div > div > select:focus,
                .stNumberInput > div > div > input:focus {
                    border: 2px solid #10b981 !important;
                    box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1) !important;
                }
                
                .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
                    color: #1f2937 !important;
                }
                
                .stInfo {
                    background-color: #ecfdf5 !important;
                    border: 1px solid #d1fae5 !important;
                    border-radius: 8px !important;
                    color: #065f46 !important;
                }
                
                .stWarning {
                    background-color: #fef3c7 !important;
                    border: 1px solid #fcd34d !important;
                    border-radius: 8px !important;
                }
                
                .stSuccess {
                    background-color: #d1fae5 !important;
                    border: 1px solid #6ee7b7 !important;
                    border-radius: 8px !important;
                }
                
                .stError {
                    background-color: #fee2e2 !important;
                    border: 1px solid #fca5a5 !important;
                    border-radius: 8px !important;
                }
            </style>
        """, unsafe_allow_html=True)
    else:
        # Tema Escuro - Melhorado
        st.markdown("""
            <style>
                :root {
                    --primary-color: #10b981;
                    --secondary-color: #059669;
                    --bg-color: #111827;
                    --card-bg: #1f2937;
                    --text-primary: #f3f4f6;
                    --text-secondary: #d1d5db;
                    --border-color: #374151;
                }
                
                .main {
                    background-color: #111827;
                    color: #f3f4f6;
                }
                
                .stMetric {
                    background: linear-gradient(135deg, #1f2937 0%, #0f172a 100%);
                    padding: 20px !important;
                    border-radius: 12px !important;
                    border: 1px solid #10b981 !important;
                    box-shadow: 0 2px 8px rgba(16, 185, 129, 0.2) !important;
                }
                
                .stTabs [data-baseweb="tab-list"] {
                    background-color: #1f2937;
                    padding: 10px;
                    border-radius: 10px;
                }
                
                .stTabs [data-baseweb="tab"] {
                    background-color: transparent;
                    border-radius: 8px;
                    color: #9ca3af;
                    font-weight: 500;
                }
                
                .stTabs [aria-selected="true"] {
                    background-color: #10b981 !important;
                    color: #111827 !important;
                }
                
                .stButton > button {
                    background-color: #10b981;
                    color: #111827;
                    border-radius: 8px;
                    border: none;
                    padding: 10px 24px;
                    font-weight: 600;
                    transition: all 0.3s ease;
                }
                
                .stButton > button:hover {
                    background-color: #34d399;
                    box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
                }
                
                .stTextInput > div > div > input,
                .stSelectbox > div > div > select,
                .stNumberInput > div > div > input {
                    background-color: #1f2937 !important;
                    border: 2px solid #374151 !important;
                    border-radius: 8px !important;
                    color: #f3f4f6 !important;
                    padding: 10px !important;
                }
                
                .stTextInput > div > div > input:focus,
                .stSelectbox > div > div > select:focus,
                .stNumberInput > div > div > input:focus {
                    border: 2px solid #10b981 !important;
                    box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.2) !important;
                }
                
                .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
                    color: #f3f4f6 !important;
                }
                
                .stInfo {
                    background-color: #064e3b !important;
                    border: 1px solid #10b981 !important;
                    border-radius: 8px !important;
                    color: #d1fae5 !important;
                }
                
                .stWarning {
                    background-color: #78350f !important;
                    border: 1px solid #fcd34d !important;
                    border-radius: 8px !important;
                }
                
                .stSuccess {
                    background-color: #064e3b !important;
                    border: 1px solid #10b981 !important;
                    border-radius: 8px !important;
                    color: #d1fae5 !important;
                }
                
                .stError {
                    background-color: #7f1d1d !important;
                    border: 1px solid #fca5a5 !important;
                    border-radius: 8px !important;
                }
            </style>
        """, unsafe_allow_html=True)
    
    return theme_mode == "☀️ Claro"


@st.cache_resource
def init_connection():
    mongo_uri = os.getenv('MONGODB_URI')
    if not mongo_uri:
        st.error("MONGODB_URI nao configurada")
        return None
    try:
        return pymongo.MongoClient(mongo_uri, tlsCAFile=certifi.where())
    except Exception as e:
        st.error(f"Erro MongoDB: {e}")
        return None


client = init_connection()


if client:
    try:
        db = client['lixeira_inteligente']
        collection_leituras = db['leituras']
        collection_usuarios = db['usuarios']
        collection_auditoria = db['auditoria']
    except Exception as e:
        st.error(f"Erro ao acessar database: {e}")
        st.stop()
else:
    st.stop()


def inicializar_sessao():
    if 'usuario_logado' not in st.session_state:
        st.session_state.usuario_logado = None
    if 'token' not in st.session_state:
        st.session_state.token = None
    if 'role' not in st.session_state:
        st.session_state.role = None
    if 'mfa_requerido' not in st.session_state:
        st.session_state.mfa_requerido = False
    if 'mfa_qr_code' not in st.session_state:
        st.session_state.mfa_qr_code = None
    if 'mfa_secret' not in st.session_state:
        st.session_state.mfa_secret = None


inicializar_sessao()


API_URL = "http://localhost:5000"


def fazer_login(username: str, senha: str):
    try:
        response = requests.post(f"{API_URL}/api/login", json={"username": username, "senha": senha})
        if response.status_code == 200:
            dados = response.json()
            st.session_state.usuario_logado = username
            st.session_state.token = dados['token']
            st.session_state.role = dados['usuario'].get('role', 'usuario')
            st.session_state.mfa_requerido = dados.get('requer_mfa', False)
            return True, "login realizado"
        else:
            return False, response.json().get('erro', 'erro no login')
    except Exception as e:
        return False, f"Erro: {e}"


def fazer_logout():
    st.session_state.usuario_logado = None
    st.session_state.token = None
    st.session_state.role = None
    st.session_state.mfa_qr_code = None
    st.session_state.mfa_secret = None


def tela_login():
    st.markdown("# ♻️ Lixeira Inteligente")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### acesso ao sistema")
        if st.session_state.mfa_requerido:
            st.warning("🔐 mfa ativado para sua conta")
            codigo_mfa = st.text_input("codigo mfa (6 digitos)", placeholder="000000")
            if st.button("✓ verificar mfa"):
                try:
                    response = requests.post(f"{API_URL}/api/mfa/verificar", json={"username": st.session_state.usuario_logado, "codigo": codigo_mfa})
                    if response.status_code == 200:
                        st.success("✓ mfa verificado!")
                        st.session_state.mfa_requerido = False
                        st.rerun()
                    else:
                        st.error("✗ codigo mfa invalido")
                except Exception as e:
                    st.error(f"erro: {e}")
        else:
            username = st.text_input("👤 usuario", placeholder="admin")
            senha = st.text_input("🔑 senha", type="password", placeholder="admin123")
            if st.button("📲 entrar", use_container_width=True):
                sucesso, mensagem = fazer_login(username, senha)
                if sucesso:
                    st.success(mensagem)
                    st.rerun()
                else:
                    st.error(mensagem)
        st.markdown("---")
        st.info("💡 demo: admin / admin123")


@st.cache_data(ttl=10)
def get_data(limite=500):
    try:
        leituras = list(collection_leituras.find({}, {'_id': 0}).sort('timestamp', -1).limit(limite))
        if leituras:
            df = pd.DataFrame(leituras)
            if 'timestamp' in df.columns:
                try:
                    df['timestamp'] = pd.to_datetime(df['timestamp'], format='ISO8601')
                except:
                    try:
                        df['timestamp'] = pd.to_datetime(df['timestamp'], format='mixed')
                    except:
                        pass
            return df
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Erro ao buscar dados: {e}")
        return pd.DataFrame()


def criar_grafico_linha(df):
    """Gráfico de linha melhorado"""
    if df.empty:
        return None
    try:
        df_sorted = df.sort_values('timestamp')
        fig = px.line(
            df_sorted,
            x='timestamp',
            y='peso_kg',
            title='📈 Evolução do Peso de Resíduos',
            markers=True,
            line_shape='spline',
            hover_data={'peso_kg': ':.2f', 'timestamp': '|%d/%m/%y %H:%M'}
        )
        fig.update_traces(
            line=dict(color='#10b981', width=3),
            marker=dict(size=8, color='#059669', line=dict(width=2, color='#10b981'))
        )
        fig.update_layout(
            hovermode='x unified',
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#f3f4f6'),
            xaxis_title='Data/Hora',
            yaxis_title='Peso (kg)',
            height=400
        )
        return fig
    except Exception as e:
        st.warning(f"erro ao plotar: {e}")
        return None


def criar_grafico_histograma(df):
    """Histograma melhorado"""
    if df.empty:
        return None
    try:
        fig = px.histogram(
            df,
            x='peso_kg',
            nbins=20,
            title='📊 Distribuição de Peso',
            labels={'peso_kg': 'Peso (kg)', 'count': 'Frequência'}
        )
        fig.update_traces(marker=dict(color='#10b981', line=dict(color='#059669', width=2)))
        fig.update_layout(
            hovermode='x unified',
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#f3f4f6'),
            height=400
        )
        return fig
    except Exception as e:
        st.warning(f"erro ao plotar: {e}")
        return None


def criar_grafico_barras(df_group, titulo, xlabel, ylabel):
    """Gráfico de barras genérico"""
    if df_group.empty:
        return None
    try:
        fig = px.bar(
            df_group,
            title=titulo,
            labels={xlabel: xlabel, ylabel: ylabel},
            text=ylabel
        )
        fig.update_traces(
            marker=dict(color='#10b981', line=dict(color='#059669', width=2)),
            textposition='auto'
        )
        fig.update_layout(
            hovermode='x unified',
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#f3f4f6'),
            height=350,
            showlegend=False
        )
        return fig
    except Exception as e:
        st.warning(f"erro ao plotar: {e}")
        return None


def dashboard_principal():
    st.title("♻️ Dashboard Inteligente de Resíduos v4.0")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown(f"### 👤 {st.session_state.usuario_logado} · **{st.session_state.role.upper()}**")
    with col3:
        if st.button("🚪 logout", use_container_width=True):
            fazer_logout()
            st.rerun()
    
    st.markdown("---")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Dashboard",
        "📈 Big Data",
        "🤖 Predições",
        "⚠️ Anomalias",
        "⚙️ Admin"
    ])
    
    with tab1:
        st.markdown("## 📡 Monitoramento em Tempo Real")
        df = get_data()
        
        if df.empty:
            st.warning("❌ Nenhum dado disponível")
        else:
            col1, col2, col3, col4 = st.columns(4)
            stats = {
                'peso_total': float(df['peso_kg'].sum()),
                'peso_medio': float(df['peso_kg'].mean()),
                'temperatura_media': float(df['temperatura'].mean()) if 'temperatura' in df.columns else 0,
                'umidade_media': float(df['umidade'].mean()) if 'umidade' in df.columns else 0,
            }
            
            with col1:
                st.metric("⚖️ Peso Total", f"{stats['peso_total']:.2f} kg")
            with col2:
                st.metric("📏 Peso Médio", f"{stats['peso_medio']:.3f} kg")
            with col3:
                st.metric("🌡️ Temperatura", f"{stats['temperatura_media']:.1f}°C")
            with col4:
                st.metric("💧 Umidade", f"{stats['umidade_media']:.1f}%")
            
            st.markdown("---")
            
            col1, col2 = st.columns(2)
            with col1:
                fig_linha = criar_grafico_linha(df)
                if fig_linha:
                    st.plotly_chart(fig_linha, use_container_width=True)
            
            with col2:
                fig_hist = criar_grafico_histograma(df)
                if fig_hist:
                    st.plotly_chart(fig_hist, use_container_width=True)
    
    with tab2:
        st.markdown("## 📊 Análise de Padrões")
        df = get_data()
        
        if not df.empty:
            try:
                df['timestamp_dt'] = pd.to_datetime(df['timestamp'], format='ISO8601', errors='coerce')
                if df['timestamp_dt'].isna().all():
                    df['timestamp_dt'] = pd.to_datetime(df['timestamp'], format='mixed', errors='coerce')
                
                df['hora'] = df['timestamp_dt'].dt.hour
                df['dia_semana'] = df['timestamp_dt'].dt.day_name()
                
                col1, col2 = st.columns(2)
                
                with col1:
                    geracao_hora = df.groupby('hora')['peso_kg'].sum().reset_index()
                    fig_hora = criar_grafico_barras(geracao_hora, '⏰ Geração por Hora', 'hora', 'peso_kg')
                    if fig_hora:
                        st.plotly_chart(fig_hora, use_container_width=True)
                
                with col2:
                    geracao_dia = df.groupby('dia_semana')['peso_kg'].sum().reset_index()
                    fig_dia = criar_grafico_barras(geracao_dia, '📅 Geração por Dia', 'dia_semana', 'peso_kg')
                    if fig_dia:
                        st.plotly_chart(fig_dia, use_container_width=True)
                
                st.markdown("### 📊 Estatísticas Descritivas")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("📈 Máximo", f"{df['peso_kg'].max():.2f} kg")
                with col2:
                    st.metric("📉 Mínimo", f"{df['peso_kg'].min():.2f} kg")
                with col3:
                    st.metric("📌 Mediana", f"{df['peso_kg'].median():.2f} kg")
                with col4:
                    st.metric("📊 Desvio Padrão", f"{df['peso_kg'].std():.3f} kg")
                    
            except Exception as e:
                st.error(f"Erro na análise: {e}")
    
    with tab3:
        st.markdown("## 🤖 Predições com ML")
        st.info("🔄 Módulo de predições com machine learning está pronto na API v2.0")
    
    with tab4:
        st.markdown("## ⚠️ Detecção de Anomalias")
        df = get_data()
        
        if not df.empty:
            media = df['peso_kg'].mean()
            desvio = df['peso_kg'].std()
            limite = media + (2 * desvio)
            anomalias = df[df['peso_kg'] > limite]
            
            if len(anomalias) > 0:
                st.warning(f"🚨 Atenção: **{len(anomalias)}** anomalias detectadas")
                st.dataframe(
                    anomalias[['timestamp', 'peso_kg', 'sensor_id']],
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.success("✅ Nenhuma anomalia detectada")
    
    with tab5:
        if st.session_state.role == 'admin':
            st.markdown("## ⚙️ Painel Administrativo")
            
            sub_tab1, sub_tab2, sub_tab3, sub_tab4 = st.tabs([
                "👥 Usuários",
                "🔐 MFA",
                "📋 Auditoria",
                "ℹ️ Sistema"
            ])
            
            with sub_tab1:
                st.markdown("### 👥 Gerenciar Usuários")
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    usuarios = list(collection_usuarios.find({}, {'_id': 0, 'hash_senha': 0, 'salt': 0}))
                    if usuarios:
                        df_usuarios = pd.DataFrame(usuarios)
                        st.dataframe(df_usuarios, use_container_width=True, hide_index=True)
                
                with col2:
                    st.markdown("### ➕ Novo Usuário")
                    novo_username = st.text_input("Username")
                    novo_nome = st.text_input("Nome Completo")
                    novo_senha = st.text_input("Senha", type="password")
                    novo_role = st.selectbox("Role", ["usuario", "gestor", "admin"])
                    novo_email = st.text_input("Email")
                    
                    if st.button("✓ Criar Usuário", use_container_width=True):
                        try:
                            response = requests.post(
                                f"{API_URL}/api/criar-usuario",
                                json={
                                    "username": novo_username,
                                    "senha": novo_senha,
                                    "nome": novo_nome,
                                    "role": novo_role,
                                    "email": novo_email
                                },
                                headers={"Authorization": f"Bearer {st.session_state.token}"}
                            )
                            if response.status_code == 201:
                                st.success("✓ Usuário criado com sucesso")
                                st.cache_data.clear()
                                st.rerun()
                            else:
                                st.error(response.json().get('erro', 'erro ao criar'))
                        except Exception as e:
                            st.error(f"erro: {e}")
            
            with sub_tab2:
                st.markdown("### 🔐 Gerenciar MFA")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### Status MFA")
                    usuarios = list(collection_usuarios.find({}, {'_id': 0, 'username': 1, 'mfa_ativado': 1}))
                    if usuarios:
                        for usuario in usuarios:
                            mfa_status = "✅ ativado" if usuario.get('mfa_ativado') else "❌ desativado"
                            st.write(f"**{usuario['username']}**: {mfa_status}")
                
                with col2:
                    st.markdown("#### Ativar MFA")
                    usuarios = list(collection_usuarios.find({}, {'_id': 0, 'username': 1}))
                    usernames = [u['username'] for u in usuarios]
                    usuario_selecionado = st.selectbox("Usuário", usernames, key="mfa_user_select")
                    
                    if st.button("📱 Gerar QR Code", key="btn_gerar_qr", use_container_width=True):
                        try:
                            response = requests.post(
                                f"{API_URL}/api/mfa/gerar-qrcode",
                                headers={"Authorization": f"Bearer {st.session_state.token}"}
                            )
                            
                            if response.status_code == 200:
                                dados = response.json()
                                st.session_state.mfa_qr_code = dados['qr_code']
                                st.session_state.mfa_secret = dados['secret']
                                st.success("✓ QR Code gerado! Escaneia no Google Authenticator")
                            else:
                                st.error("erro ao gerar qr code")
                        except Exception as e:
                            st.error(f"erro: {e}")
                    
                    if st.session_state.mfa_qr_code:
                        st.markdown("#### 1️⃣ Escanear QR Code")
                        qr_code_img = st.session_state.mfa_qr_code
                        if qr_code_img.startswith('data:image'):
                            img_data = qr_code_img.split(',')[1]
                            st.image(f"data:image/png;base64,{img_data}", width=250)
                        
                        st.markdown("#### 2️⃣ Digitar Código")
                        codigo = st.text_input("Código (6 dígitos)", max_chars=6, key="mfa_codigo_input")
                        
                        if len(codigo) == 6:
                            if st.button("✓ Ativar MFA", key="btn_ativar_mfa", use_container_width=True):
                                try:
                                    response_ativar = requests.post(
                                        f"{API_URL}/api/mfa/ativar",
                                        json={"codigo": codigo},
                                        headers={"Authorization": f"Bearer {st.session_state.token}"}
                                    )
                                    
                                    if response_ativar.status_code == 200:
                                        st.success("✓ MFA ativado com sucesso!")
                                        st.session_state.mfa_qr_code = None
                                        st.session_state.mfa_secret = None
                                        st.cache_data.clear()
                                        import time
                                        time.sleep(2)
                                        st.rerun()
                                    else:
                                        st.error(f"erro: {response_ativar.json().get('erro', 'erro desconhecido')}")
                                except Exception as e:
                                    st.error(f"erro na requisição: {e}")
                        else:
                            st.info(f"📝 Digite 6 dígitos ({len(codigo)}/6)")
            
            with sub_tab3:
                st.markdown("### 📋 Logs de Auditoria")
                logs = list(collection_auditoria.find({}, {'_id': 0}).sort('timestamp', -1).limit(50))
                if logs:
                    st.dataframe(pd.DataFrame(logs), use_container_width=True, hide_index=True)
            
            with sub_tab4:
                st.markdown("### ℹ️ Informações do Sistema")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("📊 Total de Leituras", len(get_data()))
                    usuarios_count = len(list(collection_usuarios.find({})))
                    st.metric("👥 Usuários Cadastrados", usuarios_count)
                
                with col2:
                    logs_count = len(list(collection_auditoria.find({})))
                    st.metric("📋 Logs de Auditoria", logs_count)
        else:
            st.error("❌ Acesso restrito a administradores")


def main():
    # Configurar tema
    tema_claro = set_theme()
    
    if st.session_state.usuario_logado and not st.session_state.mfa_requerido:
        dashboard_principal()
    else:
        tela_login()


if __name__ == "__main__":
    main()