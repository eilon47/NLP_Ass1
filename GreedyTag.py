import sys
import MLETrain as mle
import numpy as np


S_TAGS = 'START'
number_of_words = 0


def get_num_of_words(w_dict):
    global number_of_words
    if number_of_words is 0:
        for word in w_dict:
            number_of_words += int(w_dict[word])
    return number_of_words


def tag_sentence(line, q_dict,e_dict,w_dict,t_dict,unk_dict):
    ppt, pt = S_TAGS, S_TAGS
    result_sentence = []
    words = line.split(" ")
    first_word = words[0]
    if first_word not in w_dict.keys() and first_word.lower() in w_dict.keys():
        words[0] = words[0].lower()
    for word in words:
        word_tag = tag_word(ppt, pt, word, q_dict, e_dict, w_dict, t_dict, unk_dict)
        result_sentence.append("{}/{}".format(word, word_tag))
        ppt = pt
        pt = word_tag
    t = result_sentence[0]
    result_sentence[0] = t.title()
    return " ".join(result_sentence)


def tag_word(prev_prev_tag,prev_tag, word,q_dict,e_dict, w_dict,t_dict,unk_dict):
    max_yi = 0
    arg_max = ''
    num_of_words = get_num_of_words(w_dict)
    #in case we already know the word
    try:
        count = w_dict[word]
        for yi in t_dict.keys():
            temp_q = mle.get_q(q_dict,prev_prev_tag,prev_tag,yi,num_of_words)
            temp_e = mle.get_e(word,yi,q_dict,e_dict,unk_dict)
            if temp_e*temp_q > max_yi:
                max_yi = temp_e*temp_q
                arg_max = yi
    except KeyError:
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
    data = data.splitlines()
    fd.close()
    fd = open(out_file,'w')
    for line in data:
        result = tag_sentence(line, q_dict,e_dict,w_dict,t_dict,unk_dict)
        fd.write(result + '\n')
        print result


if __name__ == '__main__':
    if len(sys.argv) is not 6:
        exit(-1)
    input, qmle, emle, output, extra = sys.argv[1:]
    print "gets dictionaries"
    q_dict, e_dict, words_dict,tags_dict, unk_dict = mle.create_dictionaries(qmle, emle)
    print "tag the input file"
    tag_file(input, output, q_dict, e_dict, words_dict, tags_dict, unk_dict)
    print "Done!!!"
