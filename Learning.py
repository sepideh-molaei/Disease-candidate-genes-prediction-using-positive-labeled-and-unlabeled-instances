from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
import numpy as np

def train_binary_model(pos_data, reliable_negatives):
    """
    Train a binary classification model using positive data and reliable negative data with 10-fold cross-validation.
    """
    # Combine positive and reliable negative samples
    train_data = np.vstack((pos_data, reliable_negatives))
    labels = np.hstack((np.ones(len(pos_data)), -1 * np.ones(len(reliable_negatives))))
    
    # Set the parameter grid for C and gamma
    param_grid = {
        'C': [0.01],
        'gamma': [0.01],
        'kernel': ['rbf']
    }
    
    # Perform grid search with cross-validation
    grid_search = GridSearchCV(SVC(), param_grid, cv=10)
    grid_search.fit(train_data, labels)
    
    # Get the best model
    best_model = grid_search.best_estimator_
    
    return best_model

# List of diseases
diseases = {'Neurological', 'Heart Failure', 'Adrenal', 'Prostate', 'Lung', 'Colon'}

# Train the binary model for each disease
for disease in diseases:
    # Load positive gene data for the disease (selected positive genes)
    pos_data = pd.read_excel(f'{disease}_selected_genes.xlsx').to_numpy()[:, 1:]  # Convert to numpy array and exclude gene names
    
    # Select reliable negative genes (equal to number of positive genes) from sorted negative genes
    reliable_negatives = results[disease]['reliable_negative_genes'][:len(pos_data)]
    
    # Train the binary model
    binary_model = train_binary_model(pos_data, reliable_negatives)
    
    # Store the model
    results[disease]['binary_model'] = binary_model
    
    print(f"Finished training binary model for {disease}")

