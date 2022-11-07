package main

import (
	"testing"
)

func TestPM(t *testing.T) {
	sketches := [][]float64 {
		{11, 12, 23, 24, 15, 16, 19, 20, 34, 10},
		{11, 12, 13, 14, 15, 16, 20, 19, 34, 10},
		{21, 22, 13, 14, 25, 26, 19, 20, 34, 10},
		{21, 22, 13, 14, 25, 26, 20, 19, 34, 10},
		{11, 12, 33, 34, 25, 26, 19, 20, 10, 34},
		{31, 32, 33, 34, 15, 16, 20, 19, 34, 10},
		{21, 22, 33, 34, 15, 16, 19, 20, 10, 34},
	}

	tsProfiles := []TimeSeriesProfile{}
	for i := 0; i < len(sketches); i++ {
		mean, stdev := computeStats(sketches[i], 0)
		tsProfiles = append(tsProfiles, TimeSeriesProfile{i, mean, stdev, sketches[i], sketches[i]})
	}

	ParallelMixing(tsProfiles)
}