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


def add_count_to_dict(count_dict, key):
    if key not in count_dict.keys():
        count_dict[key] = 1
    else:
        count_dict[key] += 1

def create_q_estimate(file_name):
    fd = open(file_name, 'r')
    data = fd.read()
    fd.close()
    count_dict = dict()
    spaces_split_data = []
    for l in data.splitlines():
        spaces_split_data += l.split(' ')
    for i in range(len(spaces_split_data)):
        couple1 = spaces_split_data[i]
        t1 = couple1.split('/')[1]
        add_count_to_dict(count_dict, t1)
        if i+1 < len(spaces_split_data):
            couple2 = spaces_split_data[i+1]
            t2 = couple2.split('/')[1]
            t2 = (t1, t2)
            add_count_to_dict(count_dict, t2)
            if i+2 < len(spaces_split_data):
                couple3 = spaces_split_data[i+2]
                t3 = couple3.split('/')[1]
                t3 = (t2[0], t2[1], t3)
                add_count_to_dict(count_dict, t3)
    write_estimates_to_file(count_dict)

def write_estimates_to_file(dictionary):
    file_name = 'q.mle.txt'
    fd = open(file_name, 'w')
    for k, v in dictionary.items():
        if type(k) is tuple:
            k = " ".join(k)
        fd.write("{}\t{}\n".format(k, str(v)))
    fd.close()

if __name__ == '__main__':
    create_q_estimate('hmm_try')