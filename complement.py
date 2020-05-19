def pcn2op(pcn_listfn,nv):
    
    f = open('output.txt',"w")
    f.write(str(nv))
    f.write('\n')
    f.write(str(len(pcn_listfn)))
    f.write('\n')
    for pcn in pcn_listfn:
        oplist = []
        x = pcn.count([1,1])
        oplist.append(str(nv-x))
        for index,var in enumerate(pcn):
            if (var == [0,1]):
                oplist.append(str(index+1))
            elif (var == [1,0]):
                oplist.append(str(-index-1))
            
        for i in oplist:
            f.write(i)
            f.write(' ')
        f.write('\n')
    f.close()

def ip2pcn(cube_list,nv,nc):
#CREATE PCN LIST
    pcn_listfn = []
    var_listfn = set()
    for i in range(nc):
        x = cube_list[i][0]
        pcn = [[1,1]] * nv
        if(x != 0):
            for j in range(x):
                v = cube_list[i][j+1]
                var_listfn.add(abs(v))
                if(v > 0):
                    pcn[v-1] = [0,1]
                else:
                    pcn[-v-1] = [1,0]


            pcn_listfn.append(pcn)
            
    return(pcn_listfn,var_listfn)


boolean_dict = {'-':[1, 1], '0':[1, 0], '1':[0, 1]}
reversed_boolean_dict = {(1, 1):'-', (1, 0):'0', (0, 1):'1'}

def DeMorgan_Laws(pcn_listfn, var_num):
    result = []
    for index, boolean in enumerate(pcn_listfn[0]):
        if boolean == [1, 1]: pass
        elif boolean == [1, 0]:
            result.append([[0, 1] if i == index else [1, 1] for i in range(var_num)])
        else:
            result.append([[1, 0] if i == index else [1, 1] for i in range(var_num)])
    return result

def binate_var(pcn_listfn, var_num):
    True_dict = {i:0 for i in range(1,var_num+1)}
    Complement_dict = {i:0 for i in range(1,var_num+1)}
    for cube in pcn_listfn:
        for index, value in enumerate(cube):
            if value == [0, 1]: True_dict[index+1] += 1
            elif value == [1, 0]: Complement_dict[index+1] += 1
            else:   pass
    binate_list = [i for i in range(1,var_num+1) if True_dict[i] and Complement_dict[i]]
    if binate_list:
        # Pick the binate variable in the most cubes
        biggest_appearance = max(True_dict[i] + Complement_dict[i] for i in binate_list)
        binate_list_most_cubes = [i for i in binate_list if True_dict[i] + Complement_dict[i] == biggest_appearance]
        # Break ties with the smallest abs(T-C), and then with the smallest variable index
        return min(binate_list_most_cubes, key=lambda x: abs(True_dict[x] - Complement_dict[x]))
    else:
        # Pick the unate variable in the most cubes
        biggest_appearance = max(True_dict[i] + Complement_dict[i] for i in range(1,var_num+1))
        unate_list_most_cubes = [i for i in range(1,var_num+1) if True_dict[i] + Complement_dict[i] == biggest_appearance]
        # Break ties with smallest variable index
        return min(unate_list_most_cubes)

def positiveCofactor(pcn_listfn, x):
    result = []
    for cube in pcn_listfn:
        if cube[x-1] == [1, 1]: result.append(cube)
        elif cube[x-1] == [1, 0]: pass
        else:   result.append([[1, 1] if index == x-1 else val for index, val in enumerate(cube)])
    return result

def negativeCofactor(pcn_listfn, x):
    result = []
    for cube in pcn_listfn:
        if cube[x-1] == [1, 1]: result.append(cube)
        elif cube[x-1] == [0, 1]: pass
        else:   result.append([[1, 1] if index == x-1 else val for index, val in enumerate(cube)])
    return result

def and_x(x,pcn_listfn):
	
	
	for pcn in pcn_listfn:
			
		if(x>0):
			pcn[x-1] = [0,1]
		else:
			pcn[-x-1] = [1,0]
			
	return(pcn_listfn)

def and_x_bar(x, cubelist):
    for cube in cubelist:
        cube[x-1] = [1, 0]
    return cubelist

def Complement(pcn_listfn, var_num):
    # Empty cube list
    if not pcn_listfn:
        return [[[1, 1] for _ in range(var_num)]]
    # Cube list contains All-Don't-Cares Cube
    elif [[1, 1] for _ in range(var_num)] in pcn_listfn:
        return []
    # Cube list contains just one cube
    elif len(pcn_listfn) == 1:
        return DeMorgan_Laws(pcn_listfn, var_num)
    else:
        # Do recursion
        x = binate_var(pcn_listfn, var_num)
        p = Complement(positiveCofactor(pcn_listfn, x), var_num)
        n = Complement(negativeCofactor(pcn_listfn, x), var_num)
        return and_x(x, p) + and_x(-x, n)

def main():
    f = open(r"part1.pcn","r")#input file
    nv= int(f.readline())  #no of variables
    nc = int(int(f.readline())) #no of cubes

    #input cubes as list
    cube_list = []
    for i in range(nc):
        cube = f.readline().split()
        map_object = map(int, cube)
        cube = list(map_object)
        cube_list.append(cube)


    print(cube_list,'\n')

    pcn_list,var_list = ip2pcn(cube_list,nv,nc)
    output_f = Complement(pcn_list, nv)
    print (nv)
    for cube in output_f:
        print (''.join([reversed_boolean_dict[tuple(i)] for i in cube]))
    pcn2op(output_f,nv)
if __name__ == '__main__':
    main()
