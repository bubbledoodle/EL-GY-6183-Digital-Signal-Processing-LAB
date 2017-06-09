#simple selection sorting
def sort_1(x):
    sorting_x = []
    for i in range(len(x)):
        n = x[0]
        #min
        for j in range(1,len(x)):
            if n>=x[j]:
                n = x[j]
        sorting_x.append(n)
        x.remove(n)
    print "sorted x: " + `sorting_x`

# bubble sorting
def sort_2(x):
    #test = x[0]
    #tmp = x[0]
    for i in range(0,len(x)):
        for j in range(0,len(x)-i-1):
            if x[j] > x[j+1]:
                #test = tmp
                tmp = x[j+1]
                x[j+1] = x[j]
                x[j] = tmp
        #if test == tmp:
            #break
    print "sorted x: " + `x`

