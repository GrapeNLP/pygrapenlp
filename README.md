# PYGRAPENLP: the GRAPENLP Python interface

PYGRAPENLP is an open-source Python package that enables the usage of GRAPENLP 
from Python code. For more information on GRAPENLP visit
https://github.com/GrapeNLP/grapenlp-core.

_This is a fork from the [original project](https://github.com/GrapeNLP/pygrapenlp)
to add a bit of functionality on top of the base class. See [usage](#usage) 
for information about the changes and new functionality._


## Dependencies

* python >= 3.6
* libgrapenlp-dev 2.8.0 or greater


### Libgrapenlp installation

* from sources: check out the source code from the
  [grapenlp-core repository](https://github.com/GrapeNLP/grapenlp-core) and follow
  the instructions to compile and install the library.

* in Ubuntu it can also be installed via the available [PPA repository](https://launchpad.net/~grapenlp/+archive/ubuntu/ppa):

		sudo add-apt-repository ppa:grapenlp/ppa
		sudo apt-get update
		apt-get install libgrapenlp-dev


## How to install

Run the following command in the project root folder:

	python setup.py install
	
Since there is a native component, a g++ toolchain must be available in the
system to compile it.


## Usage

### Classes

Two main Python classes are provided:

* [`GrammarEngine`](src/pygrapenlp/grammar_engine.py) is the raw engine, which
  which calls the GRAPE-NLP C++ engine to parse an utterance and returns its 
  results in (almost) native format, with all the graph labels recognized in the 
  utterance.

* [`RecognizerGrammarEngine`](src/pygrapenlp/recognizer_engine.py) is a
  wrapper on top of the bare engine. It uses the output symbol name structure
  to provide additional semantics, oriented towards language classification
  tasks.
  
Both engines use as input an _utterance_ and an optional _context dictionary_. 
`RecognizerGrammarEngine` accepts additional options: `add_role` and 
`skip_empty_entities`. It also provides the additional method `top_match`,
which parses and returns the result with highest score.

### Recognizer parsing

On the results provided by GRAPE-NLP, `RecognizerGrammarEngine` does the
following additional parsing:

 * A recognition score is added, for now always set at `1.0`
 * `intent.*` symbols are considered as a sentence-wide intent classification
   (it characterizes the whole utterance). Position information is ignored
 * `ent.*` symbols are considered as _entities_, extracted from fragments
   of the utterance, with the recognized utterance fragment as entity
   value (field `name`). The label is used as entity type (field `type`)
 * the remaining symbols are treated as _tags_, with the label as `key` and
   the recognized utterance fragment as `value`
   
Entities carry a bit of additional processing:
 * A `:name` suffix is taken as a _role_ qualifier for the entity type
   (i.e. `ent.type:role` defines the entity `ent.type` with role `role`).
   This also makes it possible to have multiple instances of the same 
   entity type in a single sentence. 
 * If `add_role` is on, and the entity has a role, it is added to its data
   object (field `role`). If there is no role, or `add_role` is off,
   nothing is added.
 * Empty entities (entities whose _value_ resolve to an empty string) are removed
   from the output if `skip_empty_entities` is on (it is by default).
   This also allows adding empty strings `<E>` as paths surrounded by entity 
   marks in the grammar (effectively making the entity _optional_)
  
 
### Command-line scripts

Two command-line scripts are installed as entry points:

* `pygrapenlp_extract_raw` calls `GrammarEngine`, providing raw symbols output
* `pygrapenlp_extract` calls `RecognizerGrammarEngine`, providing recognizer
  output

Additionally, `process-grammar` is a Bash shell script that can be used to
preprocess grammars and dictionaries in source format via
[Unitex](https://unitexgramlab.org/) to produce the formats needed bythe
GrapeNLP engine (of course, Unitex must be installed for it to work).


### Processing of context

TBD


## License

<a href="/LICENSE"><img height="48" align="left" src="http://www.gnu.org/graphics/empowered-by-gnu.svg"></a>

This program is licensed under the GNU Lesser General Public License version 2.1. Contact javier.sastre@telefonica.net for further inquiries.
