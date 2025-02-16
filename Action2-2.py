import numpy as np

def euclidean_distance(gene1, gene2):
    """
    Compute the Euclidean distance between two gene expression profiles.
    """
    return np.sqrt(np.sum((gene1 - gene2) ** 2))

def calculate_min_distances(disease_genes, negative_genes):
    """
    Compute the minimum Euclidean distance of each negative gene from the disease genes.
    """
    min_distances = []
    for neg_gene in negative_genes:
        distances = [euclidean_distance(neg_gene, dis_gene) for dis_gene in disease_genes]
        min_distances.append(min(distances))
    return np.array(min_distances)

def sort_negative_genes_by_distance(disease_genes, negative_genes):
    """
    Sort the negative genes based on their minimum distance from the disease genes.
    """
    min_distances = calculate_min_distances(disease_genes, negative_genes)
    sorted_indices = np.argsort(min_distances)  # Sort in ascending order
    sorted_negative_genes = negative_genes[sorted_indices]
    return sorted_negative_genes
