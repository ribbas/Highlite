# Highlite

A simple command line tool that compares an input document to several tagged corpora for cosine similarity and other analyses.

## Quick Start

Once installed, Highlight can be executed with the required data.

### Example Usages

**To build a corpus**

- **Using getresume**

  `python highlite.py --build getresume --corpus corpus_label1 corpus_label2 --anon --pages 3`

- **Using CustomCorpus**

  `python highlite.py --build custom --corpus corpus_label1 --dir_input path/to/my_other_docs`

**To analyze the input document**

`python highlite.py john_doe_resume.pdf --corpus corpus_label1 corpus_label2 --score --ignore_terms john doe california --use_stop_words --ngram_range 1 2 --max_feats 500`

**To reconstruct the document as an HTML**

`python highlite.py john_doe_resume.pdf --recreate`

**To preview the reconstructed HTML file**

`python highlite.py john_doe_resume.pdf --preview`

**To view statistics on the analysis report**

`python highlite.py john_doe_resume.pdf --stats closest_docs top_tfidf_terms tfidf_summary`

**All the features can be chained together as well**

`python highlite.py john_doe_resume.pdf --corpus corpus_label1 --build getresume --corpus corpus_label1 corpus_label2 --anon --score --ignore_terms john doe california --use_stop_words --recreate --stats --preview`



## Installation

A Makefile has been provided for installation. The Makefile requires a virtual environment to be set up.
- `make installenv` will create and set up a virtual environment if none has been created.
- `make init` will install all the requirements if a virtual environment has been created and sourced.
- `make init-getresume PASSWORD=your_password` will install getresume if access is provided.

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

- `--corpus` (required: array of str): the list of areas or professions to obtain resumes from
- `--anon` (bool, default: False): masks the IP addresses of the spiders.
**WARNING** _This method utilizes The Tor Network. Tor must be enabled and configured to host proxies, along with the other dependecies found in [getresume](https://github.com/sabbirahm3d/getresume)_
- `--pages` (int, default: 0): number of additional pages beyond the first page to crawl through the hosting website

## CustomCorpus

If getresume is not available, corpora can be built manually with CustomCorpus.<br>
A collection of PDF files can be used as an input for building a corpus. Here is an example usage of creating a corpus with PDF files stored in the directory `/path/to/dir`:<br>

`python highlite.py --build custom --corpus corpus_label1 --dir_input path/to/dir`

Once the corpus is built, it is saved on the path determined by `highlight.settings.RAWCORPUS_DIR`. The location can be viewed with: `python highlite.py --get_corpus_dir`

### Restrictions

Currently, only PDF files are supported as the input corpus. Plain text files can also be used as a corpus by manually moving them to the directory specified by `--get_corpus_dir`.

## Options

| Feature | Description | Default | Parameters |
| ------------- | ------------- | ------------- | ------------- |
| build | Method of building corpus | `None`| `<str>: {getresume, custom}`|
| corpus | Labels of corpora to analyze against | `None` | `<list of <str>>` |
| anon | Anonymize IP (for getresume only) | `False` | N/A |
| pages | Number of pages beyond the first page to crawl (for getresume only) | `0`  | `<int>` |
| dir_input | Path of input files to be converted into the corpus (for CustomCorpus only) | `""` | `<str>` |
| input_t | Type of input sample files (for CustomCorpus only) | `pdf` | `<str>` |
| score | Score input document | `False` | N/A |
| ignore_terms | List of words to ignore in scoring document | `None` | `<list of <str>>` |
| max_feats | Maximum number of features for the TF-IDF vectorizer | `None` | `<int>` |
| ngram_range | n-grams range for the TF-IDF vectorizer | `1 3` | `2 <int>` |
| use_stop_words | Stopwords for the TF-IDF vectorizer | `False` | N/A |
| recreate | Create HTML output of the scored document | `False` | N/A |
| stats | Get summary of resume analysis | `None` | `0 or multiple <str>: {closest_docs, top_tfidf_terms, tfidf_summary, buzzwords}` |
| preview | Opens up the tagged document of the browser for preview | `False` | N/A |
| buzzwords | Update buzzwords corpus | `False` | N/A |
| get_corpus_dir | Get the location of the generated corpus | `False` | N/A |
