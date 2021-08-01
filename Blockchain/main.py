import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from blockchain import Blockchain


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


if __name__ == "__main__":

    blockchain = Blockchain(blocks_filename="Blockchain/blockchain.dat")
    show_everytime = False
    while True:
        clear_screen()

        if show_everytime:
            print("Current Blockchain: \n")
            print("Index", end="\t")
            print("Timestamp", end="\t\t")
            print("Data".ljust(16), end="\t")
            print("Previous Hash".ljust(16), end="\t")
            print("Nonce".ljust(16), end="\t")
            print("Hash".ljust(16))
            print(blockchain)
            print("\n")

        print("Options:")
        print("1. Add a new Block")
        print("2. Print the current Blockchain")
        print("3. Validate the Blockchain")
        print("4. Toggle show Blockchain above (" + str(show_everytime) + ")")
        print("5. Exit")
        choice = input("\nEnter your choice: ")
        print("\n")

        if choice == "1":
            last_block = blockchain.get_last_block()
            if not last_block:
                last_block = blockchain.add_block("This is just the Beginning")
            if last_block.is_valid(blockchain.difficulty):
                data = input("Enter the data: ")
                print("\n")
                added_block = blockchain.add_block(data)
                print("Block Added:\n")
                print(added_block)
            else:
                print("Invalid last block!!!\n")

        elif choice == "2":
            print("Printing the current Blockchain...\n")
            print(blockchain)

        elif choice == "3":
            print("Validating the Blockchain...")
            valid = blockchain.is_valid()
            if valid:
                print("The Blockchain is valid :D")
            else:
                print("The Blockchain is invalid :'(")

        elif choice == "4":
            show_everytime = not show_everytime
            print("Toggled show Blockchain above to: ", show_everytime)

        elif choice == "5":
            print("Exiting...")
            break

        else:
            print("Invalid choice")

        print("\n")
        input("Press Enter to continue...")
