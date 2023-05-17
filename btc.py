import hashlib
import time
import base58
import ecdsa
import requests

file_path = 'btc.txt'  # 修改为指定的文件路径

while True:
    # 随机生成比特币私钥
    private_key = ecdsa.util.randrange(pow(2, 256))

    # 将私钥通过椭圆曲线加密算法转换为公钥
    signing_key = ecdsa.SigningKey.from_secret_exponent(private_key, curve=ecdsa.SECP256k1)
    verifying_key = signing_key.get_verifying_key()
    public_key = bytes.fromhex("04") + verifying_key.to_string()

    # 生成比特币地址
    sha256_h = hashlib.sha256(public_key).digest()
    ripe160_h = hashlib.new('ripemd160', sha256_h).digest()
    address = base58.b58encode_check(bytes.fromhex("00") + ripe160_h).decode('utf-8')

    # 查询比特币地址余额
    def get_btc_balance(address):
        api_url = "https://chain.api.btc.com/v3/address/" + address
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            balance = data["data"]["balance"]
            return balance
        else:
            return None

    balance = get_btc_balance(address)
    if balance is not None:  # 只有余额不为0时才写入文本文件
        # 输出结果
        print("比特币私钥：", hex(private_key))
        print("比特币公钥：", public_key.hex())
        print("比特币地址：", address)
        print("比特币地址余额：%s BTC" % balance)

        if balance != 0:
            # 将私钥、公钥、地址和余额拼接成字符串
            result = f'Private key: {hex(private_key)}\nPublic key: {public_key.hex()}\nAddress: {address}\nBalance: {balance} BTC\n\n'
            # 将结果写入指定的文本文件中
            with open(file_path, 'a') as f:
                f.write(result)
        else:
            continue
    else:
        print("查询余额失败!")



    #time.sleep(0.01)
