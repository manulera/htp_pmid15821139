import pandas
import json
from pronto import Ontology
import re

fyeco_ontology = Ontology('data/fyeco.obo')

with open('data/fypo-edit-dict.json') as ins:
    fypo = json.load(ins)

mappings = pandas.read_csv('mappings/mappings_table.tsv', sep='\t', na_filter=False)

mappings['sensitive_label'] = mappings['sensitive'].apply(lambda x: fypo[x])
mappings['resistance_label'] = mappings['resistance'].apply(lambda x: fypo[x])

def formatting_function(fyeco_terms):

    fyeco_terms_no_parenthesis = re.sub('\(.+?\)', '', fyeco_terms)
    out = list()
    for fyeco_term in fyeco_terms_no_parenthesis.split(','):
        out.append(fyeco_ontology[fyeco_term].name)
    return '|'.join(out)

mappings['fyeco_labels'] = mappings['fyeco_terms'].apply(formatting_function)

mappings.to_csv('results/full_mappings.tsv', sep='\t', index=False)
