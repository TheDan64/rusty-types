# Change Log
All notable changes to this project will be documented in this file. This project adheres to [Semantic Versioning](http://semver.org/).

## [0.1.0] - Unreleased
### Added
- rusty_types/either.py
  - Either[L, R] - A class that can contain a left or right type
  - Left(L) - Instance of Either that can take a value of type L
  - Right(R) - Instance of Either that can take a value of type R
- rusty_types/option.py
  - Option[T] - A class that can optionally contain a type
  - Some(T) - Instance of Option that can take a value of type T
  - Nothing - Singleton instance of Option
- rusty_types/result.py
  - Result[O, E] - A class that can contain an ok or err type
  - Ok(O) - Instance of Result that can take a value of type O
  - Err(E) - Instance of Result that can take a value of type E
