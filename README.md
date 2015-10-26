Aranea
======

Aranea is a toy web-crawler that outputs a graph of the pages reachable by
following links from a given url. It outputs the graph in `dot` format to allow
for futher processing/analysis, and stays within the confines of the domain of
the given url.

Usage
-----

```
$ ./crawl.py http://aiohttp.readthedocs.org/en/stable/ -r -m4 | dot -Tpdf > aiohttp.pdf
```

Requirements
------------

 * `python > 3`
 * [`graphviz`](http://www.graphviz.org/) (if you want to visualise results)

Installation
------------

To install the Python dependencies simply:
```
$ pip install -r requirements.txt
```
To check your installation is working:
```
$ pip install -r requirements-test.txt
$ nosetests --with-coverage --cover-package=aranea
```

To visualise the resultant graph, you'll need to install `graphviz` with
something like:
```
apt-get install graphviz
```

Features
--------

 * Based on [`aiohttp`](http://aiohttp.readthedocs.org/en/stable/), facilitating
   efficient, interleaved async requests
 * Resolves links from HTML `<base>` tags
 * Tracks page resources from `<link>`, `<script>` and `<img>` tags, as well as
   just links to other web pages
 * Can change concurrency limits for speed/load tradeoffs (e.g. some sites may
   start refusing requests coming in too fast)
 * Can exclude resources from the output
 * Unix style "do one thing well" - passes on graphing to dedicated format/util

Issues
------

There's currently an issue when we shut down the event loop that's resulting in
the message:
```
Exception ignored in: Exception ignored in: Exception ignored...
```
This could be related to Python issues
[22836](https://bugs.python.org/issue22836) or
[23548](http://bugs.python.org/issue23548), and requires further investigation.

Also:
 * Does not follow page redirects
 * Does not track resources from CSS
 * Does not honour `robots.txt`
 * Not exhaustively tested with malformed links/content
