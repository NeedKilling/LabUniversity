def convert_types(data):
    newData = []
    for item in data: 
        
        if(isinstance(item,str)):
            try:
                newData.append(int(item))
            except:
                newData.append(item)
        else:
            newData.append(str(item))
            
    return newData
        

                

print(convert_types([1, "2", "hello", 3.5]))
print()