# Pretty-Parser

#Why pretty-parser ?
I was working with a json strings which contains numeric values as keys (float or int). default python json parser can't decode them so I worked to create my own json parser.
so , If you have a json string contains non string keys please use pretty-parser

#Usage
```python
from pretty_parser import json_decode

dict_result = json_decode('{1: "Apple", 2: "Mongo"}')
```
