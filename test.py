from web3 import Web3
import json
import config
import time


from_adrs = "0x0e41E533061f8ec22F3040237b257e5234975843"
to_adrs = "0x138EB2CED1E7d03dff233Aa527723df7876Bee52"
from_private_key = '06f59167d0095fa0b586eef0244486dd1691f1d2b2999645a29f2d7cd8d00f67'
trans_amount = 0.005
_gas_limit = 21000
_gas_price = 10  #GWEI

bsc = "https://data-seed-prebsc-1-s1.binance.org:8545/"
web3 = Web3(Web3.HTTPProvider(bsc))
if web3.isConnected():
    print("Web3 connection is completed!  :)")
else:
    print("Web3 connection is failed!     :(")
    quit()



_nonce = web3.eth.getTransactionCount(from_adrs)
print("trans_no: ", _nonce)
print("from_address :", from_adrs)
print("to_address:", to_adrs)
print("trans_amount:", trans_amount)

my_balance = web3.fromWei(web3.eth.get_balance(from_adrs), 'ether')
print("Current balance of Sender : ",my_balance, "BNB")

my_balance = web3.fromWei(web3.eth.get_balance(to_adrs), 'ether')
print("Current balance of Reciever : ",my_balance, "BNB")

tx = {
    'nonce': _nonce,
    'to': to_adrs,
    'value': web3.toWei(trans_amount, 'ether'),
    'gas': _gas_limit,
    'gasPrice': web3.toWei(_gas_price, 'gwei')
}

signed_tx = web3.eth.account.signTransaction(tx, private_key = from_private_key)
tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
trans = web3.toHex(tx_hash)
print("Transx Hash : ",trans)

time.sleep(10)

my_balance = web3.fromWei(web3.eth.get_balance(from_adrs), 'ether')
print("Current balance of Sender : ",my_balance, "BNB")

my_balance = web3.fromWei(web3.eth.get_balance(to_adrs), 'ether')
print("Current balance of Reciever : ",my_balance, "BNB")

