package main

import (
	"math"
	"testing"
)

// Test for the correctness of incremental computing algorithm for mean and standard deviation
func TestUpdateStats(t *testing.T) {
	timeSeries := []float64{0, 7, 9, 5, 2, 8, 1, 7, 7, 5, 8, 9, 4, 8, 9, 8, 1, 1, 7, 4, 9, 7, 8, 7, 9, 8, 7, 7, 4, 8, 0, 1, 5, 3, 2, 7, 3, 6, 7, 0, 5, 6, 1, 9, 3, 4, 4, 4, 1, 0, 7, 0, 2, 1, 9, 3, 4, 8, 7, 3, 2, 7, 8, 4, 4, 2, 4, 5, 0, 2, 7, 8, 3, 6, 2, 4, 7, 2, 7, 0, 0, 3, 0, 2, 3, 8, 4, 4, 3, 1, 7, 0, 5, 0, 2, 8, 5, 9, 9, 4}

	mean, stdev := computeStats(timeSeries, 0)
	epsilon := 0.001
	for i := basicWindowSize; i+windowSize <= len(timeSeries); i += basicWindowSize {
		mean, stdev = updateStats(timeSeries, mean, stdev, i)
		refMean, refStdev := computeStats(timeSeries[i:], 0)
		// t.Log("Window: No.", i / basicWindowSize, mean, refMean, math.Abs(mean-refMean), stdev, refStdev, math.Abs(stdev-refStdev))
		if math.Abs(mean-refMean) > epsilon || math.Abs(stdev-refStdev) > epsilon {
			t.Fatal()
		}
	}
}


// Test for the correctness of incremental sketch computing
func TestUpdateSketch(t *testing.T) {
	timeSeries := []float64{0, 7, 9, 5, 2, 8, 1, 7, 7, 5, 8, 9, 4, 8, 9, 8, 1, 1, 7, 4, 9, 7, 8, 7, 9, 8, 7, 7, 4, 8, 0, 1, 5, 3, 2, 7, 3, 6, 7, 0, 5, 6, 1, 9, 3, 4, 4, 4, 1, 0, 7, 0, 2, 1, 9, 3, 4, 8, 7, 3, 2, 7, 8, 4, 4, 2, 4, 5, 0, 2, 7, 8, 3, 6, 2, 4, 7, 2, 7, 0, 0, 3, 0, 2, 3, 8, 4, 4, 3, 1, 7, 0, 5, 0, 2, 8, 5, 9, 9, 4}
	randomMatrix := computeRandomMatrix(sketchSize, windowSize+basicWindowSize)
	sum := make([]int, sketchSize)
	for i := 0; i < sketchSize; i++ {
		for j := 0; j < windowSize; j++ {
			sum[i] += int(randomMatrix[i][j])
		}
	}
	c := make(chan TimeSeriesProfile)
	go computeSketch(0, timeSeries, randomMatrix, c)
	tsProfile := <-c

	windowNum := (len(timeSeries) - windowSize) / basicWindowSize
	for i := 1; i < windowNum; i++ {
		newSum := updateSlidingRMSum(sum, randomMatrix)

		go updateSketch(0, timeSeries, sum, newSum, randomMatrix, tsProfile, i*basicWindowSize, c)

		tsProfile = <-c

		slicedRandomMatrix := make([][]int8, sketchSize)
		for j := 0; j < sketchSize; j++ {
			slicedRandomMatrix[j] = randomMatrix[j][basicWindowSize:]
		}
		go computeSketch(0, timeSeries[basicWindowSize*i:], slicedRandomMatrix, c)
		refProfile := <-c

		epsilon := 0.001
		for j := 0; j < sketchSize; j++ {
			if math.Abs(refProfile.sketch[j]-tsProfile.sketch[j]) > epsilon {
				t.Fatal()
			}
		}

		randomMatrix = updateRandomMatrix(randomMatrix, basicWindowSize)
		sum = newSum
	}

}