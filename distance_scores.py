import pandas as pd
import numpy as np

def calculate_distance_scores(distances):
    """
    Calculate the distance scores for each gene based on their distance from the support vector.
    """
    # Group and score genes based on their distances
    gene_groups = [(distance, (distance // 1) + 1) for distance in distances]
    min_group = min(group for _, group in gene_groups)
    max_group = max(group for _, group in gene_groups)
    fixed_number = 200 / (max_group * (max_group + 1))
    result = [(distance, group * fixed_number, distance * group * fixed_number) for distance, group in gene_groups]
    return result

def process_unlabeled_genes(disease_files):
    results = {}
    for disease in disease_files:
        # Load the unlabeled gene data
        unlabeled_data = loadUnlabeledGenes(disease).to_numpy()[:, 1:]  # Convert to numpy array and exclude gene names
        
        # Get the trained binary model
        binary_model = results[disease]['binary_model']
        
        # Predict labels for unlabeled genes
        predicted_labels = binary_model.predict(unlabeled_data)
        
        # Compute decision function to get distances from the support vector
        distances = binary_model.decision_function(unlabeled_data)
        
        # Adjust distances based on labels: positive distance for positive label, negative for negative
        adjusted_distances = np.where(predicted_labels == 1, distances, -distances)
        
        # Calculate distance scores
        distance_scores_result = calculate_distance_scores(adjusted_distances)
        
        # Create a DataFrame from the results
        result_df = pd.DataFrame(unlabeled_data, columns=[f'Feature{i+1}' for i in range(unlabeled_data.shape[1])])
        result_df['Predicted_Label'] = predicted_labels
        result_df['Distance_from_Support_Vector'] = adjusted_distances
        result_df['Distance_Score'] = [score for _, _, score in distance_scores_result]
        
        # Save the results to an Excel file
        output_file = f'{disease}_predicted_distance_scores.xlsx'
        result_df.to_excel(output_file, index=False)
        print(f'Saved predicted distance scores for {disease} to {output_file}')

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
    """
    Load unlabeled gene data related to the disease.
    """
    data = ...  # Implement this function
    return data
