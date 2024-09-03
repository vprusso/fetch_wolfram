# fetch_wolfram

If you have a number and want to have a guess at its possible closed form expressions via CLI.

[I'm a lazy lazy man](https://www.youtube.com/watch?v=vjh56rivPTQ). I don't like manually copying and pasting a number
into WolframAlpha via the browser. This allows you to just do this via the terminal.

I find myself doing this often when I am trying to characterize floating point numbers into concise mathematical expressions. If this is you as well, hopefully this helps you as well!

## Installation

Ideally, create a virtual environment. Then:

```
pip install requirements.txt
```

## Example

```
python src/fetch_wolfram/fetch.py 3.14159
```

which yields

```
π≈3.1415926535
sqrt(6 ζ(2))≈3.1415926535
π^2/31^(1/3)≈3.14180466
```