
#10 jin zhi to 2 jin zhi
def Dec2bit(number, bitCount):
    if number == 0:
        strList = ['0'] * bitCount
    else:
        strList = ['0'] * bitCount
        index = len(strList) - 1
        while(number != 0):
            shang = number / 2
            yushu = number % 2
            strList[index] = str(yushu)
            index -= 1
            number = shang
    return ''.join(strList)

#######################################API######################

#N is the population size, pop0_list is the individual list.
#pop0_list[i] = 'xxxxxxxx'
#x=[x_s, x_e] = [1,10]
#y=[y_s, y_e] = [1, 100]
def InitPop(N, x_s, x_e, y_s, y_e, bitCount_x, bitCount_y):
    pop_list = list()
    import random

    if x_s == x_e or bitCount_x == 0:  # x is specified and not change
        while len(pop_list) < N:
            #y=[1,2,...,100]
            yi = random.randint(y_s, y_e)
            yibit = Dec2bit(yi, bitCount_y)
            oneStr = yibit
            pop_list.append(oneStr)
            #print  yi, yibit, oneStr
    elif x_s < x_e and y_s < y_e:
        while len(pop_list) < N:
            #x=[1,1,2,...,10]
            xi = random.randint(x_s, x_e)
            #y=[1,2,...,100]
            yi = random.randint(y_s, y_e)

            xibit = Dec2bit(xi, bitCount_x)
            yibit = Dec2bit(yi, bitCount_y)
            oneStr = xibit + yibit
            pop_list.append(oneStr)
            #print xi, xibit, yi, yibit, oneStr
    else:
            print 'error'

    return  pop_list

#
def Bit2Dec(bitstr):
    #print bitstr
    number = 0
    for index in range(0, len(bitstr)):
        bit = len(bitstr) - 1 - index
        if bitstr[index] == '1':
            number += pow(2, bit)
    return number

def TransCode2Indiv(indiv, x_s, x_e, y_s, y_e, bitCount_x, bitCount_y):
    if bitCount_x != 0 and bitCount_y != 0 and x_s < x_e and y_s < y_e:
        bitstr_x = indiv[0: bitCount_x]
        bitstr_y = indiv[bitCount_x: bitCount_x + bitCount_y]
        number_x = Bit2Dec(bitstr_x)
        number_y = Bit2Dec(bitstr_y)
        #print bitstr_x,bitstr_y, number_x, number_y
    elif bitCount_x == 0 or x_s == x_e:   # x_x == x_e, x is given, not change
        number_x = x_s #x_s = x_e
        bitstr_y = indiv
        number_y = Bit2Dec(bitstr_y)
    else:
        print 'error'
    return number_x, number_y


#x=[x_s,....x_e]   y=[y_s, ..., y_e]
def IsValidIndiv(indiv, x_s, x_e, y_s, y_e, bitCount_x, bitCount_y):
    [number_x, number_y] = TransCode2Indiv(indiv, x_s, x_e, y_s, y_e, bitCount_x, bitCount_y)
    if number_x >= x_s and number_x <= x_e and number_y >= y_s and number_y <= y_e:
        return True
    else:
        return False
