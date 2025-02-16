% List of diseases
diseases = {'Neurological', 'Heart Failure', 'Adrenal', 'Prostate', 'Lung', 'Colon'};

% Prepare grid search for each model
param_grid = struct( ...
    'ParzenWindow', struct('h', [0.1, 0.5, 1]), ...
    'RobustGaussian', struct('Tol', [0.01, 0.05, 0.1]), ...
    'KNN', struct('K', [3, 5, 7, 10]), ...
    'SVDD', struct('ɤ', [0.1, 1, 10], 'kernel', {'linear', 'rbf'}) ...
);

% Initialize a structure to store results for each disease
results = struct();

% Loop through each disease to train models
for i = 1:length(diseases)
    disease = diseases{i};
    fprintf('Processing %s...\n', disease);
    
    % Load the disease data for positive samples
    pos_data = loadDiseaseData(disease); % Custom function to load the data
    
    % Remove common genes from other diseases (for test data)
    neg_data = removeCommonGenes(disease, diseases); % Custom function to get other diseases' data
    
    % Perform grid search for each model
    best_model = '';
    best_accuracy = -Inf;
    best_params = struct();

    % 1. Parzen Window
    best_h = 0.1;  % Initialize default h
    for h = param_grid.ParzenWindow.h
        model = parzenWindowTrain(pos_data, h);
        accuracy = evaluateModel(model, neg_data);
        accuracy = round(accuracy, 3);  % Round to three decimal places
        if accuracy > best_accuracy
            best_accuracy = accuracy;
            best_model = model;
            best_params.ParzenWindow = struct('h', h);
        end
    end
    
    % 2. Robust Gaussian
    best_tol = 0.01; % Initialize default tolerance
    for tol = param_grid.RobustGaussian.Tol
        model = robustGaussianTrain(pos_data, tol);
        accuracy = evaluateModel(model, neg_data);
        accuracy = round(accuracy, 3);  % Round to three decimal places
        if accuracy > best_accuracy
            best_accuracy = accuracy;
            best_model = model;
            best_params.RobustGaussian = struct('Tol', tol);
        end
    end
    
    % 3. KNN
    best_k = 3; % Initialize default K
    for k = param_grid.KNN.K
        model = knnTrain(pos_data, k);
        accuracy = evaluateModel(model, neg_data);
        accuracy = round(accuracy, 3);  % Round to three decimal places
        if accuracy > best_accuracy
            best_accuracy = accuracy;
            best_model = model;
            best_params.KNN = struct('K', k);
        end
    end
    
    % 4. SVDD
    best_ɤ = 0.1;  % Initialize default ɤ
    best_kernel = 'linear'; % Initialize default kernel
    for ɤ = param_grid.SVDD.ɤ
        for kernel = param_grid.SVDD.kernel
            model = svddTrain(pos_data, ɤ, kernel);
            accuracy = evaluateModel(model, neg_data);
            accuracy = round(accuracy, 3);  % Round to three decimal places
            if accuracy > best_accuracy
                best_accuracy = accuracy;
                best_model = model;
                best_params.SVDD = struct('ɤ', ɤ, 'kernel', kernel);
            end
        end
    end
    
    % Store the best model and parameters for this disease
    results.(disease).best_model = best_model;
    results.(disease).best_accuracy = best_accuracy;
    results.(disease).best_params = best_params;
    
    fprintf('Best model for %s: %s with accuracy: %.3f%%\n', disease, best_model, best_accuracy * 100);
end

% Helper Functions
function data = loadDiseaseData(disease)
    % Custom function to load data for a specific disease
    % Example: data = load('Neurological_data.mat');
    data = ...; % Replace with actual loading logic
end

function neg_data = removeCommonGenes(current_disease, all_diseases)
    % Custom function to remove common genes between diseases for testing
    % Example: Use a union/intersection operation to filter out common genes
    neg_data = ...; % Replace with actual filtering logic
end

function model = parzenWindowTrain(data, h)
    % Train the Parzen Window model
    model = ...; % Implement Parzen Window training
end

function model = robustGaussianTrain(data, tol)
    % Train the Robust Gaussian model
    model = ...; % Implement Robust Gaussian training
end

function model = knnTrain(data, k)
    % Train the KNN model
    model = ...; % Implement KNN training
end

function model = svddTrain(data, ɤ, kernel)
    % Train the SVDD model
    model = ...; % Implement SVDD training
end

function accuracy = evaluateModel(model, neg_data)
    % Evaluate the model on negative samples (other diseases)
    accuracy = ...; % Implement model evaluation logic
end
