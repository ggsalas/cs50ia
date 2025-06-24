words = set() # 

def chech(word): 
    return word.lower() in words

def load(dictionary):
    with open(dictionary) as file:
        words.update(file.read().splitlines())
    return True

def size(): 
    return len(words)

def unload():
    return True



