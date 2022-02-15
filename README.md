# condenseBibtex
Removes entries from a .bib file that were not used by your .tex file. It uses the .aux file to find only citations that you actually used in your .tex files, and generates a new .bib file from it.

# Usage
python condenseBibtex.py --bib bibFile.bib --aux auxFile.aux --output _newBib.bib

# Limitations
The .bib file parser "getAllBibEntries(...)" was thrown together without much testing. You could rewrite this with something like pyparsing for more robust results. 
