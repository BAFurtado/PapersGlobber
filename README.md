![ABMs](image.png)

#### Bernardo Alves Furtado--Ipea
#### Jason Thompson--University of Melbourne

## This repo uses MicroCosmic God Twitter bot list of tweets to grasp bibliographic information automatically using Zotero-translators

### The full file using current 'tweets.csv' from Jason Thompson is 'results.json'

### Initial analysis can be found in json_analysis.py

## To run

1. Install zotero-translators using `docker` and following instructions
2. Provide a list of URLs of interest. In our case: `tweets.csv`
3. Run `run_translator.sh`
   1. You will turn on the server, run the queries to the server, and kill the server
4. Then run: `sanity_checks.py`
5. Then run: `json_analysis.py`
6. And finally, 'making_interactive_graph_plot.py`


TODO: Check names with single initial and collapse them together

TODO: we might want to check zotero-translators export capabilities
