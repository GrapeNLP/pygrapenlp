'''
Call the raw grammar engine via PygrapeNLP
'''


import sys
import argparse
from types import SimpleNamespace
import json

from typing import List

from pygrapenlp import GrammarEngine
from pygrapenlp.utils.u_out_bound_trie import u_out_bound_trie_string_to_string



# ---------------------------------------------------------------------------


def parse_args(args: List[str]) -> argparse.Namespace:
    """
    Parse command-line arguments
    """
    parser = argparse.ArgumentParser(description='Test grapeNLP resolution')

    parser.add_argument('--quiet', '-q', action='store_true')
    parser.add_argument('--reraise', action='store_true', help='raise on errors')

    parser.add_argument('--grammar', metavar='FST2-FILENAME')
    parser.add_argument('--dictionary', metavar='COMPRESSED-DELAF-FILENAME')

    parser.add_argument('--context', nargs='+', metavar='KEY=VALUE')

    parser.add_argument('utterance', nargs='+', help='utterances to parse')
    args = parser.parse_args(args)
    return args


def native_results_to_python_dic(sentence: str, native_results, num: int=0):
    results = []
    if native_results.empty():
        return results

    num_results = native_results.size()
    for n, r in enumerate(range(num_results)):
        segments = {}
        native_result = native_results.get_elem_at(r)
        native_result_segments = native_result.ssa
        for i in range(0, native_result_segments.size()):
            native_segment = native_result_segments.get_elem_at(i)
            native_segment_label = native_segment.name
            segment_label = u_out_bound_trie_string_to_string(native_segment_label)
            segment = {'value': sentence[native_segment.begin:native_segment.end],
                       'start': native_segment.begin,
                       'end': native_segment.end}
            segments[segment_label] = segment
        results.append(segments)
    return results


class Printer:

    def __init__(self, quiet: bool):
        self._quiet = quiet

    def __call__(self, *args, **kwargs):
        if not self._quiet:
            print(*args, **kwargs)



def process(args: SimpleNamespace):
    '''
    '''
    prt = Printer(args.quiet)

    # Parse an utterance
    prt(". Create engine")
    engine = GrammarEngine(args.grammar, args.dictionary)
    prt(". engine created")

    if not args.context:
        context = None
    else:
        context = dict(kv.split('=', 1) for kv in args.context)
        if not args.quiet:
            prt('. Context:')
            for kv in context.items():
                print('  {} = {}'.format(*kv))

    for ut in args.utterance:
        result = engine.tag(ut, context=context)

        prt('\n. Utterance:', ut)
        result = native_results_to_python_dic(ut, result)
        json.dump(result, sys.stdout, indent=2, ensure_ascii=False)


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
