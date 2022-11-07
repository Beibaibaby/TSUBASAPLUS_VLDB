package main

// Compute accuracy based on the Ground Truth and outputed positive samples
func computeAccuracy(matrix1, matrix2 [][]bool) float64 {
	size := len(matrix1)

	count := 0
	for i := 0; i < size; i++ {
		for j := i + 1; j < size; j++ {
			if matrix1[i][j] == matrix2[i][j] {
				count++
			}
		}
	}

	return float64(count) / float64(size*(size-1)/2)
}

// Compute accuracy from positive samples
func computeAccuracyFromPairs(pairs1, pairs2 []IDPair, maxID int) float64 {
	matrix1 := computeCorrelationMatrix(pairs1, maxID)
	matrix2 := computeCorrelationMatrix(pairs2, maxID)

	accuracy := computeAccuracy(matrix1, matrix2)

	return accuracy
}

// Comptue correlation matrix from highly correlated pairs
func computeCorrelationMatrix(pairs []IDPair, maxID int) [][]bool {
	matrix := make([][]bool, maxID)

	for i := 0; i < maxID; i++ {
		matrix[i] = make([]bool, maxID)
	}

	for _, pair := range pairs {
		matrix[pair.first][pair.second] = true
		matrix[pair.second][pair.first] = true
	}

	return matrix
}
