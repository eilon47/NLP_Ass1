def create_e_estimate(file_name,output_file):
    fd = open(file_name,'r')
    data = fd.read()
    count_dic = {}
    spaces_split_data = []
    for line in data.splitlines():
        spaces_split_data += line.split(' ')
    fd.close()
    for d in spaces_split_data:
        event = d.split('/')
        t = tuple(event)
        if t not in count_dic.keys():
            count_dic[t] = 1
        else:
            count_dic[t] += 1
    print count_dic

    tags_dic = {}
    for k in count_dic.keys():
        if k[1] not in tags_dic.keys():
            tags_dic[k[1]] = 1
        else:
            tags_dic[k[1]] += 1
    print tags_dic

    fd = open(output_file,'w')
    for key in count_dic:
        fd.write(key[0]+" "+key[1]+"\t"+str(count_dic[key])+"\n")
    return count_dic,tags_dic

def estimate_e(count_dic,tag_dic):
    e = {}
    for event in count_dic:
        e[event] = count_dic[event]/tag_dic[event[1]]
    return e

if __name__ == '__main__':
    count,tags = create_e_estimate('C:\\Users\\green\\Desktop\\hmm.txt','e.mle')
    estimate = estimate_e(count,tags)









