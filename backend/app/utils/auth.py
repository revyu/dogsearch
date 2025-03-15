import hmac
import hashlib
from typing import Dict
from fastapi import HTTPException
from ..config.settings import settings

def verify_vk_params(params: Dict[str, str]) -> bool:
    """
    Проверяет подпись параметров запуска от VK
    """
    if "sign" not in params:
        return False
        
    vk_subset = sorted(
        [(key, value) for key, value in params.items() if key.startswith("vk_")]
    )
    
    signature_string = "&".join([f"{key}={value}" for key, value in vk_subset])
    
    secret = settings.VK_SECRET_KEY.encode()
    signature = hmac.new(
        secret,
        signature_string.encode(),
        hashlib.sha256
    ).hexdigest()
    
    return signature == params["sign"]
