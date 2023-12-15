
# Data Wrangler (dw)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT) ![Python](https://img.shields.io/badge/python-3.6-blue.svg) ![Python](https://img.shields.io/badge/python-3.7-blue.svg) ![Python](https://img.shields.io/badge/python-3.8-blue.svg) ![Python](https://img.shields.io/badge/python-3.9-blue.svg) ![Python](https://img.shields.io/badge/python-3.10-blue.svg) ![Python](https://img.shields.io/badge/python-3.11-blue.svg) ![Python](https://img.shields.io/badge/python-3.12-blue.svg)


[dw](https://github.com/MountainField/dw) is a data wrangling tool for command-line interface user.

- Example

    ```bash
    $ cat abc.csv | dw csv to_markdown
    | a    | b    | c    |
    | ---- | ---- | ---- |
    | 1    | 1    | 1    |
    | 1    | 2    | 2    |
    | 2    | 1    | 3    |
    | 2    | 2    | 4    |
    
    $ cat abc.csv | dw csv pivot --field a --formula "sumc_c=sum(c)"
    | a    | sum_c |
    | ---- | ----- |
    | 1    | 3     |
    | 2    | 7     |
    ```


## Setup

```bash
pip install git+https://github.com/MountainField/dw
```

Author
------

- **Takahide Nogayama** - [Nogayama](https://github.com/nogayama)


License
-------

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details

Contributing
------------

Please read [CONTRIBUTING.md](./CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

