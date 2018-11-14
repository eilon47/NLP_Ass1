import mle
import sys


def create_dictionaries(q_mle, e_mle):
    q_dict = {}
    e_dict = {}
    words_dict = {}
    tags_dict = {}
    fd_q = open(q_mle, 'r')
    for line in fd_q:
        line = line.strip()
        if line == "":
            continue
        key, counter = line.split('\t')
        #if counter.strip().isnumeric():
        q_dict[key] = int(counter.strip())
    fd_e = open(e_mle, 'r')
    for line in fd_e:
        line = line.strip()
        if line == "":
            continue
        key, counter = line.split('\t')
        #if counter.strip().isnumeric():
        e_dict[key] = int(counter.strip())
        words_dict[key[0]] += 1
        tags_dict[key[1]] += 1
    return q_dict, e_dict, words_dict,tags_dict


def getE(word, tag, q_dict, e_dict):
    key = word + " " + tag
    count_word_tag = e_dict[key]
    count_tag = q_dict[tag]
    return count_word_tag / count_tag


def getQ(q_dict,tag1, tag2, tag3, num_words):
    abc = q_dict[" ".join([tag1, tag2, tag3])]
    ab = q_dict[" ".join([tag1, tag2])]
    bc = q_dict[" ".join([tag2, tag3])]
    c = q_dict[tag3]
    b = q_dict[tag2]
    l1, l2, l3 = 1/2, 1/3, 1/6
    q = l1*(abc/ab) + l2*(bc/b) + l3* (c/num_words)
    return q




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



if __name__ == '__main__':
    if len(sys.argv) != 4:
        exit()
    file_name = sys.argv[1]
    q_mle = sys.argv[2]
    e_mle = sys.argv[3]

    create_estimates(file_name,q_mle, e_mle)
    q_dict, e_dict = create_dictionaries(q_mle, e_mle)
    print ' '



