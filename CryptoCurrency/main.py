import inspect
import os
import sys

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from ojcoin import OJcoin_Client
from RSA import fetch_key, generate_key


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


if __name__ == "__main__":

    clear_screen()
    new_guy = True
    if os.path.isfile("CryptoCurrency/private_key.pem"):
        print("Previously generated RSA key found!")
        secret_code = input("Enter the secret code: ")
        private_key = fetch_key(secret_code)
        if not private_key:
            print("Incorrect secret code!")
            sys.exit()
        else:
            print("Loggen in!")
            new_guy = False
    else:
        print("No previous wallets found!")
        print("Enter a secret code to generate a new RSA key.")
        secret_code = input("Enter secret code: ")
        private_key = generate_key(secret_code)
        print("Key generated successfully.")

    ojcoin = OJcoin_Client(private_key, private_key.public_key(), secret_code)
    if new_guy:
        ojcoin.send_coins(sender="Santa Claus", receiver=private_key.public_key().export_key().decode("utf-8"), amount=10)
        print("The Developer of this program has been wise enough to give you 10 OJCoins initially.")
        print("Spend wisely :)")

    input("Press enter to continue...")
    show_balance = False
    while True:
        clear_screen()

        if show_balance:
            print("Current Balance: " + str(ojcoin.get_balance()) + "\n")

        print("Options:")
        print("1. Send Coins")
        print("2. Mine Coins")
        print("3. Get Balance")
        print("4. Print public key")
        print("5. Toggle show Balance above (" + str(show_balance) + ")")
        print("6. Exit")
        choice = input("\nEnter your choice: ")
        print("\n")

        if choice == "1":
            last_block = ojcoin.blockchain.get_last_block()
            if not last_block:
                last_block = ojcoin.blockchain.add_block("This is just the Beginning")
            amount = float(input("Enter the amount: "))
            fee = float(input("Enter the fee: "))
            print("Save the receiver's public_key in CryptoCurrency/dest_pub.pem file")
            input("Press enter to continue...")
            receiver_pub_file = open("CryptoCurrency/dest_pub.pem", "r")
            receiver_pub = receiver_pub_file.read()
            receiver_pub_file.close()
            print("\n")
            if ojcoin.send_coins(ojcoin.public_key.export_key().decode("utf-8"), receiver_pub, amount, fee):
                print("Transaction added to the memPool!")
                print("Consider it done after confirmations from the miners.")
            else:
                print("Transaction failed!")

        elif choice == "2":
            print("Mining Coins...\n")
            mined = ojcoin.add_block()
            if mined:
                print("Mined a new block:\n" + str(mined))
            else:
                print("Mining failed!")
                print("Not enough transactions in the memPool yet!")

        elif choice == "3":
            print("Your current balance is: " + str(ojcoin.get_balance()))

        elif choice == "4":
            print(ojcoin.public_key.export_key().decode("utf-8"))

        elif choice == "5":
            show_balance = not show_balance
            print("Toggled show Blockchain above to: ", show_balance)

        elif choice == "6":
            print("Exiting...")
            break

        else:
            print("Invalid choice")

        print("\n")
        input("Press Enter to continue...")
