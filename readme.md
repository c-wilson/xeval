# ReptorServer
A RESTful reputation server.

## Scope
This server can be used to collect and retrieve reputation data for any number of users or "reputees."

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
An entry point is specified during installation. From the command line, simply run 
```$ reptorServer```

There are two optional parameters for specifying IP address and port. These parameters default to 
__localhost:8000__. For help, just use `-h` when running.

The web application runs, by default at http://localhost:8000/reptor


## POST interface.
POSTs are used to add data to the database. POSTs should JSON formatted with the following schema. 
If successful, a 402 request is returned.
```json
{
    "properties": {
        "reputer": {"type": "string"},
        "reputee": {"type": "string"},
        "repute": {
            "type": "object",
            "properties": {
                "rid": {"type": "string"},
                "feature": {"enum": ["clarity", "reach"]},
                "value": {
                    "type": "number",
                    "minimum": 0.0,
                    "maximum": 10.0
                }
            }
        }
    }
}
```

## GET interface
HTTP GET is used to request data about a reputee. The body of a GET request should be formatted according
 to the following schema:
```json 
{
  "properties": {
    "reputee": {"type": "string"}
    }
}
```

This will return a JSON body with the following data format:
```json
{
  "properties": {
    "clarity": {
      "score": {
        "type": "number",
        "minimum": 0.0,
         "maximum": 10.0
      },
      "confidence": {
        "type": "number",
        "minimum": 0.0,
        "maximum": 1.0
      }
    },
    "reach": {
      "score": {
        "type": "number",
        "minimum": 0.0,
         "maximum": 10.0
      },
      "confidence": {
        "type": "number",
        "minimum": 0.0,
        "maximum": 1.0
      }
    },
    "clout": {
      "score": {
        "type": "number",
        "minimum": 0.0,
         "maximum": 1.0
      },
      "confidence": {
        "type": "number",
        "minimum": 0.0,
        "maximum": 1.0
      }
    }
  }
}

```

## Testing.
There is a pytest module for development. To use, run `$/testing/python test.py`