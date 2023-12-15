# Develper Guide for Data Wrangler



[Packaging Python Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/)



## Getting Started



### Prerequisites

```sh
$ pip3 install --upgrade pip wheel
$ python3 -m pip install --upgrade build
```



### Installing

```sh
$ git clone git@github.com:MountainField/dw.git
$ cd dw
$ pip3 install -e '.[dev]'
```



## Running Tests

The test code is written in [RSpec](https://rspec.info) style using [USpec](https://github.com/MountainField/uspec) and [PyHamcrest](https://github.com/hamcrest/PyHamcrest). But to run the tests you just execute `unittest`  that is built in test framework

```sh
$ python3 -m unittest discover -v -s src/tests -p '*_spec.py'
```



## Formatting Code

```sh
$ yapf --style='{column_limit: 9999}' -r  -i src 
```



## Build

```sh
$ rm -rf dist && python3 -m build
```





## Authors



Takahide Nogayama

<a href="https://github.com/nogayama"><img src="https://avatars.githubusercontent.com/u/11750755" width="100"/></a>



## License（ライセンス）

IBM Proprietary

