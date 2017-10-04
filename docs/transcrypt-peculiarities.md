Transcrypt peculiarities
========================

While Transcrypt does operate off of the python compiler, not all python functions translate well to JavaScript.

In short, some functionality deemed too slow to implement has been left out.

Known limitations:
- the `in` operator no longer refers to `__contains__` and no longer works on lists
- negative indices on arrays no longer work, and only return `undefined`
- indexing past the end of an array no longer errors, and just returns `undefined`
- slicing an array out of bounds will result in a list containing nulls.
  - `([1, 2, 3])[:5]` gives `[1, 2, 3]` in Python, but results in `[1, 2, 3, null, null]` in Transcrypt
