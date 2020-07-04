

import random as rand
import math

N = 4 #Nombre de pions
k = 8 #nombre de couleurs

#Format de la solution candidate:
Solution_candidate = [0, 0, 0, 0]


Colors = [1, 2, 3, 4, 5, 6, 7, 8]
#Ensemble des couleurs possibles:
#1:Rouge #2:Bleu #3:Jaune #4:Vert
#5:Noir #6:Orange #7:Violet #8:Gris

#Donne le résultat à trouver:
solution = [rand.choice(Colors) for i in range(len(Solution_candidate))]
HISTORIQUE = []
Liste_index_score = []


def tirage():  # Tirage aletoire dans le set de couleurs pour former un candidat valide
    Hypothese=[rand.choice(Colors) for i in range(len(Solution_candidate))]
    return(Hypothese)

def compare(coup,ref): # fonction qui compare deux combinaisons pour en resortir les p,m
    copie_ref = ref.copy()
    p = 0
    m = 0
    for i in range(len(coup)):
        if coup[i]==copie_ref[i]:
           p = p+1
           copie_ref[i] = 0 # Pour eviter de compter plusieurs fois une couleur bien placée
    for i in range(len(coup)):
        for j in range(len(coup)):
            if coup[i] == copie_ref[j]:
                m = m+1
                copie_ref[j] = 0
    return(p, m)

def score(p,m):
    res = (23*p)+(5*m)
    return res

def score_mastermind(Tentative,solution): #Fonction qui calcule le score entre le candidat joué et la solution
    p1, m1 = compare(Tentative, solution)
    res = score(p1, m1)
    return res
def mastermind(Tentative,solution): # Fonction qui verifie si le candidat joué est valide
    if Tentative == solution:
        return True
    else:
        return False

def insertion_historique(Tentative):
    copie_tentative =Tentative.copy()
    HISTORIQUE.append(copie_tentative)
    return HISTORIQUE
def insertion_score(score_mastermind):
    Liste_index_score.append(score_mastermind)
    return Liste_index_score



def eval(Tentative, candidat, j):
    p2, m2 = compare(Tentative, candidat)
    res = Liste_index_score[j] - score(p2, m2)
    return(abs(res))

def population_solutions_candidates(demographie): #Fonction qui génère aleatoirement une population de candidats
    Population = []
    for i in range(demographie):
        Population.append(tirage())
    return Population

def init_fitness_population_candidats(demographie): #Fonction qui initialise le tableau des fitness
    Liste_index_fitness = []
    for i in range(demographie):
        Liste_index_fitness.append([0,i]) # Le second element represente l'index de la combinaison dans la population
                                          # Le premier lui represente la fitness de chaque element

    return Liste_index_fitness


def fitness(liste): #Fonction qui calcule la fitness pour un element de la population en fonction de l'historique
    Sum = 0
    for i in range(len(HISTORIQUE)):
        Sum = Sum + eval(HISTORIQUE[i], liste, int(i))
    return Sum

def total_fitness(population, Liste_index_fitness): # Fontion qui itère la fonction précédente et permet insis de calculer la fitness de tous les elements de la population.

    for i in range(len(population)):
        Liste_index_fitness[i][0] = fitness(population[i])

    return Liste_index_fitness

def calcul_du_nb_des_meilleurs(nb_isoler):
    nb_des_meilleurs = nb_isoler
    return nb_des_meilleurs

"""def calcul_du_nb_des_meilleurs(pourcentage, taille_de_la_population):
    nb_des_meilleurs = math.floor((taille_de_la_population * pourcentage))
    #print("NB A ISOLER :", nb_des_meilleurs)
    return nb_des_meilleurs"""

def selection_des_meilleurs(nb_des_meilleurs, population, listefitness):
    Liste_des_meilleurs = []
    res = 0
    compteur_de_tours = 0
    stop_condition = 0
    #print(len(Liste_des_meilleurs))
    while len(Liste_des_meilleurs) <= nb_des_meilleurs:
        for i in range(len(population)):
            if listefitness[i][0] == res:
                #print("valeur de la fitness =", listefitness[i][0])
                #print("Indice de la combinaison ayant cette fitness =", listefitness[i][1])
                Liste_des_meilleurs.append(population[listefitness[i][1]])
            if len(Liste_des_meilleurs) == nb_des_meilleurs:
                stop_condition = 1
                break
        if stop_condition == 1:
            break
        else:
            res = res+1
            compteur_de_tours = compteur_de_tours + 1

    return Liste_des_meilleurs



def brassage_genetique(Liste_des_meilleurs):
    iteration = 7*len(Liste_des_meilleurs)
    Temp=[]
    
    for i in range(iteration):
        cut1 = rand.choice([0, 1, 2])
        part_1 = rand.choice(Liste_des_meilleurs)
        part_2 = rand.choice(Liste_des_meilleurs)

        while part_1 == part_2: #pour faire en sorte qu'on croise pas deux memes combinaisons
            part_2 = rand.choice(Liste_des_meilleurs)

        nouveau_element_1 = part_1[0:(cut1+1)]+part_2[(cut1+1):4]
        Temp.append(nouveau_element_1)

        if len(Liste_des_meilleurs) > 2000:
            break
    #print("LISTE apres taille:", len(Temp))
    Liste_des_meilleurs=Liste_des_meilleurs+Temp
    #print("TAILLE FINALE :", len(Liste_des_meilleurs))
    return Liste_des_meilleurs


