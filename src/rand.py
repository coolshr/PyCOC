width = 10
height = 15
map = []
for i in range(height ):
            map.append([])
            if i >=0 and i<= 2:
                for j in range(width ):
                    map[i].append(' ')                
            elif i == 3 or i == height -1:
                for j in range(width ):
                    if j >=0 and j <= 2:
                        map[i].append(' ')
                    elif j <= width:
                        map[i].append('W')
            else:
                for j in range(width ):
                    if j >= 0 and j <= 2:
                        map[i].append(' ')
                    elif j == 3  or j == width-1:
                        map[i].append('W' )
                    else:
                        map[i].append(' ')  

for i in map:
    for j in i:
        print(j,end='')
    print() 