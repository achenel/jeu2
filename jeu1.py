import random
print ("Bonjour !")
nombre = random.randint (1, 100)
reponse = int(input("Trouve le nombre entier positif auquel je pense.\n"))
compteur = 1
while reponse != nombre:
    compteur += 1
    if reponse < nombre:
        print("C'est plus")
    else : print("c'est moins")
    reponse = int(input("Essaye encore\n"))
print("Bravo !Tu as réussi en " + str(compteur) + " coups !")