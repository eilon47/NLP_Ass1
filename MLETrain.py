from __future__ import division
from collections import Counter
import os
import sys


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
        q_dict[key.strip()] = int(counter.strip())
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
        word = word.strip()
        tag = tag.strip()
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
    l1, l2, l3 = 1.0 / 2, 1.0 / 3, 1.0 / 6
    b, ab, bc, abc = [1.0] * 4
    c = q_dict[tag3]
    abc_t, ab_t, bc_t, b_t = get_combinations(tag1, tag2, tag3)
    if abc_t in q_dict.keys():
        abc = float(q_dict[abc_t])
    else:
        l1 = 0
    if ab_t in q_dict.keys():
        ab = float(q_dict[ab_t])
    else:
        l1 = 0
    if bc_t in q_dict.keys():
        bc = float(q_dict[bc_t])
    else:
        l2 = 0
    if b_t in q_dict.keys():
        b = float(q_dict[b_t])
    else:
        l2 = 0
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
    data = fd.readlines()
    fd.close()
    count_dict_q = Counter()
    count_dict_q_2 = Counter()
    count_dict_q_3 = Counter()
    count_dict_e = Counter()
    j = 0
    for line in data:
        words = line.strip().split(" ")
        pt, ppt = "TEMP", "TEMP"
        for word in words:
            word, t1 = split_to_word_tag(word)
            count_dict_e[word+" "+ t1] += 1
            count_dict_q[t1] += 1
            count_dict_q_2[t1+" "+pt] += 1
            count_dict_q_3[t1+" "+ pt +" "+ ppt] += 1
            ppt = pt
            pt = t1
        print j
        j += 1
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
            fd.write("{}\t{}\n".format(k, str(v)))
            print "{}\t{}\n".format(k, str(v))
    fd.close()


if __name__ == '__main__':
    if len(sys.argv) is not 4:
        exit(-1)
    input_file, qmle, emle = sys.argv[1:]
    create_estimates(input_file, qmle, emle)