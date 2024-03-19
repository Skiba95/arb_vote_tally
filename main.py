from web3 import Web3
from config import *
import random, time
from loguru import logger

w3 = Web3(Web3.HTTPProvider(rpc))

def read_private_keys(file_path):
    with open(file_path, 'r') as file:
        private_keys = [line.strip() for line in file.readlines()]
    return private_keys

private_keys_file = 'wallets.txt'
private_keys = read_private_keys(private_keys_file)

abi = [
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "proposalId",
                "type": "uint256"
            },
            {
                "internalType": "uint8",
                "name": "support",
                "type": "uint8"
            }
        ],
        "name": "castVote",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

contract = w3.eth.contract(address=Web3.to_checksum_address(contract_address), abi=abi)

def tx_confirmation(w3, tx_hash, logger):
    logger.info(f"Waiting for tx confirm")
    time.sleep(10)

    receipt = None
    while receipt is None:
        try:
            receipt = w3.eth.get_transaction_receipt(tx_hash)
        except Exception as e:
            print(e)
            time.sleep(1)

    if receipt['status'] == 1:
        logger.success(f"https://arbiscan.io/tx/{receipt.transactionHash.hex()}")
    else:
        logger.error(f"https://arbiscan.io/tx/{receipt.transactionHash.hex()}")


def get_random_support():
    return random.choice([1, 2, 0])  # 1 для "За", 2 для "Воздержаться", 0 для "Против"


def vote(proposal_id, support, private_key):
    if random_enabled:
        support = get_random_support()
       
    account = w3.eth.account.from_key(private_key)
    caller = account.address

    logger.info(f" Vote on {caller}")
    
    transaction = contract.functions.castVote(proposal_id, support).build_transaction({
        'gasPrice': w3.eth.gas_price,  
        'nonce': w3.eth.get_transaction_count(caller),
    })

    transaction["gas"] = w3.eth.estimate_gas(transaction)
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return tx_receipt

if random_wallets:
    random.shuffle(private_keys)

for private_key in private_keys:
    try:
        receipt = vote(proposal_id, support, private_key)
        tx_confirmation(w3, receipt.transactionHash, logger)
    except Exception as e:
        logger.error(f"Error occurred while processing transaction: {e}")
        
    x = random.randint(sleep_wallet_from, sleep_wallet_to)
    logger.info(f"Slepping before next wallet {x} seconds")
    time.sleep(x) 
