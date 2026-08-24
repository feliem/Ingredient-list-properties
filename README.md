# Ingredient-list-properties
Analyzing properties of molecules, such as in an ingredient list

- Cleans data (see step 2 and 3)
- Search conducted through PubChem
- Shows Log P values against compound CID / how lipophilic or hydrophilic each compound is

1. Run the code
2. Enter list of ingredients, newline (type Enter), then type "END" <br>

   eg.<br>
   > Aqua/​, Citric Acid, Persea Gratissima (Avocado) Oil <br>
   > END
4. Parsed ingredients are directly searched from PubChem <br>

    eg. <br>
   > FOUND: Aqua → CID 962 <br>
   > FOUND: Citric Acid → CID 311 <br>
   > NOT FOUND: Persea Gratissima (Avocado) Oil
5. See scatterplot of Log P against compound CID

Limitations:
- Parsed ingredients must produce discrete search results from PubChem to be displayed in scatterplot
- Does not account for synonyms