def mutation(taux_de_mutation, Liste_des_meilleurs):
    longueur = len(Liste_des_meilleurs)
    nb_de_mutation = math.floor(longueur * taux_de_mutation)
    for i in range(nb_de_mutation):
        indice_1 = rand.choice([0, 1, 2, 3])
        indice_2 = rand.choice([0, 1, 2, 3])
        x = rand.choice([t for t in range(longueur)])
        etape1 = Liste_des_meilleurs[x].copy()
        etape2 = Liste_des_meilleurs[x].copy()
        if indice_1 == indice_2 and indice_2 == 3:
            indice_2 = indice_2-rand.choice([0, 1, 2])
            etape1[indice_1] = etape2[indice_2]
            etape1[indice_2] = etape2[indice_1]
        elif indice_1 == indice_2 and indice_2 == 0:
            indice_2 = rand.choice([1, 2, 3]) - indice_2
            etape1[indice_1] = etape2[indice_2]
            etape1[indice_2] = etape2[indice_1]
        elif indice_1 == indice_2:
            r = [0, 1, 2, 3]
            r.remove(int(indice_2))
            indice_2 = rand.choice(r)
            etape1[indice_1] = etape2[indice_2]
            etape1[indice_2] = etape2[indice_1]
        else:
            etape1[indice_1] = etape2[indice_2]
            etape1[indice_2] = etape2[indice_1]
        Liste_des_meilleurs[x] = etape1
    return (Liste_des_meilleurs)

def condition_arret(population,listedefitness):
    Res = False
    """if len(population)==len(listedefitness):
        print("TOUT VA BIEN !!!")"""
    for i in range(len(population)):
        if listedefitness[i][0] == 0:
            Res = True
    #print(Res)
    return Res

def selection_premier_element(population, listedefitness):
    for i in range(len(population)):
        if listedefitness[i][0] == 0:
            Tent = population[listedefitness[i][1]]
    return Tent


if __name__ == "__main__":

#Quelques variables:
    Taille_de_la_population = 200
    #pourcentage = 0.9
    K_meilleurs = 45  # TOUJOURS INFERIEUR A TAILLE DE POPULATION
    Taux_de_mutation = 0.1
    Nb_de_coup_possibles = 12
    Nb_de_coup_joue = 0

#1ere etape: génération de la solution et premiere tentative
    print("SOLUTION A TROUVER", solution)
    Tentative = tirage()
    print("Premier tentative", Tentative)

    while mastermind(Tentative, solution)==False and Nb_de_coup_joue < Nb_de_coup_possibles:
        #2eme etape : on place la tentative et son score dans l'historique
        insertion_historique(Tentative)
        insertion_score(score_mastermind(Tentative, solution))
        Nb_de_coup_joue = Nb_de_coup_joue + 1

        #3eme etape : on cree notre population de solution qui permettra de determiner la prochaine tentative
        POP = population_solutions_candidates(Taille_de_la_population)
        #print("POPULATION :", POP)
        Fitness_de_la_pop = init_fitness_population_candidats(Taille_de_la_population)
        #print("LISTE DE FITNES INIT :",Fitness_de_la_pop ) #ATTENTION efface la liste si la fonction est appelée une seconde fois

        #4eme etape : on calcule nos evals et donc nos fitness pour chaque element de la population
        Fitness_de_la_pop = total_fitness(POP, Fitness_de_la_pop)
        #print("FITNESS PAR POPULATION :", Fitness_de_la_pop)

        zz=0
        while condition_arret(POP,Fitness_de_la_pop) == False :
            # brassage genetique + nouvelle fitness
            #Nb_selectionne = calcul_du_nb_des_meilleurs(pourcentage, len(POP))
            Nb_selectionne = calcul_du_nb_des_meilleurs(K_meilleurs)
            #print("taille :", len(POP))
            BEST_POP = selection_des_meilleurs(Nb_selectionne, POP, Fitness_de_la_pop)
            BEST_POP = brassage_genetique(BEST_POP)
            BEST_POP = mutation(Taux_de_mutation, BEST_POP)
            POP = BEST_POP
            Fitness_de_la_pop = init_fitness_population_candidats(len(POP))
            Fitness_de_la_pop = total_fitness(POP, Fitness_de_la_pop)
            #print("fitness fin genetique ", Fitness_de_la_pop)
            zz = zz+1
            if zz > 4000:
                print("BLOQUE DANS LA GENETIQUE: ON A FAIT << ",zz,">> tours ")
                exit(-1)



        Tentative = selection_premier_element(POP, Fitness_de_la_pop)
        print(Tentative)


    if mastermind(Tentative, solution) == True:
        print("SUCCES")
        print("Voici l historique des coups => ", HISTORIQUE)

        print("Nombre de coup joue =", Nb_de_coup_joue+1)
    else:
        print("Nombre de coup permis dépassé :", Nb_de_coup_joue+1 )
        print(solution)

    exit(0)