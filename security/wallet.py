from typing import Dict, List, Optional
import logging
from eth_account import Account
from web3 import Web3
from eth_typing import Address
import json
import os
from dataclasses import dataclass
from decimal import Decimal
import asyncio
from web3.exceptions import TransactionNotFound
import time

@dataclass
class WalletConfig:
    chain_id: int
    rpc_url: str
    gas_limit: int = 250000
    gas_price_multiplier: Decimal = Decimal('1.1')

@dataclass
class TokenBalance:
    token_address: str
    symbol: str
    balance: Decimal
    decimals: int

class KQIWallet:
    """Secure wallet management for KQI trading agents"""
    
    def __init__(self, config: WalletConfig):
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.web3 = Web3(Web3.HTTPProvider(config.rpc_url))
        self._private_key = None
        self._address = None
        self.token_cache = {}  # Cache for token contract interfaces
        
    async def initialize(self, private_key: Optional[str] = None):
        """Initialize wallet with private key or generate new one"""
        if private_key:
            if not private_key.startswith('0x'):
                private_key = f'0x{private_key}'
            self._private_key = private_key
        else:
            acct = Account.create()
            self._private_key = acct.key.hex()
            
        account = Account.from_key(self._private_key)
        self._address = account.address
        self.logger.info(f"Wallet initialized: {self.get_address()}")
        
    def get_address(self) -> str:
        """Get wallet's public address"""
        if not self._address:
            raise ValueError("Wallet not initialized")
        return self._address
        
    async def get_native_balance(self) -> Decimal:
        """Get native token (ETH/MATIC/etc) balance"""
        balance = await self.web3.eth.get_balance(self.get_address())
        return Decimal(balance) / Decimal(10**18)
        
    async def get_token_balance(self, token_address: str) -> TokenBalance:
        """Get balance of specific ERC20 token"""
        if token_address not in self.token_cache:
            # Load standard ERC20 ABI
            with open('assets/erc20_abi.json') as f:
                token_abi = json.load(f)
            self.token_cache[token_address] = self.web3.eth.contract(
                address=token_address,
                abi=token_abi
            )
            
        token = self.token_cache[token_address]
        decimals = await token.functions.decimals().call()
        symbol = await token.functions.symbol().call()
        balance = await token.functions.balanceOf(self.get_address()).call()
        
        return TokenBalance(
            token_address=token_address,
            symbol=symbol,
            balance=Decimal(balance) / Decimal(10**decimals),
            decimals=decimals
        )
        
    async def send_transaction(
        self,
        to_address: str,
        value: int = 0,
        data: bytes = b'',
        gas_price: Optional[int] = None
    ) -> str:
        """Send transaction with automatic gas estimation"""
        if not self._private_key:
            raise ValueError("Wallet not initialized")
            
        nonce = await self.web3.eth.get_transaction_count(self.get_address())
        
        if gas_price is None:
            gas_price = int(await self.web3.eth.gas_price * self.config.gas_price_multiplier)
            
        tx = {
            'nonce': nonce,
            'gasPrice': gas_price,
            'gas': self.config.gas_limit,
            'to': to_address,
            'value': value,
            'data': data,
            'chainId': self.config.chain_id
        }
        
        # Estimate gas and update limit
        try:
            estimated_gas = await self.web3.eth.estimate_gas(tx)
            tx['gas'] = int(estimated_gas * 1.1)  # Add 10% buffer
        except Exception as e:
            self.logger.warning(f"Gas estimation failed: {e}. Using default gas limit.")
            
        # Sign and send transaction
        signed_tx = self.web3.eth.account.sign_transaction(tx, self._private_key)
        tx_hash = await self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        
        return tx_hash.hex()
        
    async def wait_for_transaction(
        self,
        tx_hash: str,
        timeout: int = 180,
        poll_interval: float = 0.5
    ) -> bool:
        """Wait for transaction confirmation"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                receipt = await self.web3.eth.get_transaction_receipt(tx_hash)
                if receipt:
                    if receipt['status'] == 1:
                        self.logger.info(f"Transaction {tx_hash} confirmed")
                        return True
                    else:
                        self.logger.error(f"Transaction {tx_hash} failed")
                        return False
            except TransactionNotFound:
                await asyncio.sleep(poll_interval)
                continue
                
        raise TimeoutError(f"Transaction {tx_hash} not confirmed after {timeout} seconds")
        
    async def approve_token(
        self,
        token_address: str,
        spender_address: str,
        amount: Optional[int] = None
    ) -> str:
        """Approve spender for token transfers"""
        token = self.token_cache.get(token_address)
        if not token:
            raise ValueError("Token not initialized")
            
        if amount is None:
            amount = 2**256 - 1  # Max uint256
            
        data = token.functions.approve(
            spender_address,
            amount
        ).build_transaction({'gas': 0, 'nonce': 0})['data']
        
        return await self.send_transaction(token_address, data=data)
        
    def export_encrypted_keystore(self, password: str, path: str):
        """Export encrypted keystore file"""
        if not self._private_key:
            raise ValueError("Wallet not initialized")
            
        keystore = Account.encrypt(self._private_key, password)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            json.dump(keystore, f)
            
    @classmethod
    def from_encrypted_keystore(
        cls,
        config: WalletConfig,
        keystore_path: str,
        password: str
    ) -> 'KQIWallet':
        """Create wallet instance from encrypted keystore"""
        with open(keystore_path) as f:
            keystore = json.load(f)
        private_key = Account.decrypt(keystore, password)
        
        wallet = cls(config)
        asyncio.run(wallet.initialize(private_key.hex()))
        return wallet

# Usage example:
async def main():
    config = WalletConfig(
        chain_id=1,  # Ethereum mainnet
        rpc_url="https://eth-mainnet.alchemyapi.io/v2/your-api-key"
    )
    
    wallet = KQIWallet(config)
    await wallet.initialize()  # Creates new wallet
    
    # Get balances
    eth_balance = await wallet.get_native_balance()
    print(f"ETH Balance: {eth_balance}")
    
    # USDC on Ethereum
    usdc_balance = await wallet.get_token_balance("0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48")
    print(f"USDC Balance: {usdc_balance.balance} {usdc_balance.symbol}")

if __name__ == "__main__":
    asyncio.run(main())
