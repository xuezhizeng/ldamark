#!/usr/bin/python
#
# Python program for running benchmarks

import sys
import os
import os.path

import subprocess

def main(args):
    #Run appropriate topic-modeler function and append time results to log file

    args.corpus = unicode(args.corpus, 'utf-8')
    args.modeler = args.modeler.lower()
    args.function = args.function.lower()

    log_file = args.log #LOG FILE columns: corpus,stage,real,user,system
    if log_file == 'log.csv':
        log_file = os.path.join(os.getcwd(), log_file)
#        print log_file

    time = '/usr/bin/time --format "%e,%U,%S"' #time function used in each test
        
    if args.modeler == 'hypershelf':
        if args.function == 'init':
            init_results = subprocess.check_output(['/usr/bin/time', '--format', '%e,%U,%S', 'vsm', 'init', args.corpus, 'hypershelf_benchmark.ini', '--name', +args.corpus, '--rebuild'], stderr=subprocess.STDOUT).split("\n")[-2]
            prep_results = subprocess.check_output(['/usr/bin/time', '--format', '%e,%U,%S', 'vsm', 'prep', 'hypershelf_benchmark.ini', '--lang', 'en', '--high', 1000000, '--low', 5], stderr=subprocess.STDOUT).split("\n")[-2]
            temp_init = init_results.strip().split(',')
            temp_prep = prep_results.strip().split(',')
            temp_init_prep = []
            for t in [0, 1, 2]:
                temp_init_prep.append(float(temp_init[t]) + float(temp_prep[t]))

            results = args.corpus+','+'init+prep'+','+str(temp_init_prep[0])+','+str(temp_init_prep[1])+','+str(temp_init_prep[2])

        elif args.function == 'train':
            train_results = subprocess.check_output(['/usr/bin/time/', '--format', '%e,%U,%S', 'vsm', 'train', 'hypershelf_benchmark.ini', '--iter', args.iterations, '--context-type', 'document', '-k', args.topics], stderr=subprocess.STDOUT).split("\n")[-2]

            results = args.corpus+','+'train'+','+train_results.strip()

        else:
            #Improper function given
            sys.exit("Function was not init or train")

    elif args.modeler == 'mallet':
        if args.function == 'init':
            init_results = subprocess.check_output(['/usr/bin/time', '--format', '%e,%U,%S', '/home/lsaggu/mallet-2.0.8RC3/bin/mallet', 'import-dir', '--input', args.corpus, '--output', 'out.mallet', '--keep-sequence', '--remove-stopwords'], stderr=subprocess.STDOUT).split("\n")[-2]

            results = args.corpus+','+'init+prep'+','+init_results.strip()
            
        elif args.function == 'train':
            train_results = subprocess.check_output(['/usr/bin/time', '--format', '%e,%U,%S', '~/mallet-2.0.8RC3/bin/mallet', 'train-topics', '--input', 'out.mallet', '--num-topics', args.topics, '--output-state', 'mallet_out.gz', '--output-topic-keys', 'mallet_out.txt', '--output-doc-topics', 'mallet_out.txt' '--num-iterations', args.iterations], stderr=subprocess.STDOUT).split("\n")[-2]


            results = args.corpus+','+'train'+','+ train_results.strip()

        else:
            #Improper function given
            sys.exit("Function was not init or train")

    else:
        #Improper modeler
        sys.exit("Modeler given was not hypershelf or mallet")

    log = open(log_file, 'a+')
#    print subprocess.check_output(["echo", "ABCCCC"])
    log.write(results)
    log.write("\n")

    log.close()

def populate_parser(parser):
    parser.add_argument("corpus", help="Path to corpus")
    parser.add_argument("--topics", required=True, type=int, help="Number of topics")
    parser.add_argument("--iterations", default=500, type=int, help="Number of iterations")
    parser.add_argument("--log", default="log.csv", help="Path to log file")
    parser.add_argument("--m", dest="modeler", required=True, help="Topic-Modeler to run (hypershelf or mallet)")
    parser.add_argument("--f", dest="function", help="Function to run (init or train)")

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    populate_parser(parser)
    args = parser.parse_args()

#    print args
#    print os.getcwd()
    main(args)
    
