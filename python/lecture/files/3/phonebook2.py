# Implements a phone book as a list of dictionaries

people = [
    {"name": "Yuliia", "number": "+1-617-495-1000"}, # dictionary: { key: value, key: value } // 2 keys, 2 values here
    {"name": "David", "number": "+1-617-495-1000"},
    {"name": "John", "number": "+1-949-468-2750"},
]

# Search for name
name = input("Name: ")
for person in people:
    if person["name"] == name:
        number = person["number"]
        print(f"Found {number}")
        break
else:
    print("Not found")
