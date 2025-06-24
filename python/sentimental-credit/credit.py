def main():
    number = getNumber()
    isValid = validateCard(number)

    if isValid:
        getBrand(number)
    else:
        print("INVALID")


def getBrand(number):
    length = len(number)
    firstDigit = int(number[0])
    first2digits = int(number[0] + number[1])

    if (length == 15 and first2digits in [34, 37]):
        print("AMEX")
    elif (length == 16 and first2digits in range(51, 56)):
        print("MASTERCARD")
    elif (length in [16, 13] and firstDigit == 4):
        print("VISA")
    else:
        print("INVALID")


def getNumber():
    try:
        # Get a valid number, then transform as string
        number = str(int(input("Number: ")))
    except:
        getNumber()
    else:
        digitsArray = []
        for digit in number:
            digitsArray.append(digit)
        return digitsArray


def validateCard(num: str):
    firstDigits = ""
    secondDigits = ""

    # Populate firstDigits
    for n in range(len(num) - 2, -1, -2):
        double = int(num[n]) * 2
        firstDigits += str(double)

    # Populate secondDigits
    for n in range(len(num) - 1, -1, -2):
        secondDigits += str(num[n])

    total = digitsSum(firstDigits) + digitsSum(secondDigits)

    # Last digit should be "0"
    if str(total)[-1] == "0":
        return True
    else:
        return False


def digitsSum(array: str):
    result = 0
    for val in array:
        result += int(val)

    return result


main()
