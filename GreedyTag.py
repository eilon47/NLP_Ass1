import sys
import MLETrain as mle
import numpy as np

S_TAGS = ['START']
tags = ['a','b','c']

def tag_word(prev_prev_tag,prev_tag, word,q_dict,e_dict, w_dict,t_dict):
    max_yi = 0
    arg_max = ''
    #add how to calculate q(y1|start,start)
    if word in w_dict.keys():
        for yi in t_dict.key():
            temp_q = np.log(mle.getQ(q_dict,prev_prev_tag,prev_tag,yi))
            temp_e = np.log(mle.getE(word,yi,q_dict,e_dict))
            if(temp_e+temp_q) > max_yi:
                max_yi = temp_e+temp_q
                arg_max = yi
    else:
        # add tagging UNK words
    return arg_max

def tag_sencence(in_file,out_file,q_dict,e_dict,w_dict,t_dict):
    fd = open(in_file)
    data = fd.read()
    fd.close()
    spaces_split_data = []
    for l in data.splitlines():
        spaces_split_data += l.split(' ')
        p_p_t = S_TAGS[0]
        p_t = S_TAGS[0]
        for word in spaces_split_data:
            t = tag_word(p_p_t,p_t,word,q_dict,e_dict,w_dict,t_dict)
            p_p_t = p_t
            p_t = t


if __name__ == '__main__':
    if len(sys.argv) != 6:
        exit()
    in_file = sys.argv[1]
    q_mle = sys.argv[2]
    e_mle = sys.argv[3]
    out_file = sys.argv[4]
    extra_file = sys.argv[5]

    mle.create_estimates(in_file, q_mle, e_mle)
    q_dict, e_dict, words_dict,tags_dict = mle.create_dictionaries(q_mle, e_mle)


