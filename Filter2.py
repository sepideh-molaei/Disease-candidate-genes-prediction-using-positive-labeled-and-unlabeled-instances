import pandas as pd
import numpy as np

def calculate_gene_scores(gene_scores):
    gene_groups = [(gene, sr, (sr // 10) + 1) for gene, sr in gene_scores]
    min_group = min(group for _, _, group in gene_groups)
    max_group = max(group for _, _, group in gene_groups)
    fixed_number = 100 / (sum(range(min_group, max_group + 1)))
    result = [(gene, sr, group * fixed_number, sr * group * fixed_number) for gene, sr, group in gene_groups]
    return result

def process_gene_files(disease_files):
    for disease, file in disease_files.items():
        # Load the Excel file
        data = pd.read_excel(file)
        
        # Extract gene names and SR scores
        gene_scores = list(zip(data['Gene-Name'], data['ScoreValue']))
        
        # Calculate gene scores
        gene_scores_result = calculate_gene_scores(gene_scores)
        
        # Create a DataFrame from the results
        result_df = pd.DataFrame(gene_scores_result, columns=['Gene-Name', 'ScoreValue', 'GroupScore', 'GeneScore'])
        
        # Calculate the mean of GeneScores
        mean_gene_score = result_df['GeneScore'].mean()
        
        # Filter genes with GeneScore above the mean
        filtered_genes = result_df[result_df['GeneScore'] > mean_gene_score]
        
        # Save the filtered genes to a new Excel file
        output_file = f'{disease}_selected_genes.xlsx'
        filtered_genes.to_excel(output_file, index=False)
        print(f'Saved selected genes for {disease} to {output_file}')

# Dictionary of disease files
disease_files = {
    'Neurological': 'Neurological-SR.xlsx',
    'Heart Failure': 'Heart Failure-SR.xlsx',
    'Adrenal': 'Adrenal-SR.xlsx',
    'Prostate': 'Prostate-SR.xlsx',
    'Lung': 'Lung-SR.xlsx',
    'Colon': 'Colon-SR.xlsx'
}

# Process each disease file
process_gene_files(disease_files)
