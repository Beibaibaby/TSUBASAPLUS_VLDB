package main

/*
TODO:
	1. stdev maybe zero
	2. Update timeSeries parameter by only passing needed range
	3. whether discard the last smaller window
	4. Remove startPos, instead, pass only needed length of time series (basicWindowSize + WindowSize)
	5. Where to timing
	6. test dataset
	7. efficiency of using goroutine
*/

import (
	"math"
	"math/rand"
	"time"
	// "reflect"
)


// struct for infos about a time series
type TimeSeriesProfile struct {
	id     int
	mean   float64
	stdev  float64
	sketch []float64
	data   []float64
}


// Utilty function to generate a matrix drawing from Random Signs
func computeRandomMatrix(vectorNum, vectorSize int) [][]int8 {
	rand.Seed(time.Now().UnixNano())
	randomMatrix := make([][]int8, vectorNum)

	for i := 0; i < vectorNum; i++ {
		randomMatrix[i] = make([]int8, vectorSize)
		for j := 0; j < vectorSize; j++ {
			num := int8(rand.Intn(2))
			if num == 0 {
				num = -1
			}
			randomMatrix[i][j] = num
		}
	}

	return randomMatrix
}

// Return a new random matrix by discarding the first updateSize values for each vector, and add updateSize values at the end
func updateRandomMatrix(randomMatrix [][]int8, updateSize int) [][]int8 {
	vectorNum, vectorSize := len(randomMatrix), len(randomMatrix[0])
	newRandomMatrix := make([][]int8, vectorNum)

	for i := 0; i < vectorNum; i++ {
		newRandomMatrix[i] = make([]int8, vectorSize)
		copy(newRandomMatrix[i], randomMatrix[i][updateSize:])
		for j := vectorSize - updateSize; j < vectorSize; j++ {
			num := int8(rand.Intn(2))
			if num == 0 {
				num = -1
			}
			newRandomMatrix[i][j] = num
		}
	}
	return newRandomMatrix
}

// Update sliding random matrix sum in a window incrementally
func updateSlidingRMSum(oldSlidingRandomMatrixSum []int, randomMatrix [][]int8) []int {
	sketchSize := len(oldSlidingRandomMatrixSum)
	newSlidingRandomMatrixSum := make([]int, sketchSize)
	copy(newSlidingRandomMatrixSum, oldSlidingRandomMatrixSum)

	for i := 0; i < sketchSize; i++ {
		for j := 0; j < basicWindowSize; j++ {
			newSlidingRandomMatrixSum[i] -= int(randomMatrix[i][j])
		}
		for j := windowSize; j < basicWindowSize+windowSize; j++ {
			newSlidingRandomMatrixSum[i] += int(randomMatrix[i][j])
		}
	}

	return newSlidingRandomMatrixSum
}

// Compute the sketch for the first window of a time series
func computeSketch(id int, timeSeries []float64, randomMatrix [][]int8, c chan TimeSeriesProfile) {
	mean, stdev := computeStats(timeSeries, 0)
	normTimeSeries := normalize(timeSeries, mean, stdev)
	sketch := make([]float64, sketchSize)
	for i := 0; i < sketchSize; i++ {
		for j := 0; j < windowSize; j++ {
			sketch[i] += normTimeSeries[j] * float64(randomMatrix[i][j])
		}
	}
	c <- TimeSeriesProfile{id, mean, stdev, sketch, timeSeries[:windowSize]}
}

// Update dot products (Sketches) based on statistics incrementally
func updateSketch(id int, timeSeries []float64, oldSRMSum, newSRMSum []int, randomMatrix [][]int8, prevTSProfile TimeSeriesProfile, startPos int, c chan TimeSeriesProfile) {
	newSketch := make([]float64, sketchSize)
	newMean, newStdev := updateStats(timeSeries, prevTSProfile.mean, prevTSProfile.stdev, startPos)

	deltaS := make([]float64, sketchSize)
	for i := 0; i < sketchSize; i++ {
		for j := startPos - basicWindowSize; j < startPos; j++ {
			offset := j - startPos + basicWindowSize
			deltaS[i] -= float64(randomMatrix[i][offset]) * timeSeries[j]
		}
		for j := startPos + windowSize - basicWindowSize; j < startPos+windowSize; j++ {
			offset := j - startPos + basicWindowSize
			deltaS[i] += float64(randomMatrix[i][offset]) * timeSeries[j]
		}
	}

	for i := 0; i < sketchSize; i++ {
		newSketch[i] = (prevTSProfile.stdev*prevTSProfile.sketch[i] + deltaS[i] +
			prevTSProfile.mean*float64(oldSRMSum[i]) - newMean*float64(newSRMSum[i])) / newStdev
	}

	c <- TimeSeriesProfile{id, newMean, newStdev, newSketch, timeSeries[startPos : startPos+windowSize]}
}

// Compute statistics (mean, stdev) in a window of a time series starting at startPos
func computeStats(timeSeries []float64, startPos int) (float64, float64) {
	sum := 0.0
	sumSq := 0.0
	for i := startPos; i < startPos+windowSize; i++ {
		sum += timeSeries[i]
		sumSq += timeSeries[i] * timeSeries[i]
	}

	mean := sum / float64(windowSize)
	stdev := math.Sqrt(sumSq/float64(windowSize) - mean*mean)

	return mean, stdev
}

// Update statistics (mean, stdev) incrementally based on previous value
func updateStats(timeSeries []float64, prevMean, prevStdev float64, startPos int) (float64, float64) {
	sumDelta := 0.0
	sumSqDelta := 0.0
	for i := startPos - basicWindowSize; i < startPos; i++ {
		sumDelta -= timeSeries[i]
		sumSqDelta -= timeSeries[i] * timeSeries[i]
	}
	for i := startPos + windowSize - basicWindowSize; i < startPos+windowSize; i++ {
		sumDelta += timeSeries[i]
		sumSqDelta += timeSeries[i] * timeSeries[i]
	}

	mean := prevMean + sumDelta/float64(windowSize)
	stdev := math.Sqrt(prevStdev*prevStdev + prevMean*prevMean - mean*mean + sumSqDelta/float64(windowSize))

	return mean, stdev
}

// Normalize the time series of the first window
func normalize(timeSeries []float64, mean, stdev float64) []float64 {
	normTimeSeries := make([]float64, windowSize)

	for i := 0; i < windowSize; i++ {
		normTimeSeries[i] = (timeSeries[i] - mean) / stdev
	}

	return normTimeSeries
}
