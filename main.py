import os

from dotenv import load_dotenv
from web3 import Web3

load_dotenv()


class BNBChain:
    chain_id = 56
    rpc_url = "https://bsc-dataseed1.binance.org/"


# 合约地址
contract_address = "0x9055222122F974B7E6ac8eaAC952A6B6039d26e1"  # 签到合约地址

# 合约 ABI（这是一个示例 ABI，实际使用时需要用你的合约的 ABI）
contract_abi = [
    {
        "constant": False,
        "inputs": [],
        "name": "checkIn",
        "outputs": [],
        "payable": True,
        "stateMutability": "payable",
        "type": "function",
    }
]


# 账户地址和私钥（仅示例，不要在实际场景中使用）
# todo
from_address = os.getenv("from_address")
private_key = os.getenv("private_key")

web3 = Web3(Web3.HTTPProvider(BNBChain.rpc_url))

# 测试网络联通状态
web3.is_connected()

# 创建合约实例
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# 获取地址余额
wallet = web3.to_checksum_address(from_address)
wei = web3.eth.get_balance(wallet)
balance = web3.from_wei(wei, "ether")
print(f"余额为:{balance} BNB")

# 构建交易
print(f"gas:{web3.eth.gas_price}")
## 交易计数flag
nonce = web3.eth.get_transaction_count(web3.to_checksum_address(from_address))
print(f"nonce:{nonce}")

transaction = {
    "chainId": BNBChain.chain_id,
    "gas": 50000,  # 估算 gas 费用
    "gasPrice": web3.to_wei("1", "gwei"),  # 设置 gas price
    "nonce": nonce,
}

## 构建合约交互参数
transaction = contract.functions.checkIn().build_transaction(transaction)

# 签名交易
signed_txn = web3.eth.account.sign_transaction(transaction, private_key)

# 发送交易
txn_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)

# 打印交易哈希
print(f"Transaction sent with hash: {txn_hash.hex()}")

# 等待交易确认
txn_receipt = web3.eth.wait_for_transaction_receipt(txn_hash)
print(f"Transaction receipt: {txn_receipt}")
