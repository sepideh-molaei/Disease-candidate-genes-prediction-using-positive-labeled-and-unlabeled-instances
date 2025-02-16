import pandas as pd
import numpy as np

# Function to normalize the data
def normalize_row(row):
    X_max = row.max()  # Maximum value in the row
    X_min = row.min()  # Minimum value in the row
    if X_max == X_min:  # If all values are the same, no normalization is performed
        return row
    return (X_max - row) / (X_max - X_min)  # Apply the normalization formula

# List of disease file names (replace with your actual file paths)
disease_files = {
    'Neurological': 'Neurological.xlsx',
    'Heart Failure': 'Heart Failure.xlsx',
    'Adrenal': 'Adrenal.xlsx',
    'Prostate': 'Prostate.xlsx',
    'Lung': 'Lung.xlsx',
    'Colon': 'Colon.xlsx',
}

# Reading the disease files and normalizing the data
df_diseases_normalized = {}

for disease, file_path in disease_files.items():
    df = pd.read_excel(file_path)  # Load the disease file
    df_normalized = df.apply(normalize_row, axis=1)  # Normalize the data for this disease
    df_diseases_normalized[disease] = df_normalized  # Save the normalized data

# Now, compute the "Cancer" gene set based on Colon, Lung, and Prostate
colon_genes = set(pd.read_excel(disease_files['Colon'])['Gene'])  # Replace 'Gene' with the actual gene column name
lung_genes = set(pd.read_excel(disease_files['Lung'])['Gene'])  # Replace 'Gene' with the actual gene column name
prostate_genes = set(pd.read_excel(disease_files['Prostate'])['Gene'])  # Replace 'Gene' with the actual gene column name

# Union of the three disease genes
union_genes = colon_genes.union(lung_genes, prostate_genes)

# Intersection of the three disease genes
intersection_genes = colon_genes.intersection(lung_genes, prostate_genes)

# Cancer genes will be the union minus the intersection
cancer_genes = union_genes - intersection_genes

# Create a DataFrame for Cancer and normalize it
df_cancer = pd.DataFrame(list(cancer_genes), columns=['Gene'])
df_cancer_normalized = df_cancer.apply(normalize_row, axis=1)

# Save the normalized disease data and the Cancer data to an Excel file
with pd.ExcelWriter('normalized_data.xlsx') as writer:
    # Write each disease's normalized data to a separate sheet
    for disease, normalized_data in df_diseases_normalized.items():
        normalized_data.to_excel(writer, sheet_name=f'{disease} Normalized', index=False)

    # Write the Cancer data to a new sheet
    df_cancer_normalized.to_excel(writer, sheet_name='Cancer Normalized', index=False)

print("Normalization completed and saved to 'normalized_data.xlsx'.")
