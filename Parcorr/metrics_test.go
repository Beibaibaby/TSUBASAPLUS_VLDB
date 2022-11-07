package main

import (
	"testing"
)

func TestComputeAccuray(t *testing.T) {
	groundTruthPairs := []IDPair{{0, 1}, {0, 4}}
	outputPairs := []IDPair{{0, 1}}

	gtMatrix := computeCorrelationMatrix(groundTruthPairs, 5)
	outMatrix := computeCorrelationMatrix(outputPairs, 5)

	accuracy := computeAccuracy(gtMatrix, outMatrix)
	if accuracy != 0.9 {
		t.Fatal(accuracy)
	}
}
