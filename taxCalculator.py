def MH(salary, nz):
    salaryTemp = salary
    MHtemp = 0
    lastLevel = 0
    nzValue = 219
    taxLevels = ([6290,0.1],[9030,0.14],[14490,0.2],
                 [20140,0.31],[41910,0.35],[53970,0.47],[53971,0.5])
    length = len(taxLevels)
    counter = 0
    for i in taxLevels:
        if salary > i[0] and counter<length-1:
            MHtemp += (i[0]-lastLevel) * i[1]
            salaryTemp = salary - i[0]
            lastLevel = i[0]
            counter += 1
        else:
            MHtemp += salaryTemp * i[1]
            return max(MHtemp-nz*nzValue,0)
    return max(MHtemp-nz*nzValue,0)


def BL(salary):
    avrgSalary = 6331
    blr1 = 0.004 # bituh leumi tax rate below average salary
    bbr1 = 0.031  # bituh briut tax rate below average salary
    blr2 = 0.07  # bituh leumi tax rate above average salary
    bbr2 = 0.05  # bituh briut tax rate above average salary
    BLtemp = 0
    BBtemp = 0
    if salary < avrgSalary:
        return blr1*salary, bbr1*salary
    else:
        BLtemp = min((salary-avrgSalary)*blr2+avrgSalary*blr1,2665.48)
        BBtemp = min((salary - avrgSalary) * bbr2 + avrgSalary * bbr1,2077.38)
        return BLtemp, BBtemp


def VAT(expanses,gasoline,elect,water):
    vat = 0.17
    return vat*(expanses+gasoline+elect+water)


def gasolineTax(gasoline):
    blueTax = 0.5
    return blueTax*gasoline


def carTaxCalc(car):
    if car==0:
        return 0
    years = 5
    valuelost = 0.9 #10% per year
    licenseFee = 1200
    return round(car*(1-(pow(valuelost,years)))*0.5)/(12*years) + licenseFee/12 #50% of neto
