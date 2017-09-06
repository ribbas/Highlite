# Highlite

A simple command line tool that compares an input document to several tagged corpora for cosine similarity and other analyses.

## Quick Start

Once installed, Highlight can be executed with the required data.

### Basic Usage

`python highlite.py john_doe_resume.pdf computer-science data-science computer-engineering baseball-coach --ignore_words john doe california ca --use_stop_words --score --recreate --stats --preview`

## Installation

A Makefile has been provided for installation.
- `make installenv` will create and set up a virtual environment if none has been created.
- `make init` will install all the requirements if a virtual environment has been created and sourced.
- `make init-getresume PASSWORD=your_password` will also install getresume if access is provided.

Additional rules are provided for development:
- `make update` updates the Python requirements
- `make clean` removes temporary files created
- `make reset` removes all scraped data and built corpus
- `make clean-all` invokes `make clean` and `make reset`

Tests are provided through the Makefile as well with `make test`.

### Dependencies

- Python 2.7, virtualenv, PIP and the packages included in `requirements.txt`
- [Tor](https://www.torproject.org/projects/torbrowser.html.en) (if getresume is included)
- [Privoxy](https://www.privoxy.org/) (if getresume is included)


## getresume

Highlite was initially designed to analyze resumes or portfolios. [getresume](https://github.com/sabbirahm3d/getresume) is a tool that scrapes resumes given the area or profession.

### Restrictions

The hosting website for the resumes explicitly forbids any crawlers in their `robots.txt`. Because crawlers are not always used responsibly, getresume is ignored during installation.

### Usage

If getresume is made available, it is integrated with Highlite and offers the following options:

- `areas` (required: array of str): the list of areas or professions to obtain resumes from
- `--anon` (bool, default: False): masks the IP addresses of the spiders.<br>
**WARNING** _This method utilizes The Tor Network. Tor must be enabled and configured to host proxies, along with the other dependecies found in [getresume](https://github.com/sabbirahm3d/getresume)_
- `--pages` (int, default: 0): number of additional pages beyond the first page to crawl through the hosting website