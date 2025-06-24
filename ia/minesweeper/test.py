

def test():
    safes = set()
    safes.add((1, 0))

    return next(iter(safes), None)

print(test())


# safes = set()
# safes.add((1, 0))
# safes.add((1, 1))

