import sys
import MLETrain as mle
import numpy as np


S_TAGS = ['START']
tags = ['a','b','c']

def get_num_of_words(w_dict):
    num_of_words = 0
    for word in w_dict:
        num_of_words += int(w_dict[word])
    return num_of_words

def tag_word(prev_prev_tag,prev_tag, word,q_dict,e_dict, w_dict,t_dict,unk_dict):
    max_yi = 0
    arg_max = ''
    num_of_words = get_num_of_words(w_dict)
    #in case we already know the word
    if word in w_dict.keys():
        for yi in t_dict.keys():
            if str(prev_prev_tag+" "+prev_tag+" "+yi) not in q_dict.keys():
                continue

            # add log
            temp_q = mle.getQ(q_dict,prev_prev_tag,prev_tag,yi,num_of_words)
            temp_e = mle.getE(word,yi,q_dict,e_dict,unk_dict)
            if(temp_e+temp_q) > max_yi:
                max_yi = temp_e+temp_q
                arg_max = yi
    else:
        t = mle.get_special_signature(word)
        if t is None:
            return "UNK"
        # possible_tags_keys = [unk for unk in unk_dict.keys() if t in unk]
        max_key, max_val = "", 0
        for key, counter in unk_dict.items():
            if t in key and counter > max_val:
                max_key, max_val = key, counter
        arg_max = max_key[-1]
    return arg_max

def tag_file(in_file, out_file, q_dict, e_dict, w_dict, t_dict, unk_dict):
    fd = open(in_file)
    data = fd.read()
    fd.close()
    spaces_split_data = []
    fd = open(out_file,'w')
    for l in data.splitlines():
        spaces_split_data += l.split(' ')
    p_p_t = S_TAGS[0]
    p_t = S_TAGS[0]
    for word in spaces_split_data:
        if word == "and":
            print ' '
        t = tag_word(p_p_t,p_t,word,q_dict,e_dict,w_dict,t_dict,unk_dict)
        p_p_t = p_t
        p_t = t
        fd.write(str(word+'/'+t+' '))
        print str(word+'/'+t+' ')


if __name__ == '__main__':
    if len(sys.argv) is not 6:
        exit(-1)
    input, qmle, emle, output, extra = sys.argv[1:]
    q_dict, e_dict, words_dict,tags_dict, unk_dict = mle.create_dictionaries(qmle, emle)
    tag_file(input, output, q_dict, e_dict, words_dict, tags_dict, unk_dict)
    print "Done!!!"
