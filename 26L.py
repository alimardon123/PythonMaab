
lb = [          "P#---X",
                "-#-##-",
                "---#--",
                "###-#-",
                "-#---",
                "---#--"]



def solve_labirint(labirint):
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

    labirint = list_edging(labirint)    
    
    rows = len(labirint)-1
    columns = len(labirint[0])-1

    coor =  [( labirint.index(a),a.index(b)) for a in labirint for b in a if b =="X"]
    dest_x, dest_y = coor[0]

    start = [(labirint.index(a), a.index(b)) for a in labirint for b in a if b == "P"] 
    a, b = start[0]
    tomon = "chap" if b > dest_y else "o'ng"


    # Movement funksiyalari: Chap, O_ng, Tepa, Past 
    def chap(a, b):
        x = a
        y = b
        labirint[x][y-1]='P'
        labirint[x][y] = '-'
        y = y-1
        res.append("chapga")
        return x, y
    
    def o_ng(a, b):
        x = a
        y = b
        labirint[x][y+1]='P'
        labirint[x][y] = '-'
        y = y+1
        res.append("o'ngga")
        return x, y

    def pastga(a, b):
        x = a
        y = b
        labirint[x+1][y] = "P"
        labirint[x][y] = "-"
        x = x+1
        res.append("pastga")        
        return x, y

    def tepaga(a, b):
        x = a
        y = b    
        labirint[x-1][y] = "P"
        labirint[x][y] = "-"
        x= x-1
        res.append("tepaga") 
        return x, y


    # Asosiy funksiyalar InnerChap  va InnerO'ng 
    # InnerChap Agar x Chapda turan bo'lsa ishlaydi
    def innerchap(labirint, x, y):
        x = x
        y = y

        if (labirint[x][y-1] !='#') and y-1 != 0 and y > dest_y :
            x, y = chap(x, y)
            if x ==dest_x and y ==dest_y:
                return res
                
        if  (labirint[x][y+1] !='#') and y < columns and  y < dest_y :
            x, y = o_ng(x, y)
            if x ==dest_x and y ==dest_y:
                return res   
            
        if (labirint[x+1][y] != "#") and x <rows and dest_x > x:
            x, y = pastga(x, y)
            if x ==dest_x and y ==dest_y:
                return res  

        if (labirint[x-1][y] != "#" ) and  x-1 != 0 and dest_x < x:
            x, y = tepaga(x, y)
            if x ==dest_x and y ==dest_y:
                return res  
        return innerchap(labirint, x, y)  

        
    # InnerRight Agar X o'ng da turgan bo'lsa ishlaydi 
    def innerright(labirint, x, y):     
        x = x
        y = y  

        if  (labirint[x][y+1]!='#') and y < columns and y+1 <= dest_y:
            x, y = o_ng(x, y)
            if x ==dest_x and y ==dest_y:
                return res

        elif (labirint[x][y-1] != "#") and y-1 != 0 and y-1 > dest_y:
            x, y = chap(x, y)
            if x ==dest_x and y ==dest_y:
                return res

        elif (labirint[x+1][y] != "#") and x <rows and x+1 <= dest_x:
            x, y = pastga(x, y)
            if x ==dest_x and y ==dest_y:
                return res
    

        elif (labirint[x-1][y] != "#") and  x-1 != 0:
            x, y = tepaga(x, y)
            if x ==dest_x and y ==dest_y:
                return res
        

        elif (labirint[x+1][y] != "#") and x <rows:
            x, y = pastga(x, y)
            if x ==dest_x and y ==dest_y:
                return res

        return innerright(labirint, x, y)                       
                    
             
    if tomon == "chap":        
        return innerchap(labirint, a, b)
    elif tomon =="o'ng":
        return innerright(labirint, a, b)

# Funksiyani chaqirish               
print(solve_labirint(lb))
