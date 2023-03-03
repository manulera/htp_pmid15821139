"""
Converts an ontology in owl format to a json dictionary in which keys are the term ids and values are:

for first output: the term labels.
for second output: chebi terms contained in the logical definition

Expected usage is:

python ontology_to_term_dict.py data/fypo-edit.owl data/fypo-edit-dict.json data/fypo-edit-chebi-dict.json
"""

import json
import sys
import re

def main(input_file, output_file1, format):
    out_dictionary = dict()
    with open(input_file, 'r') as ins:
        for line in ins:
            line = line.strip()
            re_match = re.match(r'# Class: <http://purl.obolibrary.org/obo/FYPO_(\d+)> \((.+?)\)', line)
            if re_match:
                g = re_match.groups()
                out_dictionary['FYPO:' + g[0]] = g[1]

    with open(output_file1, 'w') as out:
        json.dump(out_dictionary, out, indent=4)


if __name__ == "__main__":

    main(sys.argv[1], sys.argv[2])
