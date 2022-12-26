
lb = [      "P#----",
            "-#-##-",
            "------",
            "--###-",
            "--#-X-"]



def solve_labirint(labirint, yaqin_tomon="o'ng"):
    res = []

    # Listimizni chetlariga qo'shimcha # qo'shib chiqamiz. 
    # Index errorni yuqotish uchun
    def list_edging(lb):
        lb = list(map(lambda x: list(x), lb))
        lb.insert(0, ["#"]*6)
        lb.append(["#"]*6)
        for i in lb:
            i.insert(0,"#")
            i.append("#")   
        return lb

    labirint = list(map(lambda x: list(x), labirint))
    labirint = list_edging(labirint)    
    
    rows = len(labirint)-1
    columns = len(labirint[0])-1

    coor =  [( labirint.index(a),a.index(b)) for a in labirint for b in a if b =="X"]
    vertikal, gorizonal = coor[0]

    start = [(labirint.index(a), a.index(b)) for a in labirint for b in a if b == "P"] 
    x, y = start[0]
    tomon = "right" if y < gorizonal else "left"
    
  

    def inner(labirint):
        p = "p"
        

        start = [(labirint.index(a), a.index(b)) for a in labirint for b in a if b == "P"] 
        x, y = start[0]
        # P ning boshlang'ich indexini  for loopda topib olamiz
        
        
        while p != 'X':
            if (labirint[x][y-1]=='-' or labirint[x][y-1]=="X") and y-1 != 0 and y >= gorizonal:
                if labirint[x][y-1]=='X':
                    res.append("chapga")
                    p = "X"
                    return res
                else:
                    labirint[x][y-1]='P'
                    labirint[x][y] = '-'
                    y = y-1
                    res.append("chapga")
                    return inner(labirint)
                
        
            
            if (labirint[x+1][y] == "-" or labirint[x+1][y]=="X") and x <rows and vertikal >= x:
                if labirint[x+1][y] == "X":
                    res.append("pastga")
                    p = "X"
                    return res
                else:
                    labirint[x+1][y] = "P"
                    labirint[x][y] = "-"
                    x = x+1
                    res.append("pastga")
                    return inner(labirint)
                    

            if  (labirint[x][y+1]=='-' or labirint[x][y+1]=='X') and y < columns and  y <= gorizonal:
                if labirint[x][y+1]=='X':
                    res.append("o'ngga")
                    p = "X"
                    return res
                else:
                    labirint[x][y+1]='P'
                    labirint[x][y] = '-'
                    y = y+1
                    res.append("o'ngga")
                    return inner(labirint)
                    

            if (labirint[x-1][y] == "-" or labirint[x-1][y] =="X") and  x-1 != 0 and vertikal <= x:
                if labirint[x-1][y] == "X":
                    res.append("tepaga")
                    p="X"
                    return res
                else:    
                    labirint[x-1][y] = "P"
                    labirint[x][y] = "-"
                    x= x-1
                    res.append("tepaga")
                    return inner(labirint)
                    
        
            
    def inner2(labirint):
        p = "p"
        

        start = [(labirint.index(a), a.index(b)) for a in labirint for b in a if b == "P"] 
        x, y = start[0]
        # P ning boshlang'ich indexini  for loopda topib olamiz
        
        
        while p != 'X':

            if  (labirint[x][y+1]=='-' or labirint[x][y+1]=='X') and y < columns and  y <= gorizonal:
                if labirint[x][y+1]=='X':
                    res.append("o'ngga")
                    p = "X"
                    return res
                else:
                    labirint[x][y+1]='P'
                    labirint[x][y] = '-'
                    y = y+1
                    res.append("o'ngga")
                    return inner2(labirint)
                    
            
        
            
            if (labirint[x+1][y] == "-" or labirint[x+1][y]=="X") and x <rows and vertikal >= x:
                if labirint[x+1][y] == "X":
                    res.append("pastga")
                    p = "X"
                    return res
                else:
                    labirint[x+1][y] = "P"
                    labirint[x][y] = "-"
                    x = x+1
                    res.append("pastga")
                    return inner2(labirint)
                    

            if (labirint[x][y-1]=='-' or labirint[x][y-1]=="X") and y-1 != 0 and y >= gorizonal:
                if labirint[x][y-1]=='X':
                    res.append("chapga")
                    p = "X"
                    return res
                else:
                    labirint[x][y-1]='P'
                    labirint[x][y] = '-'
                    y = y-1
                    res.append("chapga")
                    return inner2(labirint)
                

            if (labirint[x-1][y] == "-" or labirint[x-1][y] =="X") and  x-1 != 0 and vertikal <= x:
                if labirint[x-1][y] == "X":
                    res.append("tepaga")
                    p="X"
                    return res
                else:    
                    labirint[x-1][y] = "P"
                    labirint[x][y] = "-"
                    x= x-1
                    res.append("tepaga")
                    return inner2(labirint)
                    
             
    if yaqin_tomon == "chap":        
        return inner(labirint)
    elif yaqin_tomon =="o'ng":
        return inner2(labirint)        

print(solve_labirint(lb,"chap"))
