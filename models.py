from pydantic import BaseModel, Field
from typing import Optional

class MikrotikAuth(BaseModel):
    host: str
    port: int = 8728
    username: str
    password: str

class NatRule(BaseModel):
    chain: str = Field("dstnat", description="dstnat ou srcnat")
    action: str = Field("masquerade", description="masquerade, dst-nat, etc.")
    src_address: Optional[str]
    dst_address: Optional[str]
    to_addresses: Optional[str]
    protocol: Optional[str]
    dst_port: Optional[str]

class AddressListEntry(BaseModel):
    address: str
    list: str

class FilterRule(BaseModel):
    chain: str
    action: str
    src_address: Optional[str]
    dst_address: Optional[str]
    protocol: Optional[str]
    dst_port: Optional[str]

class DnsEntry(BaseModel):
    address: str
    comment: Optional[str]
