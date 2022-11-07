package main

import (
	"log"
	"time"
)

// Some parameters
var (
	windowSize      = 50
	basicWindowSize = 20
	sketchSize      = 10
	gridSize        = 10
	pearsonThr      = 0.7
	fractionThr     = 0.5
)

// Compute sketches and search similarity for all the time series across all the query windows
func parcorrSearch(allTimeSeries [][]float64) {

	// Special processing for the first windows
	_, randomMatrix, slidingRandomMatrixSum, tsProfiles := firstParcorrSearch(allTimeSeries)

	// Search the following windows
	timeSeriesSize := len(allTimeSeries[0])
	windowNum := (timeSeriesSize-windowSize)/basicWindowSize + 1
	for i := 1; i < windowNum; i++ {
		log.Println("Window:", i)
		_, randomMatrix, slidingRandomMatrixSum, tsProfiles = singleParcorrSearch(allTimeSeries, i*basicWindowSize, randomMatrix, slidingRandomMatrixSum, tsProfiles)
	}
}

// Special processing for the first ParCorr Search
func firstParcorrSearch(allTimeSeries [][]float64) (pairs []IDPair, randomMatrix [][]int8, slidingRandomMatrixSum []int, tsProfiles []TimeSeriesProfile) {
	timeSeriesNum := len(allTimeSeries)

	randomMatrix = computeRandomMatrix(sketchSize, windowSize+basicWindowSize)

	slidingRandomMatrixSum = make([]int, sketchSize)
	for i := 0; i < sketchSize; i++ {
		for j := 0; j < windowSize; j++ {
			slidingRandomMatrixSum[i] += int(randomMatrix[i][j])
		}
	}

	c := make(chan TimeSeriesProfile, timeSeriesNum)
	for i := 0; i < timeSeriesNum; i++ {
		go computeSketch(i, allTimeSeries[i], randomMatrix, c)
	}

	tsProfiles = make([]TimeSeriesProfile, timeSeriesNum)
	for i := 0; i < timeSeriesNum; i++ {
		tsProfile := <-c
		id := tsProfile.id
		tsProfiles[id] = tsProfile
	}
	log.Println("The First Window is Completed")

	pairs = ParallelMixing(tsProfiles)
	return
}

// normal ParCorr search after the first search
func singleParcorrSearch(allTimeSeries [][]float64, startPos int, randomMatrix [][]int8, slidingRandomMatrixSum []int, tsProfiles []TimeSeriesProfile) (pairs []IDPair, newRandomMatrix [][]int8, newSlidingRandomMatrixSum []int, newTSProfiles []TimeSeriesProfile) {
	timeSeriesNum := len(allTimeSeries)
	c := make(chan TimeSeriesProfile, timeSeriesNum)

	startTime := time.Now()
	newSlidingRandomMatrixSum = updateSlidingRMSum(slidingRandomMatrixSum, randomMatrix)
	for j := 0; j < timeSeriesNum; j++ {
		go updateSketch(j, allTimeSeries[j], slidingRandomMatrixSum, newSlidingRandomMatrixSum, randomMatrix, tsProfiles[j], startPos, c)
	}
	newRandomMatrix = updateRandomMatrix(randomMatrix, basicWindowSize)
	newTSProfiles = make([]TimeSeriesProfile, timeSeriesNum)
	for j := 0; j < timeSeriesNum; j++ {
		tsProfile := <-c
		id := tsProfile.id
		newTSProfiles[id] = tsProfile
	}
	duration := time.Since(startTime)
	log.Println("Sketches update completed, Costs", duration)

	startTime = time.Now()
	pairs = ParallelMixing(newTSProfiles)
	duration = time.Since(startTime)
	log.Println("Search completed, Costs", duration)

	return
}
