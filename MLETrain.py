import hmm_tagger
import sys


if __name__ == '__main__':

    if len(sys.argv) != 4:
        exit()

    file_name = sys.argv[1]
    e_mle = sys.argv[2]
    q_mle = sys.argv[3]

    count,tag = hmm_tagger.create_e_estimate(file_name,e_mle)


