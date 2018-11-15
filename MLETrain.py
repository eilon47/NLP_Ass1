from __future__ import division
import mle
import sys

SPECIALS = ["UNK","^Xy", "^XY", "^Xing", "^Xed","^X's", "^Xs","xy"]

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
        if word == "and":
            print ' '
        # if counter.strip().isnumeric():
        e_dict[key] = int(counter.strip())

        # updating the UNK dictionary
        signature = get_speciel_signature(word)
        if signature is not None:
            unk = (signature,tag)
            add_count_to_dict(unk_dict,unk)

        # updating the words and tags dictionary
        add_count_to_dict(words_dict,word)
        add_count_to_dict(tags_dict,tag)

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

def getQ(q_dict,tag1, tag2, tag3, num_words):
    if tag1 == "START":
        if tag1 == "START" and tag2 == "START":
            return q_dict[tag3]/num_words
        bc = q_dict[" ".join([tag2, tag3]).strip()]
        c = q_dict[tag3]
        b = q_dict[tag2]
        return (1/3)*(bc/b) + (1/6)* (c/num_words)
    if check_dict(tag1,tag2,tag3,q_dict):
        abc = q_dict[" ".join([tag1, tag2, tag3]).strip()]
    else:
        abc = 1
    if check_dict(tag1, tag2, 0, q_dict):
        ab = q_dict[" ".join([tag1, tag2]).strip()]
    else:
        ab = 1
    if check_dict(tag2,tag3,0,q_dict):
        bc = q_dict[" ".join([tag2, tag3]).strip()]
    else:
        bc = 1
    if tag3 in q_dict.keys() and tag2 in q_dict.keys():
        c = q_dict[tag3]
        b = q_dict[tag2]
    else:
        b = 1
        c = 1
    l1 = 1/2
    l2 = 1/3
    l3 = 1/6
    q = l1*(abc/ab) + l2*(bc/b) + l3* (c/num_words)
    return q

def getE(word, tag, q_dict, e_dict,unk_dict):
    key = word + " " + tag
    if key not in e_dict.keys():
        signature = get_speciel_signature(word)
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


def get_speciel_signature(word):
    if len(word) is 1:
        return SPECIALS[7]
    word_as_letters = list(word)

    #1 - prefix
    if word_as_letters[0].isupper():
        if word_as_letters[1].isupper():
            return SPECIALS[2]
        else:
            return SPECIALS[1]

    #2 - postfix
    elif str(word_as_letters[-3:-1]) == "ing":
        return SPECIALS[3]
    elif str(word_as_letters[-2:-1]) == "ed":
        return SPECIALS[4]
    elif str(word_as_letters[-2:-1]) == "'s":
        return  SPECIALS[5]
    elif word_as_letters[-1] == 's':
        return SPECIALS[6]
    elif word_as_letters[0].islower() and word_as_letters[1].islower():
        return SPECIALS[7]
    return None


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
            t = couple2.split('/')[1]
            t2 = (t1, t)
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
    s = " ".join(["", "", "dsjk"])
    print s


    if len(sys.argv) != 4:
        exit()
    file_name = sys.argv[1]
    q_mle = sys.argv[2]
    e_mle = sys.argv[3]

    create_estimates(file_name,q_mle, e_mle)
    q_dict, e_dict, w,t = create_dictionaries(q_mle, e_mle)
    print ' '



