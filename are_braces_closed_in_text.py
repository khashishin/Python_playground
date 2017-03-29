x = input()
def sprawdz_nawiasy(string):
    braces = {"(":")","[":"]","{":"}"}
    list=[]
    for sign in string:
        if sign in braces.keys():
            list.append(braces[sign])
        elif sign in braces.values():
            if len(list)==0:
                return False
            elif sign != list.pop():
                return False
            else:
                continue
    if len(list)>0:
        return False
    else:
        return True


print (sprawdz_nawiasy(x))

