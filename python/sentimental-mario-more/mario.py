
def main():
    try:
        amount = int(input("Height "))
    except:
        main()
    else:
        if (amount > 0 and amount < 9):
            print_bl(amount)
        else:
            main()

def print_bl(rows):
    for j in range(rows):
        for i in range(rows):
            print(f"horiz: {j} - vert: {i}")

def print_blocks(rows):
    for i in range(rows):
        block = i + 1
        white_space = rows - block

        print(" " * white_space, end="")
        print("#" * block, end="  ")
        print("#" * block, end="")
        print("")


main()
