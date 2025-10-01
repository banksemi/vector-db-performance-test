def recall(ground_truth_neighbors, predicted_neighbors):
    return len(set(ground_truth_neighbors).intersection(set(predicted_neighbors))) / len(ground_truth_neighbors)