[![Build Status](https://travis-ci.org/TheDan64/rusty-types.svg?branch=master)](https://travis-ci.org/TheDan64/rusty-types)

Rusty Types
===========

Python 3's type hints and typings module help code readability. They also have the added benifit of allowing a static typechecker to run over your code.

Although some might see it as unPythonic, Rusty Types provides some classes that act like specialized monads more commonly seen in languages such as Rust and Haskell. Type hints and the typings module really help these monads to shine.

Take the `Result` type. It allows you to return a data wrapper that can be checked as to whether it is expected or indicates a problem. Suppose we'd like to aggregate some errors in an HTTP request to our server:

```python
from rusty_types.result import Err, Ok, Result
from typing import Any, Dict, List

def extract_special_values(json_dict: Dict[str, Any]) -> Result[List[int], List[Dict[str, Any]]]:
    error_list = []

    if not json_dict.get("foo"):
        error = {
            "reason": "Expected a foo parameter",
            "value": None
        }
        error_list.append(error)

    if not json_dict.get("bar"):
        error = {
            "reason": "Expected a foo parameter",
            "value": None
        }
        error_list.append(error)

    # ...

    if error_list:
        return Err(error_list)

    return Ok([foo, bar, baz])

class View:
    def get_request(self, payload):
        error_list = []

        # Check some params, fill up error_list

        result = extract_special_values(payload)

        if result.is_err():
            error_list.append(result.value)

            # Now raise with our list of errors
            raise HTTPBadRequest(error_list)

        values = result.value

        # Proceed
```

In this contrived example, the Result instance makes passing up and collecting errors clean and the intent easy to understand.
