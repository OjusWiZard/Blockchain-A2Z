from ast import literal_eval
from heapq import *

from Crypto.PublicKey.RSA import RsaKey

from CryptoCurrency.RSA import sign, verify


class Transaction:
    def __init__(self, sender: str, receiver: str, amount: int, fee=0.0):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.fee = fee

    def sign(self, private_key: RsaKey):
        transaction_string = self.sender + str(self.amount) + self.receiver + str(self.fee)
        self.signature = sign(transaction_string, private_key)
        return self.signature

    def verify(self):
        transaction_string = self.sender + str(self.amount) + self.receiver + str(self.fee)
        return verify(transaction_string, self.signature, self.sender)

    def to_list(self) -> list:
        return [self.amount, self.fee, self.sender, self.receiver, self.signature]
    
    def populate_from_list(self, transaction_as_list: list):
        self.amount = transaction_as_list[0]
        self.fee = transaction_as_list[1]
        self.sender = transaction_as_list[2]
        self.receiver = transaction_as_list[3]
        self.signature = transaction_as_list[4]
    
    def populate_from_str(self, string: str):
        self.populate_from_list(literal_eval(string))

    def __str__(self) -> str:
        return str(self.to_list())

    def __lt__(self, other: "Transaction"):
        return self.fee > other.fee


class MemPool:
    def __init__(self):
        self.transactions = []

    def get_transactions(self) -> list:
        return self.transactions
    
    def set_trasactions(self, transactions: list):
        self.transactions = transactions

    def add_transaction(self, transaction: Transaction, private_key: RsaKey) -> None:
        transaction.sign(private_key)
        heappush(self.transactions, transaction)

    def get_top_transaction(self) -> Transaction:
        return heappop(self.transactions)

    def remove_transactions(self, transactions: list) -> None:
        for transaction in transactions:
            self.transactions.remove(transaction)
        heapify(self.transactions)
    
    def populate_from_list(self, transactions: list):
        self.transactions = transactions
        heapify(self.transactions)

    def __str__(self):
        return str(self.transactions)