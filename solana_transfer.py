"""
Real Solana Transfer - Actually executes the transaction
This will perform a real SOL transfer on devnet
"""

import requests
import json
import base58
import base64
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.system_program import transfer, TransferParams
from solders.transaction import Transaction
from solders.message import Message
from solders.hash import Hash
import os
from dotenv import load_dotenv

load_dotenv()

def get_latest_blockhash():
    """Get the latest blockhash from Solana devnet"""
    response = requests.post(
        "https://api.devnet.solana.com",
        json={
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getLatestBlockhash",
            "params": [{"commitment": "finalized"}]
        }
    )
    result = response.json()
    return result["result"]["value"]["blockhash"]

def send_sol_transfer():
    """Execute actual SOL transfer"""
    
    sender_private_key = os.getenv('SOLANA_SENDER_PRIVATE_KEY')
    receiver_public_key = os.getenv('SOLANA_RECEIVER_PUBLIC_KEY')
    amount_sol = 0.001
    
    try:
        # Create keypairs
        sender = Keypair.from_base58_string(sender_private_key)
        receiver = Pubkey.from_string(receiver_public_key)
        
        print(f"Sender: {sender.pubkey()}")
        print(f"Receiver: {receiver}")
        
        # Convert SOL to lamports
        lamports = int(amount_sol * 1_000_000_000)
        print(f"Transferring {amount_sol} SOL ({lamports} lamports)")
        
        # Get latest blockhash
        blockhash_str = get_latest_blockhash()
        blockhash = Hash.from_string(blockhash_str)
        print(f"Using blockhash: {blockhash_str}")
        
        # Create transfer instruction
        transfer_ix = transfer(
            TransferParams(
                from_pubkey=sender.pubkey(),
                to_pubkey=receiver,
                lamports=lamports
            )
        )
        
        # Create message and transaction
        message = Message.new_with_blockhash([transfer_ix], sender.pubkey(), blockhash)
        transaction = Transaction.new_unsigned(message)
        
        # Sign the transaction
        transaction.sign([sender], blockhash)
        
        # Serialize transaction (use bytes conversion)
        serialized = bytes(transaction)
        encoded = base64.b64encode(serialized).decode('utf-8')
        
        # Send transaction
        print("Sending transaction...")
        response = requests.post(
            "https://api.devnet.solana.com",
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "sendTransaction",
                "params": [
                    encoded,
                    {
                        "skipPreflight": False,
                        "preflightCommitment": "processed",
                        "encoding": "base64",
                        "maxRetries": 3
                    }
                ]
            }
        )
        
        result = response.json()
        print(f"Response: {result}")
        
        if "result" in result:
            signature = result["result"]
            print(f"✅ Transaction sent successfully!")
            print(f"Transaction signature: {signature}")
            print(f"View on Solana Explorer: https://explorer.solana.com/tx/{signature}?cluster=devnet")
            return signature
        else:
            print(f"❌ Transaction failed: {result}")
            return None
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return None

def confirm_transaction(signature):
    """Wait for transaction confirmation"""
    if not signature:
        return False
        
    print("Waiting for confirmation...")
    import time
    
    for i in range(30):  # Wait up to 30 seconds
        response = requests.post(
            "https://api.devnet.solana.com",
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "getSignatureStatuses",
                "params": [[signature], {"searchTransactionHistory": True}]
            }
        )
        
        result = response.json()
        if "result" in result and result["result"]["value"][0]:
            status = result["result"]["value"][0]
            if status["confirmationStatus"] in ["confirmed", "finalized"]:
                print("✅ Transaction confirmed!")
                return True
            elif status.get("err"):
                print(f"❌ Transaction failed: {status['err']}")
                return False
        
        print(f"Waiting... ({i+1}/30)")
        time.sleep(1)
    
    print("⚠️ Timeout waiting for confirmation")
    return False

if __name__ == "__main__":
    print("=== Real Solana Transfer Execution ===")
    signature = send_sol_transfer()
    if signature:
        confirm_transaction(signature)
