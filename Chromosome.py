import numpy as np

class Chromosome(object):

    def __init__(self, size_dest, size_trans):
                
        self.crm_prm = np.random.permutation(size_dest)
        self.crm_int = np.random.randint(size_trans+1, size=size_dest)
        self.waktu = 0 
        self.uang = 0

        self.value = 0
        self.probv = 0.0



