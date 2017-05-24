import numpy as np
import csv
import matplotlib.pyplot as plt
from copy import deepcopy, copy

from Chromosome import Chromosome

score = []

#Algen Parameters
probm = 0.3
probc = 0.6
pop_size = 30
size_dest = 6
size_trans = 3
generation = 50

trans_val = ["Trans Jogja",  "Taksi", "Gojek"] 
posisi = 4
pos_val = ["Malioboro", "Candi Prambanan", "Candi Borobudur", "Pantai Parangtritis", "Monumen Jogja Kembali" , "Ulen Sentalu"]
uang = 200000 # in Rupiah
waktu = 200  # in Minutes
value = [3, 4, 4, 3, 1, 4] 


def generate():
    population = []
    for i in xrange(pop_size):
        ind = Chromosome(size_dest, size_trans)
        while not constraint(ind):
            ind = Chromosome(size_dest, size_trans)
        population.append(ind)
    return population

def fitness(individu):
    sebelumnya = posisi
    gen_value = 0
    for i in xrange(len(individu.crm_prm)):
        p = individu.crm_prm[i]
        k = individu.crm_int[i]
        
        if (k != 3):
            gen_value = gen_value + value[p]
            sebelumnya = p
    return gen_value

def constraint(individu):
    # starting position
    for i in xrange(len(individu.crm_prm)):
        if (individu.crm_prm[i] == posisi) and (individu.crm_int[i]!=3):
            return False

    # transjogja constraint
    sebelumnya = posisi
    for i in xrange(len(individu.crm_prm)):
        p = individu.crm_prm[i]
        k = individu.crm_int[i]
        if (k == 0) and (score[k][sebelumnya][p][0]==-1):
            return False
        if (k != 3):
            sebelumnya = p
            
    # time
    sebelumnya = posisi
    gen_waktu = 0
    for i in xrange(len(individu.crm_prm)):
        p = individu.crm_prm[i]
        k = individu.crm_int[i]

        if (k != 3):
            gen_waktu = gen_waktu + score[k][sebelumnya][p][0]
            sebelumnya = p
    
    if(gen_waktu > waktu):
        return False

    # budget
    sebelumnya = posisi
    gen_uang = 0
    for i in xrange(len(individu.crm_prm)):
        p = individu.crm_prm[i]
        k = individu.crm_int[i]
        if (k != 3):
            gen_uang = gen_uang + score[k][sebelumnya][p][1]
            sebelumnya = p
    # print gen_uang
    if(gen_uang > uang):
        return False
    
    individu.waktu = gen_waktu
    individu.uang = gen_uang
    return True

def selection(population):
    total_fitness = np.sum([ind.value for ind in population])
    ind_prob = []
    new_pop  = []
    selector = np.random.rand(pop_size)

    for ind in population:
        ind_prob.append(1.0*ind.value/total_fitness)
    
    for i in xrange(len(ind_prob)):
        if i!=0:
            ind_prob[i] = ind_prob[i] + ind_prob[i-1]

    for i in xrange(pop_size):
        x = np.random.rand()
        parent = 0
        for j in xrange(len(ind_prob)):
            if ind_prob[j] > x:
                parent = j
                break
        new_pop.append(population[parent])

    return new_pop

def crossover_permute(individu_a, individu_b):
    parent_a = deepcopy(individu_a)
    parent_b = deepcopy(individu_b)
    offspring_a = deepcopy(individu_a)
    offspring_b = deepcopy(individu_b)

    size = len(parent_a.crm_prm)
    
    tp1 = np.random.randint(size-1)
    tp2 = tp1+1

    offspring_a.crm_prm = np.zeros(len(parent_a.crm_prm), dtype=int)
    offspring_b.crm_prm = np.zeros(len(parent_b.crm_prm), dtype=int)

    offspring_a.crm_prm[tp1:tp2+1] = deepcopy(parent_a.crm_prm[tp1:tp2+1])
    offspring_b.crm_prm[tp1:tp2+1] = deepcopy(parent_b.crm_prm[tp1:tp2+1])

    now_a = tp2+1
    now_b = tp2+1

    for i in xrange(size):
        if parent_b.crm_prm[(now_b)%size] not in offspring_a.crm_prm[tp1:tp2+1]:
            offspring_a.crm_prm[(now_a)%size] =  deepcopy(parent_b.crm_prm[(now_b)%size])
            now_a += 1
        now_b += 1

    now_a = tp2+1
    now_b = tp2+1
    for i in xrange(size):
        if parent_a.crm_prm[(now_a)%size] not in offspring_b.crm_prm[tp1:tp2+1]:
            offspring_b.crm_prm[(now_b)%size] =  deepcopy(parent_a.crm_prm[(now_a)%size])
            now_b += 1
        now_a += 1

    offspring_a.crm_prm = np.asarray(offspring_a.crm_prm)
    offspring_b.crm_prm = np.asarray(offspring_b.crm_prm)

    return [offspring_a, offspring_b]

