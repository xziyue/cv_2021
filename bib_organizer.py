import bibtexparser
import sys
import os
import itertools

if len(sys.argv) != 5:
    raise RuntimeError('This program expects 4 arguments')

if not os.path.exists(sys.argv[1]):
    raise RuntimeError("input file '{}' does not exist".format(sys.argv[1]))

with open(sys.argv[1], 'r') as infile:
    bib_db = bibtexparser.load(infile)

bib_db.entries.sort(key=lambda x : int(x['year']), reverse=True)

search_names = sys.argv[2].split(';')
for i in range(len(search_names)):
    search_names[i] = search_names[i].strip()

name_sep = [' ', ',']
search_names_repl = dict()
for name in search_names:
    new_name = ''
    last_str = ''
    for c in name:
        if c not in name_sep:
            last_str += c
        else:
            if len(last_str) > 0:
                new_name += '\\textbf{%s}' % last_str
            last_str = ''
            new_name += c
    if len(last_str) > 0:
        new_name += '\\textbf{%s}' % last_str
    search_names_repl[name] = new_name

for entry in bib_db.entries:
    name_found = False
    for name in search_names:
        if name in entry['author']:
            entry['author'] = entry['author'].replace(name, search_names_repl[name])
            name_found = True
            break
    if not name_found:
        raise RuntimeError("unable to find author to highlight for entry '{}'".format(entry['ID']))

output_lines = []
year_encountered = []

hangparas_template = r'''
\begin{cvbiblist}
%s
\end{cvbiblist}
'''

for entry in bib_db.entries:
    year = entry['year'].strip()
    if year not in year_encountered:
        output_lines.append('\\CVBibYear{%s}'%year)
        year_encountered.append(year)
    output_lines.append('\\fullcite{%s}'%entry['ID'])

with open(sys.argv[3], 'w') as outfile:
    bibtexparser.dump(bib_db, outfile)

with open(sys.argv[4], 'w') as outfile:
    item_lines = ['\\item' + x for x in output_lines]
    content_lines = '\n'.join(item_lines)
    outfile.write(hangparas_template % content_lines)