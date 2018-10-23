# v2.0.1
Removed project dependent method from Python/native interface (the main grapenlp-core method to invoke is "tag" inside Python script grammar_engine.py)

# v2.0.0

This is the first version uploaded to GitHub. It is operative, though documentation is still lacking and it is limited to Ubuntu: the Python package contains a precompiled version of the grapenlp-core library, which has been compiled in Ubuntu. In a future version I expect to split the library into an autoinstallable native library (e.g. a Debian package) and the C++/Python interface source code, and to let the Python package installation process include the compilation of the interface source code to make it platform independent. You may compile yourself the grapenlp-core library in another platform and overwrite by hand the file libgrapenlp.so inside the pygrapenlp package to port it to that platform.
