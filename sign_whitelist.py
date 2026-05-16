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

# 添加你的 HWID
data["hwid_list"].append("rvn-a3196c701b3bfd93")
data["hwid_list"].append("rvn-81ba3518933533c9")
data["hwid_list"].append("rvn-cd0c68c1ad3234b1")

# 移除旧签名
if "signature" in data:
    del data["signature"]

# 重要：签名时使用紧凑格式（无空格、无换行），只取 hwid_list 字段
signature_data = {"hwid_list": data["hwid_list"]}
json_without_sig = json.dumps(signature_data, separators=(',', ':'))

signature = private_key.sign(
    json_without_sig.encode('utf-8'),
    padding.PKCS1v15(),
    hashes.SHA256()
)
data["signature"] = base64.b64encode(signature).decode('ascii')

# 保存时仍用缩进格式，方便人读
with open("whitelist.json", "w") as f:
    json.dump(data, f, indent=2)

print("已更新 whitelist.json，当前列表:", data["hwid_list"])