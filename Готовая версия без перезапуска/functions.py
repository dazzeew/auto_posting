def list_write_list(): #Возвращает список строк из txt
    f = open('text.txt')
    l = [line.strip() for line in f] 
    f.close()
    return l

def write_in_txt(l): #Записывает функцию 
    f = open('text.txt',"w")
    for i in range(len(l)):
        if i == 0:
            f.write(l[i])
        else:
            f.write("\n" + l[i])
    f.close()