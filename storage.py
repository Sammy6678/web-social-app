import os
from datetime import datetime, timedelta
from azure.storage.blob import BlobSasPermissions, generate_blob_sas

account_name = os.getenv("STORAGE_ACCOUNT_NAME")
account_key = os.getenv("STORAGE_ACCOUNT_KEY")
container_name = os.getenv("BLOB_CONTAINER", "posts")

def generate_upload_sas(blob_name: str, minutes_valid: int = 10):
    sas = generate_blob_sas(
        account_name=account_name,
        container_name=container_name,
        blob_name=blob_name,
        account_key=account_key,
        permission=BlobSasPermissions(write=True, create=True),
        expiry=datetime.utcnow() + timedelta(minutes=minutes_valid)
    )
    url = f"https://{account_name}.blob.core.windows.net/{container_name}/{blob_name}?{sas}"
    return url
