def boundInt16(x):
    if x > 10173:
        x = 10173
    else:
        if x<-10173:
            x = -10173
    return x

def boundInt8(x):
    if x > 39:
        x = 39
    else:
        if x<-39:
            x = -39
    return x

def bound4Order(x):
    if x > 19:
        x = 19
    else:
        if x<-19:
            x = -19
    return x
