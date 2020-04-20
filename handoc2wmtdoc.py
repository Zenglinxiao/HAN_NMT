#!/usr/bin/python3
# coding: utf8
"""Convert WMT docNMT corpus files as HAN doc corpus files."""

import argparse
import codecs
import tqdm


def check_last(output, sl, tl):
    with codecs.open(output + '.' + sl, 'r', encoding='utf8') as fout_src,\
            codecs.open(output + '.' + tl, 'r', encoding='utf8') as fout_tgt:
        slen = len(fout_src.readlines())
        tlen = len(fout_tgt.readlines())
        assert slen == tlen, "out src/tgt should be aligned."
        print(f"output lines: {slen}/{tlen}")
    return slen


def handoc2wmtdoc(inputs, sl, tl, doc, output):
    msg_format = "Convert {} doc of {} valid segment into {} lines in total."
    err_msg = "Bad convert: {} doc of {} valid segment but {} lines finally."
    with codecs.open(inputs + '.' + sl, 'r', encoding='utf8') as fin_src,\
            codecs.open(inputs + '.' + tl, 'r', encoding='utf8') as fin_tgt,\
            codecs.open(inputs + '.' + doc, 'r', encoding='utf8') as fin_doc,\
            codecs.open(output + '.' + sl, 'w', encoding='utf8') as fout_src,\
            codecs.open(output + '.' + tl, 'w', encoding='utf8') as fout_tgt:
        doc_begins = [int(line.strip()) for line in fin_doc]
        doc_ends = doc_begins[1:] + ['end']
        n_docs = len(doc_begins)
        print(f'Total {n_docs} documents to be convert...')
        fin_srcs = fin_src.readlines()
        fin_tgts = fin_tgt.readlines()
        n_segments = len(fin_srcs)
        print(f'{n_segments} segments in total.')
        for bod, eod in tqdm.tqdm(zip(doc_begins, doc_ends)):
            if eod == 'end':
                fout_src.writelines(fin_srcs[bod:])
                fout_tgt.writelines(fin_tgts[bod:])
            else:
                fout_src.writelines(fin_srcs[bod:eod])
                fout_tgt.writelines(fin_tgts[bod:eod])
                fout_src.write('\n')
                fout_tgt.write('\n')
    final_length = check_last(output, sl, tl)
    if final_length == n_segments + (n_docs - 1):
        print(msg_format.format(n_docs, n_segments, final_length))
    else:
        raise RuntimeError(err_msg.format(n_docs, n_segments, final_length))


def opts_handoc2wmtdoc_file(parser):
    """Add arguments for get the diff of two vocab set."""
    parser.add_argument("--inputs", "-i", required=True,
                        help="WMT corpus file basename.")
    parser.add_argument("--sl", "-sl", required=True,
                        help="corpus source language suffix.")
    parser.add_argument("--tl", "-tl", required=True,
                        help="corpus target language suffix.")
    parser.add_argument("--doc", "-doc", type=str, default='doc',
                        help="suffix for doc index file.")
    parser.add_argument("--output", "-o", required=True,
                        help="Output files name.")
    return parser


def main():
    parser = argparse.ArgumentParser(
        description="Form doc boundary as blank lines.")
    args = opts_handoc2wmtdoc_file(parser).parse_args()
    handoc2wmtdoc(args.inputs, args.sl, args.tl, args.doc, args.output)


if __name__ == "__main__":
    main()
