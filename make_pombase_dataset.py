import pandas

mappings = pandas.read_csv('results/full_mappings.tsv', sep='\t', na_filter=False)[['condition', 'sensitive', 'fyeco_terms']]
conditions = set(mappings.condition)
# Transform the phenotype tables

phenotype_tables = list()

for paper_table in ['data/table2.tsv', 'data/table3.tsv']:
    data = pandas.read_csv(paper_table, sep='\t', na_filter=False).drop(columns=['primary_name'])
    phenotype_tables.append(data.melt(id_vars=['systematic_id'], var_name='condition', value_name='severity'))

data = pandas.concat(phenotype_tables)

data = data[~data.condition.isin(['MMS-cc', '4NQ-cc']) & ~data.severity.isin(['ND', '+'])]
# Normalise weird unicode chars
data.severity = data.severity.apply(lambda x: x.replace('−', '-'))
severity_dict = {'-': 'low', '--': 'medium', '---': 'high'}
data.severity = data.severity.apply(lambda x: severity_dict[x])

data = data.merge(mappings, on='condition', how='left')

data.rename(inplace=True, columns={
    'systematic_id': 'Gene systematic ID',
    'fyeco_terms': 'Condition',
    'sensitive': 'FYPO ID',
    'severity': 'Severity',
})


data['Allele description'] = 'deletion'
data['Expression'] = 'null'
data['Parental strain'] = '972 h-'
data['Background strain name'] = ''
data['Background genotype description'] = ''
data['Gene name'] = ''
data['Allele name'] = ''
data['Allele synonym'] = ''
data['Allele type'] = 'deletion'
data['Evidence'] = 'ECO:0001563'
data['Penetrance'] = ''
data['Extension'] = ''
data['Reference'] = 'PMID:15821139'
data['taxon'] = '4896'
data['Date'] = '2023-03-03'
data['Ploidy'] = 'haploid'
data['Allele variant'] = ''

column_order = [
    'Gene systematic ID',
    'FYPO ID',
    'Allele description',
    'Expression',
    'Parental strain',
    'Background strain name',
    'Background genotype description',
    'Gene name',
    'Allele name',
    'Allele synonym',
    'Allele type',
    'Evidence',
    'Condition',
    'Penetrance',
    'Severity',
    'Extension',
    'Reference',
    'taxon',
    'Date',
    'Ploidy',
    'Allele variant'
]

with open('results/pombase_dataset.tsv', 'w') as out:
    out.write('#Submitter_name: Manuel Lera-Ramirez\n#Submitter_ORCID: 0000-0002-8666-9746\n#Submitter_status: PomBase\n')
    data[column_order].to_csv(out, sep='\t', index=False, float_format='%.3f')