def crossover_integer(individu_a, individu_b):
    offspring_a = deepcopy(individu_a)
    offspring_b = deepcopy(individu_b)

    size = len(individu_a.crm_int)
    
    tp1 = np.random.randint(size)

    temp = deepcopy(offspring_b.crm_int[tp1:])
    offspring_b.crm_int[tp1:] = deepcopy(offspring_a.crm_int[tp1:])
    offspring_a.crm_int[tp1:] = deepcopy(temp)
    
    return [offspring_a, offspring_b]

def mutation(individu):
	size = len(individu.crm_int)
	
	i = np.random.randint(size)
	j = np.random.randint(size)
	individu.crm_prm[i], individu.crm_prm[j] = individu.crm_prm[j], individu.crm_prm[i]

	i = np.random.randint(size)
	individu.crm_int[i] = np.random.randint(size_trans)

	return individu


#===============================================================================================
# Main Program - Algen untuk wisata di Jogja
#================================================================================================
def main():
    data = []
    global score

    with open('data.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            data.append(row)  
    
    score = [[[0 for j in xrange(size_dest)] for i in xrange(size_dest)] for k in xrange(size_trans)]
    for k in xrange(size_trans):
        for i in xrange(size_dest):
            for j in xrange(size_dest):
                score[k][i][j] = (int(data[i+k*size_dest*2][j]), int(data[i+size_dest+k*size_dest*2][j]))

    score = np.asarray(score)
    # score[ kendaraan ][destinasi awal][destinasi akhir][waktu/biaya]
    # score 3 x 6 x 6 x 2

    population = generate()
    for ind in population:
        ind.value = fitness(ind)

    value_in_time = []
    for g in xrange(generation):
        print ''
        print 'GENERATION ', g+1,'/',generation
        print '----selection----'
        population = selection(population)
        
        print '----crossover----'
        offspring_p = []
        i = 0
        while i<len(population):
            pc_i = np.random.rand()
            if pc_i <= probc:
                if i+1<len(population):
                    res = crossover_permute(population[i], population[j])
                    offspring_p += res
                    i+=1
            i += 1
        offspring_p = np.asarray(offspring_p)
        
        offspring = []
        i = 0
        while i<len(offspring_p):
            pc_i = np.random.rand()
            if pc_i <= probc:
                if i+1<len(offspring_p):
                    res = crossover_integer(offspring_p[i], offspring_p[i+1])
                    offspring += res
                    i += 1
            i += 1
        offspring = np.asarray(offspring)

        # ----mutation----
        for o in offspring:
			pm = np.random.rand()
			if pm <= probm:
				o = mutation(o)

        # ----update----
        # kill the baby!
        newgen = []
        for o in offspring:
            if constraint(o):
                o.value = fitness(o)
                newgen.append(o)

		# ----FOR DEBUGGING----
        # print 'OFFSPRING-SELECTED'
        # for o in newgen:
        #     print o.crm_prm, o.crm_int, o.value

        population.sort(key=lambda ind: ind.value, reverse=True)
        newgen.sort(key=lambda ind: ind.value, reverse=True)

        if newgen == pop_size:
            elite = deepcopy(population[0])
            population = deepcopy(newgen)
            population[-1] = deepcopy(elite)
        elif newgen:
            population[-len(newgen):] = deepcopy(newgen)

        value_in_time.append(population[0].value)
    
    print "\n"
    print "Uang : Rp ", uang
    print "Waktu Yang Dimiliki : ", waktu, " Menit"
    print "Start dari : ", pos_val[posisi]
    print ''
    print 'SOLUTION'
    solution = population[0]
    print solution.crm_prm, solution.crm_int, solution.value
    print "\n"
    
    # Display
    isi_prm, isi_int = solution.crm_prm, solution.crm_int
    print "Rute Perjalanan: "  
    pos = posisi
    for i in xrange(len(isi_prm)):
        if (isi_int[i]!=3):
            print pos_val[pos] + " >> " + pos_val[isi_prm[i]] + " by " + trans_val[isi_int[i]]
            pos = isi_prm[i]
    print "indeks kepuasan = ", solution.value

    # Graph
    plt.plot(value_in_time)
    plt.ylabel('Best Value')
    plt.xlabel('Generation')
    plt.show()
                

if __name__=="__main__":
    main()