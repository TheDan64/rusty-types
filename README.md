[![Build Status](https://travis-ci.org/TheDan64/rusty-types.svg?branch=master)](https://travis-ci.org/TheDan64/rusty-types)

Rusty Types
===========

## 1. Introduction
Python 3's [type hints][type-hints] and [typing][typing] module help code readability. They also have the added benefit of allowing a static typechecker to run over your code. Prior knowledge of these two features is assumed from here on out.

Although some might see it as unPythonic, Rusty Types provides some classes that act like specialized monads more commonly seen in languages such as Rust and Haskell. Type hints and the typings module really help this approach to shine.

## 2. Example
Suppose we'd like to aggregate some errors in an HTTP request to our server. A Pythonic approach might be to use exceptions to pass up the error data and return only on a valid success:

```python
from rusty_types.result import Err, Ok, Result
from typing import Any, Dict, List

def extract_special_values(json_dict: Dict[str, Any]) -> List[int]:
    error_list = []

    if not json_dict.get("foo"):
        error = {
            "reason": "Expected a foo parameter",
            "value": None
        }
        error_list.append(error)

    # ... find more errors if any ...

    if error_list:
        raise MyCustomException(errors=error_list)

    foo = json_dict["foo"]

    # ...

    return [foo, bar, baz]

class View:
    def get_request(self, payload):
        error_list = []

        # ... find more errors if any ...

        try:
            values = extract_special_values(payload)
        except MyCustomException as e:
            error_list.append(e.errors)

            raise HTTPBadRequest(error_list)

        # Proceed
```

Here, we raise and subsequently catch one exception just to capture the underlying data and raise another exception to pass to our web framework of choice to display. This approach is sort of bulky and ugly to look at, but totally Pythonic.

Now let's look at returing the error collection. Let's hope your return types aren't too similar:

```python
def extract_special_values(json_dict: Dict[str, Any]) -> Union[List[int], List[Dict[str, Any]]]:
    # ... see above ...

    if error_list:
        return error_list

    # ...

    return [foo, bar, baz]

class View:
    def get_request(self, payload):
        # ...

        value = extract_special_values(payload)

        # Both return lists, so we have to check the inner type as well:
        if isinstance(result, List[Dict[str, Any]]):
            error_list.append(result.value)

            raise HTTPBadRequest(error_list)

        # Proceed
```

Although this approach is also somewhat Pythonic, using isinstance yourself is usually discouraged. I tend to think this approach at least, *looks* a little bit easier to read.

Now, both of these approaches aren't at all inherintely bad and can definitely be leveraged correctly. But they aren't particularly readable or nice to work with.

Here, the `Result` type would allows you to return a data wrapper that can be checked as to whether it is expected or indicates a problem regardless of whether or not the underlying data is of the same or a similar type:

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

    # ...

    if error_list:
        return Err(error_list)

    foo = json_dict["foo"]

    # ...

    return Ok([foo, bar, baz])

class View:
    def get_request(self, payload):
        error_list = []

        # Check some params, fill up error_list

        result = extract_special_values(payload)

        if result.is_err():
            error_list.append(result.value)

            raise HTTPBadRequest(error_list)

        values = result.value

        # Proceed
```

Personally, I find this approach much easier to read and I immediately can infer what the code is trying to do without having to reason about a try/except block or a manual isinstance check. Best of all, they should work with static typecheckers such as [mypy][mypy]. If not, please file a bug!

## 3. Documentation

TODO :)

[type-hints]: https://www.python.org/dev/peps/pep-0484/
[typing]: https://docs.python.org/3/library/typing.html
[mypy]: http://mypy-lang.org/
