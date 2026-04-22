import os
from pathlib import Path
from dotenv import load_dotenv

# Localiza o .env na raiz do projeto
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

print("--- Teste de Variáveis de Ambiente ---")
print(f"DATABASE_URL: {os.getenv('DATABASE_URL')}")
print(f"APP_NAME: {os.getenv('APP_NAME')}")
print(f"Caminho do .env tentado: {env_path}")