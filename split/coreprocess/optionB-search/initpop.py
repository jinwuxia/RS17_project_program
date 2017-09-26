
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



#N is the population size, pop0_list is the individual list.
#pop0_list[i] = 'xxxxxxxx'
#x=[x_s, x_e] = [1,10]
#y=[y_s, y_e] = [1, 100]
def InitPop(N, x_s, x_e, y_s, y_e):
    pop_list = list()
    import random
    for index in range(0, N):
        #x=[1,1,2,...,10]
        xi = random.randint(x_s, x_e)
        #y=[1,2,...,100]
        yi = random.randint(y_s, y_e)

        xibit = Dec2bit(xi, bitCount=4)
        yibit = Dec2bit(yi, bitCount=7)
        oneStr = xibit + yibit
        pop_list.append(oneStr)
        print xi, xibit, yi, yibit
    return  pop_list
