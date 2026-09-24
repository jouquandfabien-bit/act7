# hashgestion.py

import hashlib


class HashGestion:
    def __init__(self):
        print("Constructeur par défaut du Hash")

    def __del__(self):
        print("Destructeur par défaut du Hash")

    def calculate_sha256(self, input_string: str) -> str:
        sha256 = hashlib.sha256()
        sha256.update(input_string.encode('utf-8'))
        return sha256.hexdigest().upper()

    def calculate_file_sha256(self, filename: str) -> str:
        sha256 = hashlib.sha256()
        try:
            with open(filename, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b''):
                    sha256.update(chunk)
            return sha256.hexdigest().upper()
        except FileNotFoundError:
            print("Impossible d'ouvrir le fichier.")
            return 0

if __name__=="__main__":
    hasher = HashGestion()

    #Hash du fichier texte README.md  
    hash_txt = hasher.calculate_file_sha256("README.md")
    print(f"Hash de README.md :: {hash_txt}")

    hash_bin = hasher.calculate_file_sha256("../cryptoPython.zip")
    print(f"Hash du fichier binaire: {hash_bin}")
