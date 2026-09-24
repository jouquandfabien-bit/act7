import base64
from aesgestion import AesGestion
from rsagestion import RsaGestion


def main():
    # ----------------------------------------------------
    # 0. PREPARATION : Génération du jeu de clés RSA
    # ----------------------------------------------------
    print("--- GENERATION DES CLES RSA DU DESTINATAIRE ---")
    rsa_destinataire = RsaGestion()
    # On génère les fichiers de clés public.pem et private.pem
    rsa_destinataire.generation_clef("public.pem", "private.pem", 2048)
    print("Clés RSA générées avec succès.\n")

    # ----------------------------------------------------
    # 1. EMETTEUR (Chiffrement)
    # ----------------------------------------------------
    print("--- ROLE DE L'EMETTEUR ---")

    # A. L'émetteur génère une clé AES de session aléatoire
    aes_emetteur = AesGestion()
    aes_emetteur.generate_aes_key()

    # B. L'émetteur chiffre le message avec la clé AES
    message_original = (
        "Message très secret transmis via le chiffrement hybride !"
    )
    message_chiffre_aes = aes_emetteur.encrypt_string_to_base64(
        message_original
    )
    print(f"1. Message chiffré avec AES : {message_chiffre_aes}")

    # C. L'émetteur charge la clé PUBLIQUE RSA du destinataire
    rsa_emetteur = RsaGestion()
    rsa_emetteur.chargement_clef_publique("public.pem")

    # D. L'émetteur chiffre la clé AES avec la clé publique RSA
    cle_aes_b64 = base64.b64encode(aes_emetteur.aes_key).decode('utf-8')
    cle_aes_chiffree_rsa = rsa_emetteur.chiffrement_rsa(cle_aes_b64)
    print(
        f"2. Clé AES chiffrée avec la clé publique RSA : {cle_aes_chiffree_rsa}\n"
    )

    # ----------------------------------------------------
    # 2. DESTINATAIRE (Déchiffrement)
    # ----------------------------------------------------
    print("--- ROLE DU DESTINATAIRE ---")

    # A. Le destinataire charge sa clé PRIVÉE RSA
    # (rsa_destinataire a déjà la clé privée chargée)

    # B. Le destinataire déchiffre la clé AES grâce à sa clé privée RSA
    cle_aes_retrouvee_b64 = rsa_destinataire.dechiffrement_rsa(
        cle_aes_chiffree_rsa
    )
    cle_aes_retrouvee_bytes = base64.b64decode(cle_aes_retrouvee_b64)

    # C. Le destinataire déchiffre le message avec la clé AES retrouvée
    aes_destinataire = AesGestion()
    aes_destinataire.aes_key = cle_aes_retrouvee_bytes
    message_dechiffre = aes_destinataire.decrypt_string_from_base64(
        message_chiffre_aes
    )

    print(f"3. Message déchiffré reçu : {message_dechiffre}")


if __name__ == "__main__":
    main()
