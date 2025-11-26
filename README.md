# ♻️ Lixeira Inteligente IoT - Sistema Completo

> **Dashboard inteligente para monitoramento e análise de resíduos com autenticação MFA, analytics em tempo real e integração IoT**

![Version](https://img.shields.io/badge/version-4.0-green)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Flask](https://img.shields.io/badge/flask-2.0%2B-red)
![Streamlit](https://img.shields.io/badge/streamlit-1.28%2B-orange)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 📋 Visão Geral

O **Lixeira Inteligente** é uma solução completa para monitoramento de resíduos, combinando:

- 🔐 **Autenticação com MFA** (Google Authenticator)
- 📊 **Dashboard visual** (tema claro/escuro)
- 📈 **Analytics em tempo real** com gráficos interativos
- ⚠️ **Detecção de anomalias** automática
- 🤖 **Predições com ML**
- 📡 **Integração IoT** (ESP32/ThingSpeak)
- 🛡️ **Auditoria completa**

---

## 🗂️ Estrutura do Projeto

```
lixeira-inteligente-iot/
├── projeto-lixeira-dashboard/
│   ├── dashboard.py              # Dashboard Streamlit (v4.0)
│   ├── requirements.txt           # Dependências do frontend
│   └── .streamlit/
│       └── config.toml            # Config do Streamlit
│
├── app_v2.py                      # API Flask principal
├── auth.py                        # Módulo de autenticação
├── mfa.py                         # Módulo de MFA (TOTP)
├── analytics.py                   # Análise de dados
├── requirements-full.txt          # Dependências backend + frontend
│
├── test_api.py                    # Testes da API
├── .env                           # Variáveis de ambiente
├── .gitignore
└── README.md                      # Este arquivo
```

---

## 🚀 Instalação Rápida

### 1️⃣ **Pré-requisitos**

- Python 3.10+
- MongoDB (local ou Atlas)
- Git
- pip/conda

### 2️⃣ **Clone o Repositório**

```bash
git clone https://github.com/seu-usuario/lixeira-inteligente-iot.git
cd lixeira-inteligente-iot
```

### 3️⃣ **Crie um Ambiente Virtual**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 4️⃣ **Instale as Dependências**

```bash
# Instalar todas as dependências (API + Dashboard)
pip install -r requirements-full.txt

# Ou separadamente:
# Backend
pip install flask flask-cors pymongo python-dotenv pyotp qrcode pillow

# Frontend
pip install streamlit pandas plotly
```

### 5️⃣ **Configure o Arquivo .env**

Crie um arquivo `.env` na raiz do projeto:

```env
# MongoDB
MONGODB_URI=mongodb+srv://usuario:senha@cluster0.mongodb.net/?retryWrites=true&w=majority

# Flask
FLASK_ENV=development
DEBUG=True
PORT=5000

# Segurança
SECRET_KEY=sua_chave_secreta_aqui_minimo_32_caracteres

# MFA
TOTP_ISSUER=Lixeira Inteligente
```

**💡 Dica:** Substitua `usuario:senha` pelas suas credenciais do MongoDB Atlas!

### 6️⃣ **Inicie os Serviços**

**Terminal 1 - API Flask:**
```bash
python app_v2.py
```

Você verá:
```
* Running on http://0.0.0.0:5000
```

**Terminal 2 - Dashboard Streamlit:**
```bash
cd projeto-lixeira-dashboard
streamlit run dashboard.py
```

Você verá:
```
Local URL: http://localhost:8501
Network URL: http://seu-ip:8501
```

---

## 📦 Dependências

### Backend (`requirements-full.txt`)

```
Flask==2.3.3
Flask-CORS==4.0.0
pymongo==4.5.0
python-dotenv==1.0.0
pyotp==2.9.0
qrcode==7.4.2
Pillow==10.0.0
```

### Frontend

```
streamlit==1.28.0
pandas==2.0.3
plotly==5.17.0
pymongo==4.5.0
python-dotenv==1.0.0
```

---

## 🔑 Primeira Execução

### 1. Login padrão

```
Usuário: admin
Senha: admin123
```

### 2. Ativar MFA (Recomendado)

1. Acesse **⚙️ Admin → 🔐 MFA**
2. Clique em **📱 Gerar QR Code**
3. Abra **Google Authenticator** e escaneia o QR
4. Digite o código de 6 dígitos
5. Clique em **✓ Ativar MFA**

### 3. Testar API

```bash
python test_api.py
```

---

## 📚 Uso da API

### Autenticação

**POST** `/api/login`
```bash
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "senha": "admin123"}'
```

**Resposta:**
```json
{
  "sucesso": true,
  "token": "seu_token_aqui",
  "usuario": {"username": "admin", "role": "admin"},
  "requer_mfa": false
}
```

### MFA

**POST** `/api/mfa/gerar-qrcode`
```bash
curl -X POST http://localhost:5000/api/mfa/gerar-qrcode \
  -H "Authorization: Bearer seu_token_aqui"
```

**POST** `/api/mfa/ativar`
```bash
curl -X POST http://localhost:5000/api/mfa/ativar \
  -H "Authorization: Bearer seu_token_aqui" \
  -H "Content-Type: application/json" \
  -d '{"codigo": "123456"}'
```

**POST** `/api/mfa/verificar`
```bash
curl -X POST http://localhost:5000/api/mfa/verificar \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "codigo": "123456"}'
```

### Dados

**POST** `/api/dados` (Enviar leitura de sensor)
```bash
curl -X POST http://localhost:5000/api/dados \
  -H "Content-Type: application/json" \
  -d '{
    "peso_kg": 12.5,
    "sensor_id": "esp32-001",
    "temperatura": 22.5,
    "umidade": 65.0,
    "localizacao": "entrada"
  }'
```

**GET** `/api/leituras?limite=100`
```bash
curl -X GET http://localhost:5000/api/leituras?limite=100 \
  -H "Authorization: Bearer seu_token_aqui"
```

### Analytics

**GET** `/api/analytics/padroes?dias=30`
```bash
curl -X GET http://localhost:5000/api/analytics/padroes?dias=30 \
  -H "Authorization: Bearer seu_token_aqui"
```

**GET** `/api/analytics/anomalias?sensibilidade=2.0`
```bash
curl -X GET http://localhost:5000/api/analytics/anomalias?sensibilidade=2.0 \
  -H "Authorization: Bearer seu_token_aqui"
```

---

## 🔐 Segurança

### MFA (Multi-Factor Authentication)

- ✅ TOTP baseado em tempo (RFC 6238)
- ✅ Compatível com Google Authenticator, Authy, Microsoft Authenticator
- ✅ Tolerância de ±5 períodos (fuso horário)
- ✅ Secrets guardados de forma segura no MongoDB

### Autenticação

- ✅ Senhas com hash (pbkdf2)
- ✅ Tokens JWT
- ✅ CORS habilitado
- ✅ Rate limiting recomendado

### Auditoria

- ✅ Logs de todas as operações
- ✅ Rastreamento de login/logout
- ✅ Histórico de alterações
- ✅ Visualização em tempo real

---

## 🛠️ Solução de Problemas

### Erro: `MONGODB_URI not configured`

**Solução:**
1. Crie um arquivo `.env` na raiz
2. Adicione sua URI do MongoDB Atlas
3. Reinicie a aplicação

```env
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/dbname
```

### Erro: `Port 5000 already in use`

**Solução:**
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :5000
kill -9 <PID>
```

### Erro: `ModuleNotFoundError: No module named 'flask'`

**Solução:**
```bash
pip install -r requirements-full.txt
```

### MFA não funciona

**Checklist:**
- [ ] Relógio do sistema sincronizado
- [ ] Código com 6 dígitos
- [ ] Google Authenticator com o app correto
- [ ] Secret salvo corretamente no banco

---

## 📊 Recursos do Dashboard

### 🎨 Temas
- ☀️ **Claro** - Paleta verde ecológica
- 🌙 **Escuro** - Tema elegante com verde vibrante

### 📊 Visualizações
- **Métricas em tempo real** - Peso, temperatura, umidade
- **Gráficos de linha** - Evolução com animação
- **Histogramas** - Distribuição de peso
- **Gráficos de barras** - Padrões por hora/dia

### 🔍 Análises
- **Padrões de geração** - Identificar picos
- **Estatísticas** - Máx, mín, mediana, desvio padrão
- **Anomalias** - Detecção automática
- **Predições** - Próximos 7 dias (ML ready)

### ⚙️ Admin
- 👥 Gerenciar usuários
- 🔐 Configurar MFA
- 📋 Logs de auditoria
- ℹ️ Informações do sistema

---

## 🚀 Deploy

### Heroku

```bash
# 1. Login
heroku login

# 2. Criar app
heroku create seu-app-lixeira

# 3. Adicionar variáveis de ambiente
heroku config:set MONGODB_URI="sua_uri"

# 4. Deploy
git push heroku main
```

### Docker

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements-full.txt .
RUN pip install -r requirements-full.txt

COPY . .

EXPOSE 5000 8501

CMD ["python", "app_v2.py"] &
CMD ["streamlit", "run", "projeto-lixeira-dashboard/dashboard.py"]
```

---

## 📖 Documentação Adicional

- [API Endpoints](./docs/API.md)
- [Configuração MongoDB](./docs/MONGODB.md)
- [Guia MFA](./docs/MFA.md)
- [Deploy Guide](./docs/DEPLOY.md)

---

## 👥 Contribuidores

- **b3rnardo15** - Desenvolvedor principal

---

## 📝 Licença

MIT License - veja `LICENSE` para detalhes

---

## 🤝 Suporte

Encontrou um bug? Abra uma [issue](https://github.com/seu-usuario/lixeira-inteligente-iot/issues)

Tem uma sugestão? Faça um [pull request](https://github.com/seu-usuario/lixeira-inteligente-iot/pulls)

---

## 📞 Contato

- Email: seu-email@example.com
- GitHub: [@b3rnardo15](https://github.com/b3rnardo15)
- LinkedIn: [Seu Perfil](https://linkedin.com/in/seu-perfil)

---

**Desenvolvido com 💚 por b3rnardo15**

**Última atualização:** 25 de Novembro de 2025
