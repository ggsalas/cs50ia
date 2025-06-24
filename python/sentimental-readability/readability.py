def main():
    text = getText()
    values = getValues(text)
    grade = getGrade(values)
    print(grade)


def getGrade(values):
    words = values["words"]
    letters = values["letters"]
    sentences = values["sentences"]

    L = letters * 100 / words
    S = sentences * 100 / words
    index = 0.0588 * L - 0.296 * S - 15.8

    if (index < 1):
        return "Before Grade 1"
    if (index > 16):
        return "Grade 16+"
    else:
        return f"Grade {round(index)}"


def getValues(text):
    wordsArray = text.split()
    words = len(wordsArray)
    letters = 0
    sentences = 0

    for n in [".", "!", "?"]:
        sentences += text.count(n)

    for char in "".join(wordsArray):
        if (char not in [".", "!", "?", ",", ":", "\"", "'"]):
            letters += 1
    return {
        "words": words,
        "letters": letters,
        "sentences": sentences
    }


def getText():
    text = input("Text: ")
    return text.strip()


main()
