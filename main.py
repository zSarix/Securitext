from string import ascii_letters, ascii_lowercase, digits
from random import choice
from json import dumps, loads

ascii_printable: str = ascii_letters  # variable qui stocke [a-zA-Z]
alphabet_length = len(ascii_lowercase)

def ask_info():
    """
    Fonction pour demander les informations à l'utilisateur.

    Returns:
        Tuple[str, str, str, int]: Les choix de l'utilisateur pour la méthode, le fichier et le décalage.
    """
    etat1, etat2, etat3, etat4 = True, True, True, True
    method_choice, type_choice, file_choice, shift_choice = None, None, None, None

    all_digits = digits + "-"
    
    while etat1:
        method_choice = str(input("Quelle méthode souhaitez-vous utiliser (chiffrer/déchiffrer): "))
        etat1 = False if method_choice in ["chiffrer", "déchiffrer"] else True

    while etat2:
        type_choice = str(input(f"Quelle type pour {method_choice} voulez-vous utiliser (Rot/Dictionnaire): "))
        etat2 = False if type_choice in ["Rot", "Dictionnaire"] else True

    while etat3:
        file_choice = str(input(f"Souhaitez-vous {method_choice} depuis un fichier (Y/n): "))
        etat3 = False if file_choice in ["Y", "n"] else True

    if type_choice == "Rot":
        while etat4:
            try:
                shift_choice = int(input(f"Avec quel décalage souhaitez-vous {method_choice}: "))
                etat4 = False if all(str(x) in all_digits for x in str(shift_choice)) else True
            except ValueError:
                print("Veuillez entrer un nombre valide.")

    return method_choice, type_choice, file_choice, shift_choice


def ask_text(etat: str):
    """
    Fonction pour demander le texte à l'utilisateur.

    Args:
        etat (str): L'état actuel (chiffrer/déchiffrer).

    Returns:
        str: Le texte fourni par l'utilisateur.
    """
    text = str(input(f"Quel est votre texte à {etat}: "))
    return text


def write_file(text: str, decal: int, methode: str, __name_file: str = None) -> str:
    """
    Fonction pour écrire le texte dans un fichier.

    Args:
        text (str): Le texte à écrire.
        decal (int): Le décalage utilisé.
        methode (str): La méthode utilisée (chiffrer/déchiffrer).
    """
    if __name_file is None:
        with open(f"./rot{decal}_{methode}.md", "w") as file:
            file.write(text)
    else:
        with open(f"{__name_file}", 'w') as file:
            file.write(text)


def read_file(name_file: str) -> str:
    """
    Fonction pour lire le contenu d'un fichier.

    Args:
        name_file (str): Le nom du fichier à lire.

    Returns:
        str: Le contenu du fichier.
    """
    with open(f"{name_file}", "r") as file:
        return file.read()


def chiffrer(text: str, decal: int) -> str:
    """
    Fonction pour chiffrer le texte.

    Args:
        text (str): Le texte à chiffrer.
        decal (int): Le décalage pour le chiffrement.

    Returns:
        str: Le texte chiffré.
    """
    chiffrement = ""

    for char in text:
        if char not in ascii_printable:
            chiffrement += char
        else:
            if char.islower():
                index = (ascii_printable.index(char) + decal) % alphabet_length
            else:
                index = (ascii_printable.index(char) + decal) % alphabet_length + alphabet_length
                
            chiffrement += ascii_printable[index]

    return chiffrement


def chiffrement_dictionary(text: str) -> str:
    """
    Fonction pour chiffrer le texte avec un dictionnaire aléatoire.

    Args:
        text (str): Le texte à chiffrer.

    Returns:
        str: Le texte chiffré.
    """
    aux_ascii_printable: str = ascii_letters  # variable qui stocke [a-zA-Z]

    dico = dict()
    chiffrement = ""

    # création du dico aléatoire
    for elmt in aux_ascii_printable:
        value = choice(aux_ascii_printable)
        dico[f"{elmt}"] = value
        aux_ascii_printable = aux_ascii_printable.replace(value, "", 1)

    # pour chaque element du text
    for elmt_txt in text:
        # si l'element n'est pas dans ascii_printable (ex: un espace ou !)
        if elmt_txt not in ascii_printable:
            chiffrement += elmt_txt
        else:
            # pour chaque element du dico
            for elmt_dico in dico.keys():
                # si l'element du text == element du dico
                if elmt_txt == elmt_dico:
                    # chiffrement += dico.get(element)
                    chiffrement += dico.get(elmt_txt)

    with open("./Dico_For_Cypher.json", "w") as file:
        file.write(dumps(dico))

    return chiffrement


def dechiffrement_dictionary(text: str, dico: dict) -> str:
    """
    Fonction pour déchiffrer le texte avec un dictionnaire donné.

    Args:
        text (str): Le texte à déchiffrer.
        dico (dict): Le dictionnaire de chiffrement.

    Returns:
        str: Le texte déchiffré.
    """
    aux_ascii_printable: str = ascii_letters  # variable qui stocke [a-zA-Z]

    data = read_file(dico)

    dico = loads(data)
    dechiffrement = ""

    for elmt_txt in text:
        if elmt_txt not in aux_ascii_printable:
            dechiffrement += elmt_txt
        else:
            for key, value in dico.items():
                if elmt_txt == value:
                    dechiffrement += key

    return dechiffrement


