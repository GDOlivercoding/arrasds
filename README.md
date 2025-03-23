Arras.io data science (analysis) from a google form

saved_figs: DIR
the directory when pngs of saved matplotlib figures will be

.gitignore
git ignore file

arrasds.csv:
the raw data values from the form
unfilltered, with all nazi, racist and nsfw comments from troll submittors

arrasds.json:
filtered, with invalid values filled with 'null'

sane_arrasds.json:
final formatted file, with values being narrowed
to their best types as much as possible

README.md:
read me

arrasds.py:
the file where matplotlib snippets are made

noplotanalysis.py:
data analysis without plotting with
all code lead to results shown

sanity_json_converter.py:
file to convert arrasds.json to sane_arrasds.json

voting results.txt:
file with pure voting results

actual ds.py:
actual data science, where statistics
arent shoved directly into my face
on a silver plater

csv_to_json.py:
convert csv (like arrasds.csv) to json (like arrasds.json)