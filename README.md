# MikroTik FastAPI

API RESTful em Python para executar tarefas principais no MikroTik RouterOS via API nativa (porta 8728).

## Funcionalidades
- 🖧 Listar Interfaces
- 🌐 Gerenciar NAT (listar, adicionar, remover)
- 💾 Gerar e baixar Backup
- 📋 Gerenciar Address List (listar, adicionar, remover)
- 🚫 Gerenciar Filter Rules (listar, adicionar, remover)
- 🧩 Gerenciar DNS estático (listar, adicionar, remover)

## Instalação
```bash
git clone https://github.com/tadfelipe/mikrotik-fastapi.git
cd mikrotik-fastapi
python3 -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Uso
```bash
uvicorn main:app --reload
```

### Exemplo de requisição
```http
POST /interfaces
Content-Type: application/json
{
  "host": "192.168.88.1",
  "port": 8728,
  "username": "admin",
  "password": "minhaSenha"
}
```

## Endpoints
| Método | Rota               | Descrição                          |
|--------|--------------------|------------------------------------|
| GET    | /interfaces        | Listar interfaces                  |
| GET    | /nat               | Listar regras NAT                  |
| POST   | /nat               | Adicionar regra NAT                |
| DELETE | /nat/{id}          | Remover regra NAT                  |
| POST   | /backup            | Gerar e baixar backup              |
| GET    | /address-list      | Listar Address List                |
| POST   | /address-list      | Adicionar Address List             |
| DELETE | /address-list/{id} | Remover Address List               |
| GET    | /filter            | Listar Filter Rules                |
| POST   | /filter            | Adicionar Filter Rule              |
| DELETE | /filter/{id}       | Remover Filter Rule                |
| GET    | /dns               | Listar entradas DNS estático       |
| POST   | /dns               | Adicionar DNS estático             |
| DELETE | /dns/{id}          | Remover DNS estático               |
| GET    | /download/{file}   | Baixar arquivo de backup gerado    |
