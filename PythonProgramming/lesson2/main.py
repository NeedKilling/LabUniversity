        # 1 кол - во физ.лиц и юр. лиц
        # 2 кол - во лиц которые вышли из списка
        # 3 кол - во лиц по годам
import csv

    


def totalPerson():
    with open("ino_list.csv","r",newline="",encoding='utf-8') as file:
        ino = csv.DictReader(file)
        totalFiz = 0
        totalYr = 0
        for row in ino:
            if(row["Тип иностранного агента"] == "Физические лица"):
                totalFiz+=1
            elif(row["Тип иностранного агента"] == "Юридические лица"):  
                totalYr+=1
    return print(f"Физические лица = {totalFiz}, Юридические лица = {totalYr}")



def inoExit():
    with open("ino_list.csv","r",newline="",encoding='utf-8') as file:
        ino = csv.DictReader(file)
        totalExit = 0
        for row in ino:
            if(row["Дата принятия Минюстом России решения об исключении из реестра (при наличии)"]):
                totalExit += 1
        
    return print(f"кол-во лиц которые вышли из списка = {totalExit}")
    
def inoForYear():
    with open("ino_list.csv","r",newline="",encoding='utf-8') as file:
        ino = csv.DictReader(file)
        i = 0
        for row in ino:
            print(row["Дата принятия Минюстом России решения о включении в реестр"][-4:])
            i+=1
        print(i)    

totalPerson()   
inoExit()
inoForYear()
    