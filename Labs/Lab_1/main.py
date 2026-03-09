import hashlib

def hash_string(input: str) -> str:
    sha256 = hashlib.sha256()
    sha256.update(input.encode('utf-8'))
    return sha256.hexdigest()


def save_in_file(filename: str, hashes: list[str]): 
    with open(filename, "w") as f:
        for h in hashes:
            f.write(h + "\n")


def read_from_file(filename:str) -> list[str]:
    with open(filename, "r") as f:
        return [line.strip() for line in f]

if __name__ == "__main__":

    mylist = ["password123", "123456", "19x*44sA!_"]
    hashes = [hash_string(i) for i in mylist]
    save_in_file("hashes.txt", hashes)
    #print(read_from_file("hashes.txt"))
    pwds = read_from_file("hashes.txt")
    for pwd in pwds:
        if hash_string("141adsa") == pwd:
            print("i am hacker :)")
