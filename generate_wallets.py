"""
Wallet Generator for Solana and Ethereum
This script generates new wallet addresses and private keys for both blockchains

Usage: python generate_wallets.py

IMPORTANT: Save the generated keys securely and never share them!
"""

from solders.keypair import Keypair
from web3 import Web3
import secrets
import base58
import json

def generate_solana_wallet():
    """Generate a new Solana wallet"""
    print("=== Generating Solana Wallet ===")
    
    # Generate new keypair
    keypair = Keypair()
    
    # Get public key (address)
    public_key = str(keypair.pubkey())
    
    # Get private key in different formats
    private_key_bytes = bytes(keypair)
    private_key_base58 = base58.b58encode(private_key_bytes).decode('ascii')
    private_key_list = list(private_key_bytes)
    
    print(f"Public Key (Address): {public_key}")
    print(f"Private Key (Base58): {private_key_base58}")
    print(f"Private Key (Bytes List): {private_key_list}")
    print(f"Fund this wallet at: https://faucet.solana.com/")
    print(f"Enter this address: {public_key}")
    print()
    
    return {
        'public_key': public_key,
        'private_key_base58': private_key_base58,
        'private_key_bytes': private_key_list
    }

def generate_ethereum_wallet():
    """Generate a new Ethereum wallet"""
    print("=== Generating Ethereum Wallet ===")
    
    # Generate random private key
    private_key_bytes = secrets.token_bytes(32)
    private_key_hex = private_key_bytes.hex()
    private_key_with_prefix = f"0x{private_key_hex}"
    
    # Create account from private key
    account = Web3().eth.account.from_key(private_key_bytes)
    address = account.address
    
    print(f"Address: {address}")
    print(f"Private Key: {private_key_with_prefix}")
    print(f"Fund this wallet at: https://faucets.chain.link/sepolia")
    print(f"Enter this address: {address}")
    print()
    
    return {
        'address': address,
        'private_key': private_key_with_prefix
    }

def save_wallets_to_env(solana_wallets, ethereum_wallets):
    """Save wallet information to .env file"""
    
    env_content = f"""# Generated Wallet Information
# NEVER share these private keys or commit this file to version control!

# Solana Wallet 1 (Sender)
SOLANA_SENDER_PRIVATE_KEY={solana_wallets[0]['private_key_base58']}
SOLANA_SENDER_PUBLIC_KEY={solana_wallets[0]['public_key']}

# Solana Wallet 2 (Receiver)  
SOLANA_RECEIVER_PUBLIC_KEY={solana_wallets[1]['public_key']}
SOLANA_RECEIVER_PRIVATE_KEY={solana_wallets[1]['private_key_base58']}

# Ethereum Wallet 1 (Sender)
ETHEREUM_SENDER_PRIVATE_KEY={ethereum_wallets[0]['private_key']}
ETHEREUM_SENDER_ADDRESS={ethereum_wallets[0]['address']}

# Ethereum Wallet 2 (Receiver)
ETHEREUM_RECEIVER_ADDRESS={ethereum_wallets[1]['address']}
ETHEREUM_RECEIVER_PRIVATE_KEY={ethereum_wallets[1]['private_key']}

# Ethereum RPC URL (you can use public RPC or get your own from Infura/Alchemy)
ETHEREUM_RPC_URL=https://rpc.sepolia.org
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Wallet information saved to .env file")

def save_wallets_to_json(solana_wallets, ethereum_wallets):
    """Save wallet information to JSON file for backup"""
    
    wallet_data = {
        'solana': {
            'wallet_1': solana_wallets[0],
            'wallet_2': solana_wallets[1]
        },
        'ethereum': {
            'wallet_1': ethereum_wallets[0],
            'wallet_2': ethereum_wallets[1]
        }
    }
    
    with open('wallets_backup.json', 'w') as f:
        json.dump(wallet_data, f, indent=2)
    
    print("✅ Wallet backup saved to wallets_backup.json")

def main():
    print("🔑 Blockchain Wallet Generator")
    print("=" * 50)
    
    # Generate Solana wallets
    print("Generating 2 Solana wallets...\n")
    solana_wallet_1 = generate_solana_wallet()
    solana_wallet_2 = generate_solana_wallet()
    
    # Generate Ethereum wallets
    print("Generating 2 Ethereum wallets...\n")
    ethereum_wallet_1 = generate_ethereum_wallet()
    ethereum_wallet_2 = generate_ethereum_wallet()
    
    # Save to files
    solana_wallets = [solana_wallet_1, solana_wallet_2]
    ethereum_wallets = [ethereum_wallet_1, ethereum_wallet_2]
    
    save_wallets_to_env(solana_wallets, ethereum_wallets)
    save_wallets_to_json(solana_wallets, ethereum_wallets)
    
    print("\n" + "=" * 50)
    print("🎉 WALLETS GENERATED SUCCESSFULLY!")
    print("=" * 50)
    
    print("\n📋 NEXT STEPS:")
    print("1. Fund your Solana wallets:")
    print(f"   • Go to: https://faucet.solana.com/")
    print(f"   • Request devnet SOL for: {solana_wallet_1['public_key']}")
    print(f"   • Request devnet SOL for: {solana_wallet_2['public_key']}")
    
    print("\n2. Fund your Ethereum wallets:")
    print(f"   • Go to: https://faucets.chain.link/sepolia")
    print(f"   • Request Sepolia ETH for: {ethereum_wallet_1['address']}")
    print(f"   • Request Sepolia ETH for: {ethereum_wallet_2['address']}")
    
    print("\n3. Run the transfer scripts:")
    print("   • python solana_transfer_secure.py")
    print("   • python ethereum_transfer_secure.py")
    
    print("\n⚠️  SECURITY WARNINGS:")
    print("• NEVER share your private keys")
    print("• NEVER use these keys on mainnet")
    print("• Keep wallets_backup.json secure")
    print("• Add .env to .gitignore if using version control")

if __name__ == "__main__":
    main()
