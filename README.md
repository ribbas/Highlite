# Highlite

A simple command line tool that compares an input document to several tagged corpora for cosine similarity and other analyses.

## Installation

A Makefile has been provided for installation. 

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