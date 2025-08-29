"""
Wallet Balance Checker
Check balances of your generated Solana and Ethereum wallets
"""

from web3 import Web3
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solana.rpc.api import Client
from solana.rpc.commitment import Confirmed
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_ethereum_balances():
    """Check Ethereum wallet balances on Sepolia"""
    print("=== Ethereum Wallet Balances (Sepolia) ===")
    
    # Get addresses from .env
    sender_address = os.getenv('ETHEREUM_SENDER_ADDRESS')
    receiver_address = os.getenv('ETHEREUM_RECEIVER_ADDRESS')
    rpc_url = "https://eth-sepolia.public.blastapi.io"  # More reliable public RPC
    
    try:
        w3 = Web3(Web3.HTTPProvider(rpc_url))
        if not w3.is_connected():
            print("❌ Failed to connect to Sepolia network")
            return
        
        print(f"✅ Connected to Sepolia testnet")
        
        # Check sender balance
        if sender_address:
            balance_wei = w3.eth.get_balance(sender_address)
            balance_eth = w3.from_wei(balance_wei, 'ether')
            print(f"Sender ({sender_address}): {balance_eth} ETH")
        
        # Check receiver balance  
        if receiver_address:
            balance_wei = w3.eth.get_balance(receiver_address)
            balance_eth = w3.from_wei(balance_wei, 'ether')
            print(f"Receiver ({receiver_address}): {balance_eth} ETH")
            
    except Exception as e:
        print(f"❌ Error checking Ethereum balances: {e}")

def check_solana_balances():
    """Check Solana wallet balances on devnet"""
    print("\n=== Solana Wallet Balances (Devnet) ===")
    
    # Get addresses from .env
    sender_pubkey = os.getenv('SOLANA_SENDER_PUBLIC_KEY')
    receiver_pubkey = os.getenv('SOLANA_RECEIVER_PUBLIC_KEY')
    
    try:
        client = Client("https://api.devnet.solana.com")
        print(f"✅ Connected to Solana devnet")
        
        # Check sender balance
        if sender_pubkey:
            pubkey = Pubkey.from_string(sender_pubkey)
            balance = client.get_balance(pubkey, commitment=Confirmed)
            balance_sol = balance.value / 1_000_000_000
            print(f"Sender ({sender_pubkey}): {balance_sol} SOL")
        
        # Check receiver balance
        if receiver_pubkey:
            pubkey = Pubkey.from_string(receiver_pubkey)
            balance = client.get_balance(pubkey, commitment=Confirmed)
            balance_sol = balance.value / 1_000_000_000
            print(f"Receiver ({receiver_pubkey}): {balance_sol} SOL")
            
    except Exception as e:
        print(f"❌ Error checking Solana balances: {e}")

def main():
    print("🔍 Checking Your Wallet Balances...")
    print("=" * 50)
    
    check_ethereum_balances()
    check_solana_balances()
    
    print("\n" + "=" * 50)
    print("💡 Funding Instructions:")
    print("Ethereum: https://faucets.chain.link/sepolia")  
    print("Solana: https://faucet.solana.com/")

if __name__ == "__main__":
    main()
