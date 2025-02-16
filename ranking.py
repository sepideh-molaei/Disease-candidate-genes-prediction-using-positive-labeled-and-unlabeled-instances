import numpy as np
import pandas as pd

def euclidean_distance(gene1, gene2):
    """Compute the Euclidean distance between two gene expression profiles."""
    return np.sqrt(np.sum((gene1 - gene2) ** 2))

def assign_score_relevance(unlabeled_data, disease_data):
    """Assign the Score-Relevance of the closest positive gene to each unlabeled gene."""
    sr_scores = []
    for gene in unlabeled_data:
        closest_gene = min(disease_data, key=lambda x: euclidean_distance(gene, x[1:]))
        sr_scores.append(closest_gene[1])
    return sr_scores

def process_unlabeled_genes(disease_files):
    results = {}
    for disease, file in disease_files.items():
        # Load disease gene data (selected positive genes)
        disease_data = pd.read_excel(f'{disease}_selected_genes.xlsx').to_numpy()
        
        # Load unlabeled gene data
        unlabeled_data = loadUnlabeledGenes(disease).to_numpy()[:, 1:]  # Convert to numpy array and exclude gene names
        
        # Get the trained binary model
        binary_model = results[disease]['binary_model']
        
        # Predict labels for unlabeled genes
        predicted_labels = binary_model.predict(unlabeled_data)
        
        # Compute decision function to get distances from the support vector
        distances = binary_model.decision_function(unlabeled_data)
        
        # Adjust distances based on labels: positive distance for positive label, negative for negative
        adjusted_distances = np.where(predicted_labels == 1, distances, -distances)
        
        # Assign Score-Relevance to each unlabeled gene based on the closest positive gene
        sr_scores = assign_score_relevance(unlabeled_data, disease_data)
        
        # Calculate final scores for each gene by multiplying SR score with adjusted distance
        final_scores = np.array(sr_scores) * adjusted_distances
        
        # Create a DataFrame from the results
        result_df = pd.DataFrame(unlabeled_data, columns=[f'Feature{i+1}' for i in range(unlabeled_data.shape[1])])
        result_df['Predicted_Label'] = predicted_labels
        result_df['Distance_from_Support_Vector'] = adjusted_distances
        result_df['SR_Score'] = sr_scores
        result_df['Final_Score'] = final_scores
        
        # Calculate the final score for each gene by summing the scores of its profiles
        result_df['Gene_Name'] = pd.read_excel(file)['Gene-Name']  # Assuming gene names are in the same order
        gene_final_scores = result_df.groupby('Gene_Name')['Final_Score'].sum().reset_index()
        
        # Sort genes by their final scores
        sorted_genes = gene_final_scores.sort_values(by='Final_Score', ascending=False)
        
        # Save the results to an Excel file
        output_file = f'{disease}_final_ranked_genes.xlsx'
        sorted_genes.to_excel(output_file, index=False)
        print(f'Saved final ranked genes for {disease} to {output_file}')

# Example dictionary of disease files
disease_files = {
    'Neurological': 'Neurological-SR.xlsx',
    'Heart Failure': 'Heart Failure-SR.xlsx',
    'Adrenal': 'Adrenal-SR.xlsx',
    'Prostate': 'Prostate-SR.xlsx',
    'Lung': 'Lung-SR.xlsx',
    'Colon': 'Colon-SR.xlsx'
}

# Process each disease file
process_unlabeled_genes(disease_files)

# Helper Functions
def loadUnlabeledGenes(disease):
    """Load unlabeled gene data related to the disease."""
    data = ...  # Implement this function
    return data
