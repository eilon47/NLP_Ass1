
SPECIALS = ["^Xy", "^XY", "^Xing", "^Xed", "^Xs","^X's"]

def add_count_to_dict(count_dict, key):
    if key not in count_dict.keys():
        count_dict[key] = 1
    else:
        count_dict[key] += 1


def is_speciel_signature(word):
    i = 0;
    return SPECIALS[i]


def create_estimates(file_name, q_file, e_file):
    fd = open(file_name, 'r')
    data = fd.read()
    fd.close()
    count_dict_q = dict()
    count_dict_q_2 = dict()
    count_dict_q_3 = dict()
    count_dict_e = dict()
    spaces_split_data = []
    for l in data.splitlines():
        spaces_split_data += l.split(' ')
    for i in range(len(spaces_split_data)):
        couple1 = spaces_split_data[i]
        word, t1 = couple1.split('/')
        add_count_to_dict(count_dict_e, (word, t1))
        add_count_to_dict(count_dict_q, t1)
        if i+1 < len(spaces_split_data):
            couple2 = spaces_split_data[i+1]
            t2 = couple2.split('/')[1]
            t2 = (t1, t2)
            add_count_to_dict(count_dict_q_2, t2)
            if i+2 < len(spaces_split_data):
                couple3 = spaces_split_data[i+2]
                t3 = couple3.split('/')[1]
                t3 = (t2[0], t2[1], t3)
                add_count_to_dict(count_dict_q_3, t3)
    write_estimates_to_file([count_dict_q, count_dict_q_2, count_dict_q_3], q_file)
    write_estimates_to_file([count_dict_e], e_file)


def write_estimates_to_file(dictionaries, filename):
    fd = open(filename, 'w')
    for dictionary in dictionaries:
        for k, v in dictionary.items():
            if type(k) is tuple:
                k = " ".join(k)
            fd.write("{}\t{}\n".format(k, str(v)))
    fd.close()
