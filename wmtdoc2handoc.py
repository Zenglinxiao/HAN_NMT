#!/usr/bin/python3
# coding: utf8
"""Convert WMT docNMT corpus files as HAN doc corpus files."""

import argparse
import codecs


def check_last(output, sl, tl, doc_index):
    with codecs.open(output + '.' + sl, 'r', encoding='utf8') as fout_src,\
            codecs.open(output + '.' + tl, 'r', encoding='utf8') as fout_tgt:
        slen = len(fout_src.readlines())
        tlen = len(fout_tgt.readlines())
        assert slen == tlen, "out src/tgt should be aligned."
        print(f"output lines: {slen}/{tlen}")
    if doc_index[-1] == slen:
        print("remove last newline index.")
        doc_index = doc_index[:-1]
    return doc_index


def wmtdoc2handoc(inputs, sl, tl, output):
    msg_format = "Extract {} valid segment from {} lines, {} doc in total."
    err_msg="#not simutanously blank line: [{}]|[{}].#"
    doc_index = [0]
    with codecs.open(inputs + '.' + sl, 'r', encoding='utf8') as fin_src,\
            codecs.open(inputs + '.' + tl, 'r', encoding='utf8') as fin_tgt,\
            codecs.open(output + '.' + sl, 'w', encoding='utf8') as fout_src,\
            codecs.open(output + '.' + tl, 'w', encoding='utf8') as fout_tgt:
        valid_segments = 0
        droped_line = 0
        for i, (sline, tline) in enumerate(zip(fin_src, fin_tgt)):
            if sline.strip() == '':
                if tline.strip() != '':
                    print(err_msg.format(sline, tline))
                    droped_line += 1
                else:
                    doc_index.append(valid_segments)
            else:
                valid_segments += 1
                fout_src.write(sline)
                fout_tgt.write(tline)
    doc_index = check_last(output, sl, tl, doc_index)
    print(f"drop bad blank line pair: {droped_line}")
    print(msg_format.format(valid_segments, i+1, len(doc_index)))
    with codecs.open(output + '.doc', 'w', encoding='utf8') as fout_doc:
        for doc_idx in doc_index:
            fout_doc.write(str(doc_idx) + '\n')


def opts_wmtdoc2handoc_file(parser):
    """Add arguments for get the diff of two vocab set."""
    parser.add_argument("--inputs", "-i", required=True,
                        help="WMT corpus file basename.")
    parser.add_argument("--sl", "-sl", required=True,
                        help="corpus source language suffix.")
    parser.add_argument("--tl", "-tl", required=True,
                        help="corpus target language suffix.")
    parser.add_argument("--output", "-o", required=True,
                        help="Output files name.")
    return parser


def main():
    parser = argparse.ArgumentParser(
        description="Extract doc boundary from blank lines.")
    args = opts_wmtdoc2handoc_file(parser).parse_args()
    wmtdoc2handoc(args.inputs, args.sl, args.tl, args.output)


if __name__ == "__main__":
    main()
