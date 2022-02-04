# CondenseBibFromAux
Removes entries from a .bib file that were not used by your .tex file. It uses the .aux file to find only the used citations, and generates a new .bib file from it.

# Usage:
python condenseBibFromAux.py --bib bibFile.bib --aux auxFile.aux --output _newBib.bib
