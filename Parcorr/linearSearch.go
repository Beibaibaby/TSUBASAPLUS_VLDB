package main

import (
	"log"
)

func linearSearch(allTimeSeries [][]float64) {
	timeSeriesSize := len(allTimeSeries[0])

	windowNum := (timeSeriesSize-windowSize)/basicWindowSize + 1
	for i := 0; i < windowNum; i++ {
		log.Println("Window: ", i)
		singleLinearSearch(allTimeSeries, basicWindowSize*i)
	}
}

func singleLinearSearch(allTimeSeries [][]float64, startPos int) []IDPair {
	pairs := []IDPair{}
	timeSeriesNum := len(allTimeSeries)

	tsProfiles := make([]TimeSeriesProfile, timeSeriesNum)
	for i := 0; i < timeSeriesNum; i++ {
		mean, stdev := computeStats(allTimeSeries[i], startPos)
		tsProfiles[i] = TimeSeriesProfile{i, mean, stdev, []float64{}, allTimeSeries[i][startPos : startPos+windowSize]}
	}

	for i := 0; i < timeSeriesNum; i++ {
		for j := i + 1; j < timeSeriesNum; j++ {
			pearson := computePearson(tsProfiles[i], tsProfiles[j])
			if pearson >= pearsonThr {
				// log.Println(i, j, pearson)
				pairs = append(pairs, IDPair{i, j})
			}
		}
	}
	log.Println("Number of pairs found:", len(pairs))

	return pairs
}

func parallelSingleLinearSearch(allTimeSeries [][]float64, startPos int) []IDPair {
	pairs := []IDPair{}
	timeSeriesNum := len(allTimeSeries)

	for i := 0; i < timeSeriesNum; i++ {
		mean1, stdev1 := computeStats(allTimeSeries[i], startPos)
		tsProfile1 := TimeSeriesProfile{i, mean1, stdev1, []float64{}, allTimeSeries[i][startPos : startPos+windowSize]}
		for j := i + 1; j < timeSeriesNum; j++ {
			mean2, stdev2 := computeStats(allTimeSeries[j], startPos)
			tsProfile2 := TimeSeriesProfile{i, mean2, stdev2, []float64{}, allTimeSeries[j][startPos : startPos+windowSize]}

			pearson := computePearson(tsProfile1, tsProfile2)
			if pearson >= pearsonThr {
				// log.Println(i, j, pearson)
				pairs = append(pairs, IDPair{i, j})
			}
		}
	}

	log.Println("Number of pairs found:", len(pairs))

	return pairs
}

// func singleTSLinearSearch(tsProfile1 TimeSeriesProfile, ts2 int, c chan<- IDPair) {

// }
