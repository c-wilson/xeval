# ReptorServer
A RESTful reputation server.

## Installation instructions:
I am most comfortable using the Anaconda Python distribution, which is nicely cross-platform and has a great package installation experience and almost everything I’ve needed to date.

1. Download and follow installation instructions for _miniconda_ from www.anaconda.com
2. From a terminal, make an environment named “xeval” for the project:
```
$ conda create -n xeval python=3.6
```
3. Activate the environment and install packages we’ll need:
```
$ source activate xeval
(xeval) $ conda install -c conda-forge falcon
(xeval) $ conda install numpy requests jsonschema pytest
```
4. Clone this repository and run setup.py from xeval environment:
```
(xeval) $ python setup.py install
```

## Running.
An entry point is specified. From the command line, run `$ reptorServer`.

There are two optional parameters for specifying IP address and port. Default is __localhost:8000__.