def dechiffrer(text: str, decal: int) -> str:
    dechiffrement = ""

    for char in text:
        if char not in ascii_printable:
            dechiffrement += char
        else:
            if char.islower():
                index = (ascii_printable.index(char) - decal) % alphabet_length
            else:
                index = (ascii_printable.index(char) - decal) % alphabet_length + alphabet_length
                
            dechiffrement += ascii_printable[index]

    return dechiffrement


def main():
    """
    Fonction principale pour exécuter le programme.
    """
    tuple_info = ask_info()  # tuple_info[0] = chiffrer, tuple_info[1] = Dictionnaire, tuple_info[2] = Y, tuple_info[3] = 13 (décalage)

    # Utilisation d'une correspondance de motif (pattern matching) pour gérer différentes options
    match tuple_info[0:3]:
        case ("chiffrer", "Rot", "Y"):
            # Chiffrement avec rotation depuis un fichier
            name_file = str(input(f"Quel est le nom du fichier (ex: {tuple_info[0]}.md): "))
            write_file(chiffrer(read_file(name_file), tuple_info[3]), tuple_info[3], tuple_info[0])
            print(f"Done ! Le fichier rot{tuple_info[3]}_chiffrer.md à été créer et, il contient le chiffrement de votre fichier {name_file} !")

        case ("chiffrer", "Rot", "n"):
            # Chiffrement avec rotation depuis une entrée utilisateur
            print(chiffrer(ask_text(tuple_info[0]), tuple_info[3]))

        case ("chiffrer", "Dictionnaire", "Y"):
            # Chiffrement avec dictionnaire depuis une entrée utilisateur
            name_file = str(input("Quel est le nom du fichier à créer pour stocker le résultat (ex: dico.md): "))
            write_file(chiffrement_dictionary(ask_text(tuple_info[0])), tuple_info[3], tuple_info[0], name_file)
            print(f"Done ! Le fichier {name_file} à été créer et, il contient le chiffrement de votre texte ! Et le dictionnaire utilisé a été créer ici: Dico_For_Cypher.json !")

        case ("chiffrer", "Dictionnaire", "n"):
            # Chiffrement avec dictionnaire sans stockage dans un fichier
            print(chiffrement_dictionary(ask_text(tuple_info[0])))
            print("Le dictionnaire a été enregistré ici: Dico_For_Cypher.json")

        case ("déchiffrer", "Rot", "Y"):
            # Déchiffrement avec rotation depuis un fichier
            name_file = str(input(f"Quel est le nom du fichier (ex: {tuple_info[0]}.md): "))
            write_file(dechiffrer(read_file(name_file), tuple_info[3]), tuple_info[3], tuple_info[0])
            print(f"Done ! Le fichier rot{tuple_info[3]}_déchiffrer.md à été créer et, il contient le déchiffrement de votre fichier {name_file} !")

        case ("déchiffrer", "Rot", "n"):
            # Déchiffrement avec rotation depuis une entrée utilisateur
            print(dechiffrer(ask_text(tuple_info[0]), tuple_info[3]))

        case ("déchiffrer", "Dictionnaire", "Y"):
            # Déchiffrement avec dictionnaire depuis un fichier
            name_file = str(input("Quel est votre fichier à déchiffrer: "))
            name_json_file = str(input("Quel est le nom du fichier dictionnaire à utiliser pour le déchiffrement (ex: dico.md): "))
            write_file(dechiffrement_dictionary(read_file(name_file), name_json_file), tuple_info[3], tuple_info[0], "Dict_Dechiffrement.txt")
            print(f"Done ! Le fichier Dict_Dechiffrement.txt à été créer et, il contient le déchiffrement de votre fichier {name_file} !")

        case ("déchiffrer", "Dictionnaire", "n"):
            # Déchiffrement avec dictionnaire sans stockage dans un fichier
            name_file = str(input("Quel est le nom du fichier dictionnaire (ex: dico.md): "))
            print(dechiffrement_dictionary(ask_text(tuple_info[0]), name_file))

        case _:
            # Cas par défaut si aucune correspondance n'est trouvée
            print('Erreur dans le code...')


if __name__ == "__main__":
    print(r"""
  ______                              _
 / _____)                            (_)   _                    _
( (____   _____   ____  _   _   ____  _  _| |_  _____  _   _  _| |_
 \____ \ | ___ | / ___)| | | | / ___)| |(_   _)| ___ |( \ / )(_   _)
 _____) )| ____|( (___ | |_| || |    | |  | |_ | ____| ) X (   | |_
(______/ |_____) \____)|____/ |_|    |_|   \__)|_____)(_/ \_)   \__)

""")
    main()