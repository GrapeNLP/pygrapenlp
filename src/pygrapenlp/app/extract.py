'''
Call the grammar engine via PygrapeNLP
'''


import os
import sys
import argparse
from types import SimpleNamespace
from operator import itemgetter
import json

from typing import List

from pygrapenlp import RecognizerGrammarEngine, CompressedDelaf
from pygrapenlp.utils.u_set_trie import add_u_set_trie_strings_to_string_set



# ---------------------------------------------------------------------------


def parse_args(args: List[str]) -> argparse.Namespace:
    """
    Parse command-line arguments
    """
    parser = argparse.ArgumentParser(description='Test grapeNLP resolution')

    parser.add_argument('--quiet', '-q', action='store_true')
    parser.add_argument('--raw-output', '--raw', action='store_true')
    parser.add_argument('--reraise', action='store_true', help='raise on errors')

    parser.add_argument('--grammar', metavar='FST2-FILENAME')
    parser.add_argument('--dictionary', metavar='COMPRESSED-DELAF-FILENAME')

    parser.add_argument('--context', nargs='+', metavar='KEY=VALUE')

    g = parser.add_mutually_exclusive_group(required=True)
    g.add_argument('--utterance', nargs='+', help='utterances to parse')
    g.add_argument('--dict-words', nargs='+', help='dictionary words to look up')

    args = parser.parse_args(args)
    return args


def process(args: SimpleNamespace):
    '''
    '''
    # Look up words in the dictionary
    if args.dict_words:
        name, ext = os.path.splitext(args.dictionary)
        print(args.dictionary, name, ext)
        dic = CompressedDelaf(args.dictionary, name + '.inf')
        for w in args.dict_words:
            print(". Word:", w)
            #print(dic.get_set_of_ambiguous_word_serialized_semantic_properties(w))
            proplist = dic.get_ambiguous_word_properties(w)
            if not proplist:
                print('  --not found')
                continue
            result = set()
            for prop in proplist:
                add_u_set_trie_strings_to_string_set(prop.semantic_traits, result)
            print("  ", result)
        return

    # Parse an utterance
    print(". Create engine")
    engine = RecognizerGrammarEngine(args.grammar, args.dictionary)
    print(". engine created")

    if not args.context:
        context = None
    else:
        context = dict(kv.split('=', 1) for kv in args.context)
        print('. Context:')
        for kv in context.items():
            print('  {} = {}'.format(*kv))

    for ut in args.utterance:
        result = engine.top_match(ut, context=context)
        if args.raw_output:
            print(json.dumps(result, indent=2, ensure_ascii=False))
            continue

        print('\n. Utterance:', ut)
        print('. Intent:', result['intent'])

        if result['entities']:
            print('. Entities:')
            for ent in sorted(result['entities'], key=itemgetter('start_index')):
                print('   type =', ent['type'], end=' ')
                print('   value =', ent['name'])

        if 'tags' in result:
            print('. Tags:')
            for tag in sorted(result['tags'], key=itemgetter('start_index')):
                print('   ', tag['key'], '=' if tag['value'] else '', tag['value'])


# ---------------------------------------------------------------------------

def main(args=None):
    '''
    Entry point
    '''
    if args is None:
        args = sys.argv[1:]
    args = parse_args(args)

    try:
        process(args)
    except Exception as e:
        print('Error:', e)
        if args.reraise:
            raise
        sys.exit(1)


if __name__ == '__main__':
    main()
