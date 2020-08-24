# 2020/08/24 - Common Crawl Search Engine

- ccse will search for keywords in [Common Crawl datasets](https://commoncrawl.org/)
- 188 + 291 (aho-corasick algorithm) = 479 lines of code.

## Getting started

```
# wget https://commoncrawl.s3.amazonaws.com/crawl-data/CC-MAIN-2018-26/segments/1529267859766.6/wet/CC-MAIN-20180618105733-20180618125538-00026.warc.wet.gz
...
# gunzip CC-MAIN-20180618105733-20180618125538-00026.warc.wet.gz
...
# ccse CC-MAIN-20180618105733-20180618125538-00026.warc.wet keyword search engine
...
# time ./ccse.scm  CC-MAIN-20180618105733-20180618125538-00026.warc.wet keyword search engine > out.txt

real	0m 12.67s
user	0m 12.54s
sys	0m 0.10s
```

## ChangeLog

- 2020/08/24: v0.1.0 - initial release 

  - [alpine](/bin/ccse/alpine/v0.1.0/ccse)
  - [debian buster](/bin/ccse/debian/buster/v0.1.0/ccse)
