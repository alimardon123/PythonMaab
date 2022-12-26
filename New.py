

lb = [            
                    "P#----",
                    "------",
                    "---#--",
                    "----#-",
                    "-###X-",
                    "------"]



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
    try:
        coor =  [( labirint.index(a),a.index(b)) for a in labirint for b in a if b =="X"]
        dest_x, dest_y = coor[0]

        start = [(labirint.index(a), a.index(b)) for a in labirint for b in a if b == "P"] 
        a, b = start[0]
        old_a = a
        old_b = b
        tomon = "chap" if b > dest_y else "o'ng"
    except IndexError:
        return "Futbolchi yoki Maqsad Listda yo'q. Ularni kiriting."

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
    def innerchap(labirint, x, y, old_x, old_y):
        try:
            x = x
            y = y
            old_x = old_x
            old_y = old_y

            if (labirint[x][y-1] !='#') and y-1 != 0 and y > dest_y :
                old_x = x
                old_y = y
                x, y = chap(x, y)
                if x ==dest_x and y ==dest_y:
                    return res
                    
            if  (labirint[x][y+1] !='#') and y < columns and  y < dest_y :
                old_x = x
                old_y = y
                x, y = o_ng(x, y)
                if x ==dest_x and y ==dest_y:
                    return res   
                
            if (labirint[x+1][y] != "#") and x <rows and dest_x > x:
                old_x = x
                old_y = y
                x, y = pastga(x, y)
                if x ==dest_x and y ==dest_y:
                    return res  
            if (labirint[x-1][y] != "#" ) and  x-1 != 0 and dest_x < x:
                old_x = x
                old_y = y
                x, y = tepaga(x, y)
                if x ==dest_x and y ==dest_y:
                    return res  
            return innerchap(labirint, x, y, old_x, old_y)  

        except RecursionError:
            return "Hamma yo'llar yopiq. Maqsadga yetib bo'lmaydi." 

    # InnerRight Agar X o'ng da turgan bo'lsa ishlaydi 
    def innerright(labirint, x, y, old_x, old_y):     
        x = x
        y = y
        old_x = old_x
        old_y = old_y

        try:
            if (labirint[x][y+1]!='#') and y < columns and y+1 <= dest_y and (y+1 != old_y):  
                while (labirint[x][y+1]!='#') and y < columns and y+1 <= dest_y:
                        old_x = x
                        old_y = y
                        x, y = o_ng(x, y)
                        if x ==dest_x and y ==dest_y:
                            return res

            elif (labirint[x][y-1] != "#") and y-1 != 0 and   y-1 != old_y and (y-1 > dest_y or  labirint[x+1][y-1] !="#" or (x == dest_x and (labirint[x][y+1] =="#" or (labirint[x+1][y] == "#" and labirint[x-1][y] == "#" and y+1 == old_y)))):
                while (labirint[x][y-1] != "#") and y-1 != 0 and y-1 != old_y and  (y-1 > dest_y or labirint[x+1][y-1] !="#" or (x == dest_x and (labirint[x][y+1] =="#" or (labirint[x+1][y] == "#" and labirint[x-1][y] == "#" and y+1 == old_y)))):
                    old_x = x
                    old_y = y
                    x, y = chap(x, y)
                    if x ==dest_x and y ==dest_y:
                        return res

            elif (labirint[x+1][y] != "#") and x <rows and x+1 <= dest_x and labirint[x+1][y+1] != "#":
                while (labirint[x+1][y] != "#") and x <rows and x+1 <= dest_x :
                    old_x = x
                    old_y = y
                    x, y = pastga(x, y)
                    if x ==dest_x and y ==dest_y:
                        return res
                    if labirint[x][y+1] != "#" and x+1 ==old_x :
                        break

            elif (labirint[x-1][y] != "#") and  x-1 != 0  and (labirint[x+1][y] != "-" ):
                while (labirint[x-1][y] != "#") and  x-1 != 0 and  x-1 != old_x:
                    old_x = x
                    old_y = y
                    x, y = tepaga(x, y)
                    if x ==dest_x and y ==dest_y:
                        return res
                    if labirint[x][y+1] != "#":
                        break    

            elif (labirint[x+1][y] != "#") and x <rows :           
                while (labirint[x+1][y] != "#") and x <rows:
                    old_x = x
                    old_y = y
                    x, y = pastga(x, y)
                    if x ==dest_x and y ==dest_y:
                        return res
                    if labirint[x][y+1] != "#":
                        break        
                        
            return innerright(labirint, x, y, old_x, old_y) 

        except RecursionError:
            return "Hamma yo'llar yopiq. Maqsadga yetib bo'lmaydi."  



    if tomon == "chap":        
        return innerchap(labirint, a, b, old_a, old_b)
    elif tomon =="o'ng":
        return innerright(labirint, a, b, old_a, old_b)

# Funksiyani chaqirish               
print(solve_labirint(lb))
