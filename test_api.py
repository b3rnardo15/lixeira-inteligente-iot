"""
Script para testar a API da Lixeira Inteligente localmente
Simula requisições do ESP32 sem precisar do dispositivo
"""

import requests
import json
from datetime import datetime, timedelta
import time

# URL da API (mude se estiver em outro lugar)
API_URL = "http://localhost:5000"

def test_conexao():
    """Testa se a API está online"""
    print("\n📍 Testando conexão com API...")
    try:
        response = requests.get(f"{API_URL}/api/saude")
        print(f" Status: {response.status_code}")
        print(f"Resposta: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print(" Erro: Não conseguiu conectar à API")
        print(f"   Certifique-se que a API está rodando em {API_URL}")
        return False

def test_home():
    """Testa o endpoint home"""
    print("\n Testando endpoint home...")
    try:
        response = requests.get(f"{API_URL}/")
        print(f" Status: {response.status_code}")
        print(f"Resposta: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f" Erro: {e}")

def enviar_dado_teste(peso_kg, sensor_id="ESP32_001", temperatura=24.5, umidade=65.2):
    """Envia um dado de teste para a API (simula ESP32)"""
    print(f"\n Enviando dado de teste (peso: {peso_kg} kg)...")
    
    payload = {
        "peso_kg": peso_kg,
        "sensor_id": sensor_id,
        "temperatura": temperatura,
        "umidade": umidade,
        "localizacao": "Bloco A - SENAC PE",
        "timestamp": datetime.utcnow().isoformat()
    }
    
    try:
        response = requests.post(
            f"{API_URL}/api/dados",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        print(f" Status: {response.status_code}")
        resultado = response.json()
        print(f"Resposta: {json.dumps(resultado, indent=2)}")
        return response.status_code == 201
        
    except Exception as e:
        print(f" Erro: {e}")
        return False

def obter_leituras(limite=10):
    """Obtém as leituras armazenadas"""
    print(f"\n Obtendo últimas {limite} leituras...")
    
    try:
        response = requests.get(
            f"{API_URL}/api/leituras?limite={limite}&ordenar=desc"
        )
        
        print(f" Status: {response.status_code}")
        resultado = response.json()
        
        if resultado['success']:
            print(f"Total de leituras: {resultado['total']}")
            print("\nDados:")
            for i, leitura in enumerate(resultado['leituras'], 1):
                print(f"\n{i}. {leitura['timestamp']}")
                print(f"   Peso: {leitura['peso_kg']} kg")
                print(f"   Sensor: {leitura['sensor_id']}")
                print(f"   Temp: {leitura['temperatura']}°C")
                print(f"   Umidade: {leitura['umidade']}%")
        
        return result.success
        
    except Exception as e:
        print(f" Erro: {e}")
        return False

def obter_estatisticas():
    """Obtém estatísticas dos dados"""
    print("\n Obtendo estatísticas...")
    
    try:
        response = requests.get(f"{API_URL}/api/estatisticas")
        
        print(f" Status: {response.status_code}")
        resultado = response.json()
        
        if resultado['success']:
            stats = resultado['estatisticas']
            print("\nEstatísticas dos dados:")
            print(f"  Total de leituras: {stats['total_leituras']}")
            print(f"  Peso total: {stats['peso_total']} kg")
            print(f"  Peso médio: {stats['peso_medio']} kg")
            print(f"  Peso máximo: {stats['peso_maximo']} kg")
            print(f"  Peso mínimo: {stats['peso_minimo']} kg")
            print(f"  Temp média: {stats['temperatura_media']}°C")
            print(f"  Umidade média: {stats['umidade_media']}%")
        
        return resultado['success']
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def listar_sensores():
    """Lista todos os sensores cadastrados"""
    print("\n Listando sensores...")
    
    try:
        response = requests.get(f"{API_URL}/api/sensores")
        
        print(f" Status: {response.status_code}")
        resultado = response.json()
        
        if resultado['success']:
            print(f"Total de sensores: {resultado['total_sensores']}")
            for sensor in resultado['sensores']:
                print(f"  - {sensor}")
        
        return resultado['success']
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def simular_uso_lixeira():
    """Simula o uso da lixeira com múltiplos dados"""
    print("\n Simulando uso da lixeira por 30 segundos...")
    
    pesos = [0.5, 1.2, 0.8, 2.1, 1.5, 0.9, 3.2, 1.1]
    
    for i, peso in enumerate(pesos, 1):
        print(f"\n[{i}/{len(pesos)}] Simulando descarte de {peso} kg...")
        enviar_dado_teste(peso_kg=peso)
        
        if i < len(pesos):
            time.sleep(2)  # Aguarda 2 segundos entre envios

def menu_testes():
    """Menu interativo de testes"""
    while True:
        print("\n" + "="*50)
        print(" MENU DE TESTES - API Lixeira Inteligente")
        print("="*50)
        print("1. Testar conexão com API")
        print("2. Listar endpoints")
        print("3. Enviar dado de teste único")
        print("4. Listar sensores")
        print("5. Obter últimas leituras")
        print("6. Obter estatísticas")
        print("7. Simular múltiplos descartes")
        print("8. Sair")
        print("="*50)
        
        escolha = input("Escolha uma opção (1-8): ").strip()
        
        if escolha == "1":
            test_conexao()
        elif escolha == "2":
            test_home()
        elif escolha == "3":
            peso = float(input("Digite o peso em kg: "))
            enviar_dado_teste(peso_kg=peso)
        elif escolha == "4":
            listar_sensores()
        elif escolha == "5":
            limite = int(input("Quantas leituras? (padrão 10): ") or "10")
            obter_leituras(limite=limite)
        elif escolha == "6":
            obter_estatisticas()
        elif escolha == "7":
            simular_uso_lixeira()
        elif escolha == "8":
            print("\n👋 Até logo!")
            break
        else:
            print("❌ Opção inválida!")

if __name__ == "__main__":
    print("""
    ╔════════════════════════════════════════════╗
    ║  🧪 TESTE DA API - Lixeira Inteligente    ║
    ║                                            ║
    ║  Certifique-se que a API está rodando:    ║
    ║  python app.py                             ║
    ╚════════════════════════════════════════════╝
    """)
    
    # Teste de conexão inicial
    if test_conexao():
        menu_testes()
    else:
        print("\n Não foi possível conectar à API.")
        print("Inicie a API com: python app.py")