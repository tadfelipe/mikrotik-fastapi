# MikroTik FastAPI

API RESTful em Python para executar tarefas principais no MikroTik RouterOS via API nativa (porta 8728).

## Funcionalidades
- 🖧 Listar Interfaces
- 🌐 Gerenciar NAT (listar, adicionar, remover, buscar por comentário)
- 💾 Gerar e baixar Backup
- 📋 Gerenciar Address List (listar, adicionar, remover, buscar por comentário)
- 🚫 Gerenciar Filter Rules (listar, adicionar, remover, buscar por comentário)
- 🧩 Gerenciar DNS estático (listar, adicionar, remover, buscar por comentário)

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

### Exemplo de requisição para buscar por comentário
```http
GET /nat?comment=exemplo de comentario
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
| GET    | /nat               | Listar regras NAT (opcionalmente, filtrar por comentário) |
| POST   | /nat               | Adicionar regra NAT                |
| DELETE | /nat/{id}          | Remover regra NAT                  |
| POST   | /backup            | Gerar e baixar backup              |
| GET    | /address-list      | Listar Address List (opcionalmente, filtrar por comentário) |
| POST   | /address-list      | Adicionar Address List             |
| DELETE | /address-list/{id} | Remover Address List               |
| GET    | /filter            | Listar Filter Rules (opcionalmente, filtrar por comentário) |
| POST   | /filter            | Adicionar Filter Rule              |
| DELETE | /filter/{id}       | Remover Filter Rule                |
| GET    | /dns               | Listar entradas DNS estático (opcionalmente, filtrar por comentário) |
| POST   | /dns               | Adicionar DNS estático             |
| DELETE | /dns/{id}          | Remover DNS estático               |
| GET    | /download/{file}   | Baixar arquivo de backup gerado    |
