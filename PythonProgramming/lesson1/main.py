# with open("numbers.txt", "r") as numbersFile:
#     #numbers = numbersFile.read()
#     sum = 0
#     for line in numbersFile:
#         for number in line.strip().split(" "):
#             sum += int(number) 

#     print(f"\nSum: {sum}\n")


surname = []

with open("users.txt","r",encoding = "utf-8") as file:
    for line in file:
        #line = line.strip()
        surname.append(line)
        
    surname = sorted(surname)

    i = 0
    # for user in surname:
    #     i+=1
    #     if user.strip() == "Петрова Мария":
    #         print(f"\nuser: {user}  I: = {i}\n")
    #         break
    for  i,user in enumerate(surname,1):
        if user.strip() == "Петрова Мария":
            print(i)
            break
    print(surname)
    
    with open("sorted_user.txt", 'w') as sortedUser:
        file.write(surname)



        























        # 1 кол - во физ.лиц и юр. лиц
        # 2 кол - во лиц которые вышли из списка
        # 3 кол - во лиц по годам