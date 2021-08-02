from ast import literal_eval
from csv import reader
from itertools import combinations

from Crypto.PublicKey.RSA import RsaKey
from memPool import MemPool, Transaction
from RSA import *

from Blockchain.block import Block
from Blockchain.blockchain import Blockchain


class OJcoin_Client:
    def __init__(self, private_key: RsaKey, public_key: RsaKey, secret_code: str):
        self.mempool = MemPool()
        self.blockchain = Blockchain(blocks_filename="CryptoCurrency/ojcoin.dat")
        self.transactions_per_block = 1
        private_key = private_key.export_key(passphrase=secret_code).decode("utf-8")
        public_key = public_key.export_key().decode("utf-8")
        self.private_key = RSA.import_key(private_key, passphrase=secret_code)
        self.public_key = RSA.import_key(public_key)


    def add_block(self) -> Block:
        added = None
        chosen_transactions = combinations(self.mempool.transactions, self.transactions_per_block)
        for transaction_set in chosen_transactions:
            for transaction in transaction_set:
                if transaction.sender != "Santa Claus":
                    if not transaction.verify():
                        print("Removing invalid transaction: " + str(transaction))
                        self.mempool.remove_transactions([transaction])
                        continue
            transactions_list = [transaction.to_list() for transaction in transaction_set]
            added = self.blockchain.add_block(transactions_list)
            if added:
                self.mempool.remove_transactions(transaction_set)
                return added
        return added

    def send_coins(self, sender:str, receiver:str, amount:float, fee=0.0) -> bool:
        if not sender == "Santa Claus":
            if self.get_balance() < amount + fee:
                print("Not enough money")
                return False
        transaction = Transaction(sender, receiver, amount, fee)
        self.mempool.add_transaction(transaction, self.private_key)
        if len(self.mempool.transactions) >= self.transactions_per_block:
            self.add_block()
        return True
    
    def get_balance(self) -> float:
        blocks_reader = reader(open(self.blockchain.blocks_filename, "r"), delimiter="|")
        balance = 0.0
        
        for block_as_list in blocks_reader:
            block = Block(0, "", "0").populate_from_list(block_as_list)
            if block.index != 1:
                transactions_as_list = literal_eval(block.data)
                for transaction_as_list in transactions_as_list:
                    transaction = Transaction("", "", 0, 0)
                    transaction.populate_from_list(transaction_as_list)
                    if transaction.receiver == self.public_key.export_key().decode("utf-8"):
                        balance += transaction.amount

        blocks_reader = reader(open(self.blockchain.blocks_filename, "r"), delimiter="|")
        for block_as_list in blocks_reader:
            block = Block(0, "", "0").populate_from_list(block_as_list)
            if block.index != 1:
                transactions_as_list = literal_eval(block.data)
                for transaction_as_list in transactions_as_list:
                    transaction = Transaction("", "", 0, 0)
                    transaction.populate_from_list(transaction_as_list)
                    if transaction.sender == self.public_key.export_key().decode("utf-8"):
                        balance -= transaction.amount + transaction.fee
        
        return balance
