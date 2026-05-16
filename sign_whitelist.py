import json
import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

with open("private.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None)

try:
    with open("whitelist.json", "r") as f:
        data = json.load(f)
except FileNotFoundError:
    data = {"hwid_list": []}

# 在这里手动添加新的 HWID（每次添加用户时修改）
# data["hwid_list"].append("rvnp-xxxxxxxxxxxxxxxx")

if "signature" in data:
    del data["signature"]

json_without_sig = json.dumps(data, indent=2)
signature = private_key.sign(
    json_without_sig.encode('utf-8'),
    padding.PKCS1v15(),
    hashes.SHA256()
)
data["signature"] = base64.b64encode(signature).decode('ascii')

with open("whitelist.json", "w") as f:
    json.dump(data, f, indent=2)

print("已更新 whitelist.json，当前列表:", data["hwid_list"])