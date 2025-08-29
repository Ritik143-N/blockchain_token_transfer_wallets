"""
Enhanced Ethereum Fund Transfer Script with Environment Variables
This script transfers ETH from one wallet to another on Sepolia testnet

Usage:
1. Copy .env.example to .env
2. Fill in your actual wallet keys and RPC URL in .env file
3. Run: python ethereum_transfer_secure.py
"""

from web3 import Web3
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration from environment variables
SENDER_PRIVATE_KEY = os.getenv('ETHEREUM_SENDER_PRIVATE_KEY')
SENDER_ADDRESS = os.getenv('ETHEREUM_SENDER_ADDRESS')
RECEIVER_ADDRESS = os.getenv('ETHEREUM_RECEIVER_ADDRESS')
RPC_URL = "https://eth-sepolia.public.blastapi.io"  # Reliable public RPC
AMOUNT_ETH = 0.001  # Amount to transfer in ETH

def transfer_eth():
    """Transfer ETH from sender to receiver on Sepolia testnet"""
    
    if not all([SENDER_PRIVATE_KEY, SENDER_ADDRESS, RECEIVER_ADDRESS]):
        print("Error: Please set ETHEREUM_SENDER_PRIVATE_KEY, ETHEREUM_SENDER_ADDRESS, and ETHEREUM_RECEIVER_ADDRESS in .env file")
        return
    
    try:
        # Connect to Sepolia testnet
        w3 = Web3(Web3.HTTPProvider(RPC_URL))
        
        if not w3.is_connected():
            print("Failed to connect to Sepolia network")
            return
            
        print("Connected to Sepolia testnet")
        
        # Check sender balance
        balance_wei = w3.eth.get_balance(SENDER_ADDRESS)
        balance_eth = float(w3.from_wei(balance_wei, 'ether'))
        print(f"Sender balance: {balance_eth} ETH")
        
        if balance_eth < AMOUNT_ETH:
            print(f"Insufficient balance! Need at least {AMOUNT_ETH} ETH")
            return
        
        # Get current gas price and estimate gas
        gas_price = w3.eth.gas_price
        gas_limit = 21000  # Standard gas limit for ETH transfer
        
        # Calculate transaction fee
        tx_fee = float(w3.from_wei(gas_price * gas_limit, 'ether'))
        print(f"Estimated transaction fee: {tx_fee} ETH")
        
        if balance_eth < (AMOUNT_ETH + tx_fee):
            print(f"Insufficient balance for transaction + gas fee!")
            return
        
        # Get nonce (transaction count)
        nonce = w3.eth.get_transaction_count(SENDER_ADDRESS)
        
        # Build transaction
        transaction = {
            'nonce': nonce,
            'to': RECEIVER_ADDRESS,
            'value': w3.to_wei(AMOUNT_ETH, 'ether'),
            'gas': gas_limit,
            'gasPrice': gas_price,
            'chainId': 11155111  # Sepolia chain ID
        }
        
        print(f"Transferring {AMOUNT_ETH} ETH to {RECEIVER_ADDRESS}")
        
        # Sign transaction
        signed_txn = w3.eth.account.sign_transaction(transaction, SENDER_PRIVATE_KEY)
        
        # Send transaction using raw_transaction instead of rawTransaction
        tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
        tx_hash_hex = w3.to_hex(tx_hash)
        
        print(f"Transaction sent!")
        print(f"Transaction hash: {tx_hash_hex}")
        print(f"View on Etherscan: https://sepolia.etherscan.io/tx/{tx_hash_hex}")
        
        # Wait for confirmation (optional)
        print("Waiting for confirmation...")
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
        
        if receipt.status == 1:
            print("Transaction confirmed successfully!")
        else:
            print("Transaction failed!")
            
    except Exception as e:
        print(f"Error: {e}")

def check_wallet_balance(address):
    """Check balance of a wallet"""
    try:
        w3 = Web3(Web3.HTTPProvider(RPC_URL))
        if not w3.is_connected():
            print("Failed to connect to network")
            return
            
        balance_wei = w3.eth.get_balance(address)
        balance_eth = w3.from_wei(balance_wei, 'ether')
        print(f"Balance for {address}: {balance_eth} ETH")
        return balance_eth
    except Exception as e:
        print(f"Error checking balance: {e}")
        return None

if __name__ == "__main__":
    print("=== Ethereum Fund Transfer (Secure Version) ===")
    transfer_eth()
