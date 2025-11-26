# 🚀 Quick Start - Lixeira Inteligente

Siga este guia para colocar a aplicação rodando em **5 minutos**!

---

## ⚡ Início Rápido (5 min)

### 1. Clone e Entre no Diretório

```bash
git clone https://github.com/seu-usuario/lixeira-inteligente-iot.git
cd lixeira-inteligente-iot
```

### 2. Crie Ambiente Virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale Dependências

```bash
pip install -r requirements-full.txt
```

### 4. Configure o Banco de Dados

**Opção A: MongoDB Atlas (Recomendado - Cloud)**
1. Acesse https://www.mongodb.com/cloud/atlas
2. Crie uma conta gratuita
3. Crie um cluster (M0 é free)
4. Crie um usuário de banco de dados
5. Copie a connection string

**Opção B: MongoDB Local**
```bash
# Instalar MongoDB Community
# Depois iniciar:
mongod
```

### 5. Configure o .env

```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite o arquivo .env com suas credenciais
# Adicione sua MongoDB URI
```

**Seu .env deve ter:**
```env
MONGODB_URI=mongodb+srv://usuario:senha@seu-cluster.mongodb.net/lixeira_inteligente
FLASK_ENV=development
DEBUG=True
PORT=5000
SECRET_KEY=sua_chave_aleatorias_de_32_caracteres
```

### 6. Inicie a API

**Terminal 1:**
```bash
python app_v2.py
```

Você verá:
```
* Serving Flask app 'app'
* Running on http://0.0.0.0:5000
```

### 7. Inicie o Dashboard

**Terminal 2:**
```bash
cd projeto-lixeira-dashboard
streamlit run dashboard.py
```

Você verá:
```
Local URL: http://localhost:8501
```

### 8. Acesse

Abra seu navegador em: **http://localhost:8501**

---

## 🔐 Login Padrão

```
Usuário: admin
Senha: admin123
```

---

## 📱 Ativar MFA (Opcional mas Recomendado)

1. Faça login com admin/admin123
2. Vá em **⚙️ Admin → 🔐 MFA**
3. Clique **📱 Gerar QR Code**
4. Abra **Google Authenticator** (baixe se não tiver)
5. Escaneia o QR Code
6. Digite o código de 6 dígitos
7. Clique **✓ Ativar MFA**

---

## 🧪 Testar a API

### Health Check

```bash
curl http://localhost:5000/api/saude
```

### Fazer Login

```bash
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "senha": "admin123"
  }'
```

### Enviar Dados (IoT)

```bash
curl -X POST http://localhost:5000/api/dados \
  -H "Content-Type: application/json" \
  -d '{
    "peso_kg": 15.5,
    "sensor_id": "esp32-001",
    "temperatura": 22.5,
    "umidade": 65.0,
    "localizacao": "entrada"
  }'
```

---

## 🐛 Problemas Comuns

### ❌ `MONGODB_URI nao configurada`

**Solução:**
1. Crie o arquivo `.env` na raiz
2. Adicione sua MONGODB_URI
3. Reinicie a aplicação

### ❌ `Port 5000 already in use`

**Solução:**
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :5000
kill -9 <PID>
```

Ou mude no `.env`:
```env
PORT=5001
```

### ❌ `ModuleNotFoundError`

**Solução:**
```bash
# Verifique se venv está ativo
pip install -r requirements-full.txt
```

### ❌ Streamlit não carrega

**Solução:**
```bash
streamlit cache clear
streamlit run projeto-lixeira-dashboard/dashboard.py --logger.level=debug
```

---

## 📊 Dados de Teste

Para testar o dashboard com dados, execute:

```bash
python test_api.py
```

Isso vai:
- ✅ Criar usuário de teste
- ✅ Fazer login
- ✅ Enviar 100 leituras de teste
- ✅ Testar os endpoints principais

---

## 🌐 Estrutura de Pastas

```
lixeira-inteligente-iot/
├── projeto-lixeira-dashboard/
│   └── dashboard.py          ← Streamlit (porta 8501)
├── app_v2.py                 ← Flask API (porta 5000)
├── auth.py                   ← Autenticação
├── mfa.py                    ← MFA/TOTP
├── analytics.py              ← Análise de dados
├── .env.example              ← Copie para .env
├── requirements-full.txt     ← Dependências
└── README.md                 ← Documentação completa
```

---

## 🎯 Próximos Passos

1. ✅ **Criar MFA** - Segurança adicional
2. ✅ **Testar IoT** - Enviar dados de sensores
3. ✅ **Explorar Dashboard** - Ver gráficos e análises
4. ✅ **Ler Documentação** - Veja README.md completo
5. ✅ **Deploy** - Publique na nuvem (Heroku, Railway, etc)

---

## 📚 Recursos

- **README.md** - Documentação completa
- **API.md** - Documentação dos endpoints
- **MFA.md** - Guia de autenticação MFA

---

## 💡 Dicas

- 📱 Use Google Authenticator para MFA (mais seguro)
- 🔐 Mude a senha padrão do admin!
- 📊 Envie muitos dados para ver gráficos legais
- 🐳 Use Docker para deploy (veja Dockerfile)
- 📈 Configure alertas de anomalias

---

## ❓ Precisa de Ajuda?

1. Verifique o arquivo **README.md**
2. Leia os logs (verifique o terminal)
3. Abra uma [Issue](https://github.com/seu-usuario/lixeira-inteligente-iot/issues)

---

**Boa sorte! 🎉**

Desenvolvido com 💚 por **b3rnardo15**
