import mle
import sys


def create_dictionaries(q_mle, e_mle):
    q_dict = {}
    e_dict = {}
    fd_q = open(q_mle, 'r')
    for line in fd_q:
        line = line.strip()
        if line == "":
            continue
        key, counter = line.split('\t')
        if counter.strip().isnumeric():
            q_dict[key] = int(counter.strip())
    fd_e = open(e_mle, 'r')
    for line in fd_e:
        line = line.strip()
        if line == "":
            continue
        key, counter = line.split('\t')
        if counter.strip().isnumeric():
            e_dict[key] = int(counter.strip())
    return q_dict, e_dict


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



if __name__ == '__main__':
    if len(sys.argv) != 4:
        exit()
    file_name = sys.argv[1]
    e_mle = sys.argv[2]
    q_mle = sys.argv[3]

    mle.create_estimates(file_name,q_mle, e_mle)
    q_dict, e_dict = create_dictionaries(q_mle, e_mle)




