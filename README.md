# PYGRAPENLP: the GRAPENLP Python interface

PYGRAPENLP is an open-source Python package that enables the usage of GRAPENLP 
from Python code. For more information on GRAPENLP visit
https://github.com/GrapeNLP/grapenlp-core.

_This is a small for from the [original
project](https://github.com/GrapeNLP/pygrapenlp) to add a bit of functionality
on top of the base class._


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
  allows parsing a sentence and extracting its output symbols, as declared in
  the grammar, as a bare Python dictionary

* [`RecognizerGrammarEngine`](src/pygrapenlp/recognizer_engine.py) is a
  wrapper on top of the bare engine. It uses the output symbol name structure
  to provide additional semantics, oriented towards language classification
  tasks:
    - `intent.*` symbols are considered as sentence-wide intent classification
	   (it characterizes the whole utterance)
	- `int.*` symbols are considered as _entities_, extracted from fragments
	  of the utterance
    - the remaining symbols are treated as _tags_
    - entities carry a bit of additional processing:
	    * a `:name` suffix is taken as a _role_ qualifier for the entity type
          (i.e. `ent.type:role` defines the entity `ent.type` with role `role`).
		  This also enables the appearance of multiple instances of the same 
		  entity type in a single sentence
        * empty entities (entities that resolve to an empty string) are removed
          from the output. This allows adding empty strings `<E>` as paths 
		  surrounded by entity marks in the grammar (effectively making them 
		  _optional_)
	  
 
### Command-line scripts

Two command-line scripts are installed as entry points:

* `pygrapenlp_extract_raw` calls `GrammarEngine`, providing raw symbols output
* `pygrapenlp_extract` calls `RecognizerGrammarEngine`, providing recognizer
  output

Additionally, `process-grammar` is a Bash shell script that can be used to
preprocess grammars and dictionaries in source format via
[Unitex](https://unitexgramlab.org/) to produce the formats needed bythe
GrapeNLP engine (of course, Unitex must be installed for it to work).


## License

<a href="/LICENSE"><img height="48" align="left" src="http://www.gnu.org/graphics/empowered-by-gnu.svg"></a>

This program is licensed under the GNU Lesser General Public License version 2.1. Contact javier.sastre@telefonica.net for further inquiries.
