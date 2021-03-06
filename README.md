[![Build Status](https://travis-ci.org/TheDan64/rusty-types.svg?branch=master)](https://travis-ci.org/TheDan64/rusty-types)

Rusty Types
===========

## 1. Introduction
Python 3's [type hints][type-hints] and [typing][typing] module help code readability. They also have the added benefit of allowing a static typechecker to run over your code. Prior knowledge of these two features is assumed from here on out.

Although some might see it as unPythonic, Rusty Types provides some classes that act like specialized monads more commonly seen in languages such as Rust and Haskell. Type hints and the typings module really help this approach to shine.

## 2. Installation
Rusty Types works with all versions of Python 3, however there may be a version specific requirements:
* 3.0 - 3.4: typing library, version 3.5.3 or higher (is a dependency)
* 3.5: Python must be version 3.5.3+
* 3.6: None!

## 3. Usage
Suppose we'd like to aggregate some errors in an HTTP request to our server. A Pythonic approach might be to use exceptions to pass up the error data and return only on a valid success:

```python
from typing import Dict, List

def extract_special_values(json_dict) -> List[int]:
    error_list = []

    if not json_dict.get("foo"):
        error = {
            "reason": "Expected a foo parameter",
            "value": None
        }
        error_list.append(error)

    if error_list:
        raise MyCustomException(errors=error_list)

    foo = json_dict["foo"]

    return [foo, ...]

def get_request(self, payload):
    error_list = []

    try:
        values = extract_special_values(payload)
    except MyCustomException as e:
        error_list.append(e.errors)

        raise HTTPBadRequest(error_list)

    # Success! Use values
```

Here, we raise and subsequently catch one exception just to capture the underlying data and raise another exception to pass to our web framework of choice to display. This approach is sort of bulky and ugly to look at, but totally Pythonic.

Now let's look at returing the error collection in a Pythonic manner. Let's hope your return types aren't too similar:

```python
from typing import Any, Dict, List

def extract_special_values(json_dict) -> Union[List[int], List[Dict[str, Any]]]:
    error_list = []

    if not json_dict.get("foo"):
        error = {
            "reason": "Expected a foo parameter",
            "value": None
        }
        error_list.append(error)

    if error_list:
        return error_list

    foo = json_dict["foo"]

    return [foo, ...]

def get_request(self, payload):
    error_list = []

    values = extract_special_values(payload)

    # Both return lists, so we have to check the inner type as well:
    if isinstance(values, List[Dict[str, Any]]):
        error_list.append(values)

        raise HTTPBadRequest(error_list)

    # Success! Use values
```

Now you might be thinking, "Hold up! isinstance?! What gives? I thought you said the next example would be Pythonic?" Well, it is. We're not checking whether our value is an instance of a specific type, but of an [Abstract Base Class][abcs]. ABCs define a set of methods which describe the behavior of a type rather than looking at the actual type itself. I tend to think this approach at least, *looks* a little bit easier to read.

Now, both of these approaches aren't at all inherintely bad and can definitely be leveraged correctly. But they aren't as readable or nice to work with as we would like.

Here, the `Result` type allows you to return one of two data wrappers: `Ok(data)` or `Err(data)`. They have the same methods, but each return different results. We can determine if the underlying data was returned from a successful call or not:

```python
from rusty_types.result import Err, Ok, Result
from typing import Any, Dict, List

def extract_special_values(json_dict) -> Result[List[int], List[Dict[str, Any]]]:
    error_list = []

    if not json_dict.get("foo"):
        error = {
            "reason": "Expected a foo parameter",
            "value": None
        }
        error_list.append(error)

    if error_list:
        return Err(error_list)

    foo = json_dict["foo"]

    return Ok([foo, ...])

def get_request(self, payload):
    error_list = []

    result = extract_special_values(payload)

    if result.is_err():
        error_list.append(result.unwrap())

        raise HTTPBadRequest(error_list)

    values = result.unwrap()

    # Success! Use values
```

Personally, I find this approach much easier to read and I immediately can infer what the code is trying to do without having to reason about a try/except block or a manual isinstance check.

Best of all, because `Result`'s internal isinstance check is overriden, `Ok` and `Err` will be seen as instances if and only if they have the correct inner value type:

```python
result = Result[int, str]

assert isinstance(Ok(1), result)
assert isinstance(Err("foo"), result)

assert not isinstance(Ok("foo"), result)
assert not isinstance(Err(1), result)
```

Note: You wouldn't normally be making these isinstance calls in your actual code. But, this means they should work well with static typecheckers such as [mypy][mypy]. If not, please file a bug!

## 4. Documentation

### Either

TODO :)

### Result

TODO (:

### Option

TODO :)

## 5. Planned Features

All syntax is very TBD but here is a preview of what might be added.

### Custom Types

Custom types would allow for tagged union-like classes that can have a lot more variants than the types already provided.

Suppose we wanted to create a custom type that has three distinct variants. One of which allows for a generic type, T:
```python
class CustomType(TaggedUnion):
    A(int)
    B(float, T)
    C
```

This would allow us to return values based around those types:
```python
# Note that str would fill in for T above and any of these returns would be valid:
def foo() -> CustomType[str]:
    return A(1)
    return B(3.14, "bar")
    return C
```

### Pattern Matching

Having to call `.unwrap()` is more of a placeholder for now. It'll still exist long term but the preferred way to get a value would be to match it directly.

For example, today:
```python
if option.is_some():
    print(option.unwrap())
```

Would ideally become something like pattern matching in other languages:
```python
match(option, Some(value)):
    print(value)
```

Of course, Python doesn't give us a lot of room to work with. Suggestions and ideas are welcome!

[abcs]: https://docs.python.org/3/library/abc.html
[type-hints]: https://www.python.org/dev/peps/pep-0484/
[typing]: https://docs.python.org/3/library/typing.html
[mypy]: http://mypy-lang.org/
