from routeros_api import RouterOsApiPool

def get_mikrotik_api(host: str, username: str, password: str, port: int = 8728):
    pool = RouterOsApiPool(
        host,
        username=username,
        password=password,
        port=port,
        plaintext_login=True
    )
    return pool.get_api(), pool
