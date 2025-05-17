import re
import logging

# 1) Defina o Filter que vai redigir username e password
class CredentialFilter(logging.Filter):
    def filter(self, record):
        # Aplica regex sobre a mensagem completa
        redacted = re.sub(
            r"(username=|password=)[^&\s]+",
            r"\1******",
            record.getMessage()
        )
        record.msg = redacted
        record.args = None
        return True

# 2) Anexe o filtro ao logger de access do Uvicorn
logging.getLogger("uvicorn.access").addFilter(CredentialFilter())
# (Opcional: para o logger de erros também)
# logging.getLogger("uvicorn.error").addFilter(CredentialFilter())

logging.getLogger("routeros_api").addFilter(CredentialFilter())
import logging
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import FileResponse
from models import MikrotikAuth, NatRule, AddressListEntry, FilterRule, DnsEntry
from mikrotik_client import get_mikrotik_api
import datetime
import os

app = FastAPI(title="MikroTik RouterOS API")

def with_api(auth: MikrotikAuth = Depends()):
    try:
        api, pool = get_mikrotik_api(auth.host, auth.username, auth.password, auth.port)
        return api, pool, auth
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Falha na conexão: {e}")

@app.get("/interfaces")
def list_interfaces(api_pool=Depends(with_api)):
    api, pool, _ = api_pool
    result = api.get_resource("/interface").get()
    pool.disconnect()
    return result
@app.get("/nat")
def list_nat(api_pool=Depends(with_api), comment: str = None):
    api, pool, auth = api_pool
    logging.info(f"Conectando ao MikroTik com o host: {auth.host}")
    rules = api.get_resource("/ip/firewall/nat").get()
    if comment:
        rules = [rule for rule in rules if comment.lower() in rule.get("comment", "").lower()]
    pool.disconnect()
    return rules

@app.post("/nat")
def add_nat(rule: NatRule, api_pool=Depends(with_api)):
    api, pool, _ = api_pool
    res = api.get_resource("/ip/firewall/nat").add(**rule.dict(exclude_none=True))
    pool.disconnect()
    return {"success": True, "id": res}

@app.delete("/nat/{rule_id}")
def delete_nat(rule_id: str, api_pool=Depends(with_api)):
    api, pool, _ = api_pool
    api.get_resource("/ip/firewall/nat").remove(**{".id": rule_id})
    pool.disconnect()
    return {"success": True}

@app.get("/address-list")
def list_address_list(api_pool=Depends(with_api), comment: str = None):
    api, pool, _ = api_pool
    lst = api.get_resource("/ip/firewall/address-list").get()
    if comment:
        lst = [entry for entry in lst if comment.lower() in entry.get("comment", "").lower()]
    pool.disconnect()
    return lst

@app.post("/address-list")
def add_address_list(entry: AddressListEntry, api_pool=Depends(with_api)):
    api, pool, _ = api_pool
    res = api.get_resource("/ip/firewall/address-list").add(**entry.dict())
    pool.disconnect()
    return {"success": True, "id": res}

@app.delete("/address-list/{entry_id}")
def delete_address_list(entry_id: str, api_pool=Depends(with_api)):
    api, pool, _ = api_pool
    api.get_resource("/ip/firewall/address-list").remove(**{".id": entry_id})
    pool.disconnect()
    return {"success": True}

@app.get("/filter")
def list_filter(api_pool=Depends(with_api), comment: str = None):
    api, pool, _ = api_pool
    rules = api.get_resource("/ip/firewall/filter").get()
    if comment:
        rules = [rule for rule in rules if comment.lower() in rule.get("comment", "").lower()]
    pool.disconnect()
    return rules

@app.post("/filter")
def add_filter(rule: FilterRule, api_pool=Depends(with_api)):
    api, pool, _ = api_pool
    res = api.get_resource("/ip/firewall/filter").add(**rule.dict(exclude_none=True))
    pool.disconnect()
    return {"success": True, "id": res}

@app.delete("/filter/{rule_id}")
def delete_filter(rule_id: str, api_pool=Depends(with_api)):
    api, pool, _ = api_pool
    api.get_resource("/ip/firewall/filter").remove(**{".id": rule_id})
    pool.disconnect()
    return {"success": True}

@app.get("/dns")
def list_dns(api_pool=Depends(with_api), comment: str = None):
    api, pool, _ = api_pool
    entries = api.get_resource("/ip/dns/static").get()
    if comment:
        entries = [entry for entry in entries if comment.lower() in entry.get("comment", "").lower()]
    pool.disconnect()
    return entries

@app.post("/dns")
def add_dns(entry: DnsEntry, api_pool=Depends(with_api)):
    api, pool, _ = api_pool
    res = api.get_resource("/ip/dns/static").add(**entry.dict(exclude_none=True))
    pool.disconnect()
    return {"success": True, "id": res}

@app.delete("/dns/{entry_id}")
def delete_dns(entry_id: str, api_pool=Depends(with_api)):
    api, pool, _ = api_pool
    api.get_resource("/ip/dns/static").remove(**{".id": entry_id})
    pool.disconnect()
    return {"success": True}

@app.post("/backup")
def do_backup(api_pool=Depends(with_api)):
    api, pool, auth = api_pool
    timestamp = datetime.datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    filename = f"backup_{auth.host}_{timestamp}.backup"
    api.get_resource("/system/backup").call("save", {"name": filename.replace('.backup','')})
    pool.disconnect()
    backup_path = os.path.join(os.getcwd(), filename)
    # Supondo que RouterOS salve no diretório atual via FTP/SCP configurado
    return FileResponse(path=backup_path, filename=filename, media_type='application/octet-stream')

@app.get("/download/{file_name}")
def download_file(file_name: str):
    file_path = os.path.join(os.getcwd(), file_name)
    if os.path.exists(file_path):
        return FileResponse(path=file_path, filename=file_name, media_type='application/octet-stream')
    raise HTTPException(status_code=404, detail="Arquivo não encontrado")
