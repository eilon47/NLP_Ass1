import sys
import MLETrain as mle

S_TAGS = ['START']
tags = ['a','b','c']

def tag_word(prev_prev_word,prev_word, word,q_dict,e_dict):
    max_yi = 0
    for yi in tags:
        temp_q = mle.getQ(q_dict,word,prev_prev_word,prev_word)
        temp_e = mle.getE(word,yi,q_dict,e_dict)







if __name__ == '__main__':
    if len(sys.argv) != 6:
        exit()
    in_file = sys.argv[1]
    q_mle = sys.argv[2]
    e_mle = sys.argv[3]
    out_file = sys.argv[4]
    extra_file = sys.argv[5]

    mle.create_estimates(in_file, q_mle, e_mle)
    q_dict, e_dict = mle.create_dictionaries(q_mle, e_mle)


