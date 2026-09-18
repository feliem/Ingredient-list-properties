import pubchempy as pcp
import pandas as pd
import re
import matplotlib.pyplot as plt

print("Enter your ingredient list.")
print("Type END on a new line when finished:")

lines = []

while True:
    line = input()

    if line.strip().upper() == "END":
        break

    lines.append(line)

text = "\n".join(lines)

# --------------------------------
# Parse ingredients
# --------------------------------

# Remove markdown links
molecules = re.findall(r'\[([^\]]+)\]\(', text)

# If no markdown links, parse as plain text
if not molecules:

    molecules = []

    for line in lines:

        # Remove Active/Inactive Ingredients labels
        line = re.sub(
            r'^\s*(?:Active|Inactive)\s+Ingredients\s*:\s*',
            '',
            line,
            flags=re.IGNORECASE
        )

        # Split by comma
        molecules.extend(line.split(','))


# Clean ingredients

cleaned_molecules = []

for molecule in molecules:

    # Remove zero-width spaces
    molecule = molecule.replace('\u200b', ' ')
    molecule = molecule.replace('/', ' ')

    # Remove percentage concentrations
    molecule = re.sub(r'\s*\([^)]*\d+\s*%\)', '', molecule)

    # Remove extra whitespace
    molecule = ' '.join(molecule.split())

    if molecule:
        cleaned_molecules.append(molecule)

molecules = cleaned_molecules

# print(molecules)


#Lists to store properties
id = []
names = []
weights = []
logP = []
inchikey = []
smiles = []

#Loop through compounds
for mol in molecules:

    try:
        compounds = pcp.get_compounds(mol, 'name')

        if not compounds:
            print(f"NOT FOUND: {mol}")
            continue

        compound = compounds[0]

        print(f"FOUND: {mol} → CID {compound.cid}")

    except Exception as e:
        print(f"ERROR searching {mol}: {e}")
        continue

    id.append(compound.cid)
    names.append(mol)
    weights.append(compound.molecular_weight)
    logP.append(compound.xlogp)
    inchikey.append(compound.inchikey)
    smiles.append(compound.connectivity_smiles)

#Create dataframe
data = {'CID' : id,
        'Name' : names,
        'Weights' : weights,
        'LogP' : logP,
        'InChiKey' : inchikey,
        'Canonical smiles' : smiles}

data = pd.DataFrame(data)

print(data.head())

# Check the info of the dataset
print(data.info())

# Check for missing values
print(data.isnull().sum())  



plt.figure(figsize=(8,6))

# Create the bar plot
plt.bar(data['CID'], data['LogP'], color='green', alpha=0.6)

# Overlay scatter plot to show individual points
plt.scatter(data['CID'], data['LogP'], color='red', s=100, label='LogP Points')

for _, row in data.iterrows():
    plt.annotate(
        row['Name'],
        (row['CID'], row['LogP']),
        xytext=(5, 5),
        textcoords='offset points'
    )

plt.title('LogP Values Across Compounds', fontsize=16)
plt.xlabel('Compound CID', fontsize=14)
plt.ylabel('LogP', fontsize=14)
plt.grid(True, axis='y')
plt.legend()

plt.show()
