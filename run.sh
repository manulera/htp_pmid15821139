# Download necessary files
bash get_data.sh
# Create a fypo term id - fypo term label dictionary in json
python ontology_to_term_dict.py data/fypo-edit.owl data/fypo-edit-dict.json
# Create the full_mappings.tsv file. It's redundant with mappings_table.tsv, but it is useful to verify that the FYPO and FYECO terms are correct
python make_full_mappings.py
# Create the pombase dataset
python make_pombase_dataset.py
