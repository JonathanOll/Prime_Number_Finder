from time import time
from math import sqrt
from os import listdir, mkdir, remove
from os.path import exists
from re import match

PATH="prime_numbers/"  # Chemin où enregistrer/charger les sauvegardes
SAVE_DELAY = 10  # Délai entre chaque sauvegarde (en sec)
DELETE_OLD_SAVE = True  # Faut-il supprimer les anciennes sauvegardes après en avoir enregistré une nouvelle

def save(prime_numbers, path):
    name = path+"prime_numbers-" + str(int(time())) + ".sav"
    if not exists(path): mkdir(path)
    file = open(name, 'w+')
    file.write(",".join(str(i) for i in prime_numbers))


def delete_old(path):
    saves = []
    for a in listdir(path):
        if match(r"prime\_numbers\-[0-9]+", a):
            saves.append(int(a.replace("prime_numbers-", "").replace(".sav", "")))
    for a in saves:
        if a < max(saves):
            remove(path+"prime_numbers-" + str(a) + ".sav")


def load_recent(path):
    saves = []
    if not exists(path): return []
    for a in listdir(path):
        if match(r"prime\_numbers\-[0-9]+", a):
            saves.append(int(a.replace("prime_numbers-", "").replace(".sav", "")))
    try:
        print("loaded",path+"prime_numbers-" + str(max(saves)) + ".sav")
        return load(path+"prime_numbers-" + str(max(saves)) + ".sav")
    except:
        pass


def load(file_path):
    res = []
    try:
        file = open(file_path, "r")
        content = file.read()
        for number in content.split(","):
            res.append(int(number))
    except:
        pass
    finally:
        return res


def is_prime(number, prime_numbers):
    for current in prime_numbers:
        if number % current == 0:
            return False
        if current >= sqrt(number):
            return True
    return True


def run(load_path=None):
    prime_numbers = [2]
    if load_path:
        prime_numbers = load_recent(load_path)
    if len(prime_numbers) > 1:
        current = prime_numbers[-1] + 2
    else:
        current = 3
    last_save = time()
    while True:
        if time() - last_save > SAVE_DELAY:
            save(prime_numbers, PATH)
            if DELETE_OLD_SAVE:
                delete_old(PATH)
            last_save = time()
        if is_prime(current, prime_numbers):
            print("Found", len(prime_numbers), "prime numbers  ", end="\r")
            prime_numbers.append(current)
        current += 2


if __name__ == "__main__":
    run("prime_numbers/")