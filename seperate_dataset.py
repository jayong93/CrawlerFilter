#!/usr/bin/python3

import argparse
import random

def add_arguments(parser):
    parser.add_argument("title", type=argparse.FileType('r', encoding='utf-8'), help="text file which has titles")
    parser.add_argument("comment", type=argparse.FileType('r', encoding='utf-8'), help="text file which has comments")
    parser.add_argument("--title_prefix", default='title')
    parser.add_argument("--comment_prefix", default='comment')
    return parser


if __name__ == '__main__':
    parser = add_arguments(argparse.ArgumentParser())
    args = parser.parse_args()
    title_list = args.title.read().splitlines()
    comment_list = args.comment.read().splitlines()
    data_set = list(zip(title_list, comment_list))
    random.shuffle(data_set)

    train_len = int(len(data_set)*0.7)
    title_train = open(args.title_prefix + '_train', 'w', encoding='utf-8')
    comment_train = open(args.comment_prefix + '_train', 'w', encoding='utf-8')
    title_test = open(args.title_prefix + '_test', 'w', encoding='utf-8')
    comment_test = open(args.comment_prefix + '_test', 'w', encoding='utf-8')
    for (title, comment) in data_set[:train_len]:
        title_train.write(title+'\n')
        comment_train.write(comment+'\n')
    for (title, comment) in data_set[train_len:]:
        title_test.write(title+'\n')
        comment_test.write(comment+'\n')
