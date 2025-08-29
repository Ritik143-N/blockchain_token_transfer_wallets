# Blockchain Fund Transfer Assignment

This project demonstrates how to transfer funds between wallets on both Solana and Ethereum testnets using Python.

## Prerequisites

1. **Python 3.7+** installed
2. **MetaMask** browser extension (for Ethereum)
3. **Phantom** wallet extension (for Solana)

## Setup Instructions

### 1. Install Required Python Packages

```bash
# Install dependencies
pip install solana web3 base58
```

### 2. Wallet Setup

#### For Solana (Phantom):
1. Install Phantom wallet extension
2. Create two accounts in Phantom
3. Switch to Devnet (testnet) in Phantom settings
4. Get devnet SOL from: https://faucet.solana.com/
5. Export private keys: Settings > Export Private Key

#### For Ethereum (MetaMask):
1. Install MetaMask browser extension
2. Create two accounts in MetaMask
3. Switch to Sepolia testnet
4. Get Sepolia ETH from: https://faucets.chain.link/sepolia
5. Export private keys: Account Details > Export Private Key

### 3. Configuration

#### Solana Transfer (`solana_transfer.py`):
- Replace `SENDER_PRIVATE_KEY_BASE58` with your sender's private key
- Replace `RECEIVER_PUBLIC_KEY` with receiver's public key
- Adjust `AMOUNT_SOL` as needed

#### Ethereum Transfer (`ethereum_transfer.py`):
- Replace `SENDER_PRIVATE_KEY` with your sender's private key (with 0x prefix)
- Replace `SENDER_ADDRESS` with sender's wallet address
- Replace `RECEIVER_ADDRESS` with receiver's wallet address
- Replace `SEPOLIA_RPC_URL` with your Infura/Alchemy URL or use public RPC
- Adjust `AMOUNT_ETH` as needed

## Usage

### Run Solana Transfer:
```bash
python solana_transfer.py
```

### Run Ethereum Transfer:
```bash
python ethereum_transfer.py
```

## Important Notes

- **Never share your private keys** in production
- Use only testnet/devnet for testing
- Keep your private keys secure
- Test with small amounts first
- Make sure wallets have sufficient testnet funds

## Testnet Faucets

### Solana Devnet:
- https://faucet.solana.com/

### Ethereum Sepolia:
- https://faucets.chain.link/sepolia
- https://sepoliafaucet.com/

## Block Explorers

### Solana:
- https://explorer.solana.com/?cluster=devnet

### Ethereum:
- https://sepolia.etherscan.io/

## Troubleshooting

1. **Connection issues**: Check your internet connection and RPC URLs
2. **Insufficient funds**: Make sure wallets have enough testnet tokens
3. **Invalid keys**: Verify private keys are correctly formatted
4. **Gas fees**: Ensure sufficient balance for transaction fees on Ethereum

## Security Warnings

- ⚠️ Never use these scripts with mainnet private keys
- ⚠️ Always use testnets for learning and development
- ⚠️ Store private keys securely (consider using environment variables)
