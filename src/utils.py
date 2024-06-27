import csv


def getInsts():
    nTypeInsts = {}
    rTypeInsts = {}
    iTypeInsts = {}
    sTypeInsts = {}
    jTypeInsts = {}

    with open('../data/insts.csv', 'r') as file:
        reader = csv.reader(file)
        
        for row in reader[1:]:
            match row[1]:
                case 'n':
                    nTypeInsts.update({row[0]: row[2]})
                case 'r':
                    rTypeInsts.update({row[0]: row[2]})
                case 'i':
                    iTypeInsts.update({row[0]: row[2]})
                case 's':
                    sTypeInsts.update({row[0]: row[2]})
                case 'j':
                    jTypeInsts.update({row[0]: row[2]})
    
    return nTypeInsts, rTypeInsts, iTypeInsts, sTypeInsts, jTypeInsts


# Constants
N_TYPE_INTS, R_TYPE_INTS, I_TYPE_INTS, S_TYPE_INSTS, J_TYPE_INTS = getInsts()
INSTRUCTIONS = {**N_TYPE_INTS, **R_TYPE_INTS, **I_TYPE_INTS, **S_TYPE_INSTS, **J_TYPE_INTS}