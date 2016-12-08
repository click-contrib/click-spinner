# Click Spinner

[![PyPI](https://img.shields.io/pypi/v/click-spinner.svg)](https://pypi.python.org/pypi/click-spinner/) [![Build Status](https://travis-ci.org/click-contrib/click-spinner.svg?branch=master)](https://travis-ci.org/click-contrib/click-spinner)

Sometimes you would just like to show the user some progress, 
but a progress bar is not suitable because you don’t know how much longer it would take. 
In these cases you might want to display a simple spinner using the `spinner()` function.

Example usage:

```py
with click_spinner.spinner():
        do_something()
        do_something_else()
```

It looks like this:

![spinner](https://cloud.githubusercontent.com/assets/1288133/18229827/29629cd4-728f-11e6-8007-6c85ac50565c.gif)

Spinner class based on on a [gist by @cevaris](https://gist.github.com/cevaris/79700649f0543584009e).

Introduced in [PR #649](https://github.com/pallets/click/pull/649). 

## Install

```
pip install click-spinner
```

Supports Python 2.7 and 3.

## Authors

- Yoav Ram (@yoavram)
- Andreas Maier (@andy-maier)
