from __future__ import division

import os
import sys


l1, l2, l3 = 1.0/2, 1.0/3, 1.0/6


class Specials:
    def __init__(self):
        pass

    UNK = "UNK"
    Xy = "^Xy"
    XY = "^XY"
    Xing = "^Xing"
    Xed = "^Xed"
    X_s = "^X's"
    Xs = "^Xs"
    xy = "^xy"
    NUM = "NUM"


def create_dictionaries(q_mle, e_mle):
    q_dict = {}
    e_dict = {}
    words_dict = {}
    tags_dict = {}
    unk_dict = {}
    # creating the q dictionary
    fd_q = open(q_mle, 'r')
    for line in fd_q:
        line = line.strip()
        if line == "":
            continue
        key, counter = line.split('\t')
        #if counter.strip().isnumeric():
        q_dict[key] = int(counter.strip())
    # creating the e dictionary
    fd_e = open(e_mle, 'r')
    for line in fd_e:
        line = line.strip()
        if line == "":
            continue
        # gets key val as (w,t)->counter
        key, counter = line.split('\t')
        # gets w,t
        word,tag = key.split(' ')
        # if counter.strip().isnumeric():
        e_dict[key] = int(counter.strip())

        # updating the UNK dictionary
        signature = get_special_signature(word)
        if signature is not None:
            unk = (signature,tag)
            add_count_to_dict(unk_dict,unk)

        # updating the words and tags dictionary
        add_count_to_dict(words_dict,word)
        add_count_to_dict(tags_dict,tag)

    fd_e.close()
    fd_q.close()
    return q_dict, e_dict, words_dict,tags_dict,unk_dict


def check_dict(tag1,tag2,tag3,q_dict):
    if tag3 == 0:
        if str(tag1 + " " + tag2) in q_dict.keys():
            return True
        else:
            return False
    if str(tag1+" "+tag2+" "+tag3) in q_dict.keys():
        return True
    return False


def get_q(q_dict,tag1, tag2, tag3, num_words):
    global l1, l2, l3
    c = float(q_dict[tag3])
    b, ab, bc, abc = [1.0] * 4
    if tag1 == "START":
        if tag1 == "START" and tag2 == "START":
            return l3*(c/num_words)
        bc = float(q_dict[" ".join([tag2, tag3]).strip()])
        b = float(q_dict[tag2])
        return l2*(bc/b) + l3* (c/num_words)
    abc_t, ab_t, bc_t, b_t = get_combinations(tag1, tag2, tag3)
    if abc_t in q_dict.keys():
        abc = float(q_dict[abc_t])
    if ab_t in q_dict.keys():
        ab = float(q_dict[ab_t])
    if bc_t in q_dict.keys():
        bc = float(q_dict[bc_t])
    if b_t in q_dict.keys:
        b = float(q_dict[b_t])
    q = l1*(abc/ab) + l2*(bc/b) + l3* (c/num_words)
    return q


def get_combinations(tag1, tag2, tag3):
    abc = " ".join([tag1, tag2, tag3])
    bc = " ".join([tag2, tag3])
    ab = " ".join([tag1, tag2])
    b = tag2
    return abc, ab, bc, b


def get_e(word, tag, q_dict, e_dict,unk_dict):
    key = word + " " + tag
    if key not in e_dict.keys():
        signature = get_special_signature(word)
        if (signature,tag) in unk_dict.keys():
            count_word_tag = unk_dict[signature,tag]
        else:
            count_word_tag = 1
    else:
        count_word_tag = e_dict[key]
    count_tag = q_dict[tag]
    return count_word_tag / count_tag


def add_count_to_dict(count_dict, key):
    if key not in count_dict.keys():
        count_dict[key] = 1
    else:
        count_dict[key] += 1


def get_special_signature(word):
    if check_if_numeric(word):
        return Specials.NUM
    if len(word) is 1:
        return Specials.xy
    word_as_letters = list(word)

    #1 - prefix
    if word_as_letters[0].isupper():
        if word_as_letters[1].isupper():
            return Specials.XY
        else:
            return Specials.Xy

    #2 - postfix
    elif str(word_as_letters[-3:-1]) == "ing":
        return Specials.Xing
    elif str(word_as_letters[-2:-1]) == "ed":
        return Specials.Xed
    elif str(word_as_letters[-2:-1]) == "'s":
        return  Specials.X_s
    elif word_as_letters[-1] == 's':
        return Specials.Xs
    elif word_as_letters[0].islower() and word_as_letters[1].islower():
        return Specials.xy
    return None



def check_if_numeric(word):
    temp = word.strip().replace(",","").replace(".","").replace("-","")
    try:
        temp = float(temp)
        return True
    except ValueError:
        return False




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
        word, t1 = split_to_word_tag(couple1)
        add_count_to_dict(count_dict_e, (word, t1))
        add_count_to_dict(count_dict_q, t1)
        if i+1 < len(spaces_split_data):
            couple2 = spaces_split_data[i+1]
            w, t = split_to_word_tag(couple2)
            t2 = (t1, t)
            add_count_to_dict(count_dict_q_2, t2)
            if i+2 < len(spaces_split_data):
                couple3 = spaces_split_data[i+2]
                w, t3 = split_to_word_tag(couple3)
                t3 = (t2[0], t2[1], t3)
                add_count_to_dict(count_dict_q_3, t3)
                print t3, i

    write_estimates_to_file([count_dict_q, count_dict_q_2, count_dict_q_3], q_file)
    write_estimates_to_file([count_dict_e], e_file)


def split_to_word_tag(word):
    index = word.rfind('/')
    tag = word[index+1:]
    word = word[:index]
    return word, tag


def write_estimates_to_file(dictionaries, filename):
    fd = open(filename, 'w')
    for dictionary in dictionaries:
        for k, v in dictionary.items():
            if type(k) is tuple:
                k = " ".join(k)
            fd.write("{}\t{}\n".format(k, str(v)))
    fd.close()


if __name__ == '__main__':
    if len(sys.argv) is not 4:
        exit(-1)
    input_file, qmle, emle = sys.argv[1:]
    create_estimates(input_file, qmle, emle)