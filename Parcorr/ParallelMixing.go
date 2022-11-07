package main

/*
	1. window size must be even
*/

import (
	"fmt"
	"log"
	"sort"
)

// pair for storing a subvector of a sketch
type SubvectorProfile struct {
	id            int
	first, second float64
}

type IDPair struct {
	first, second int
}

func (p IDPair) String() string {
	return fmt.Sprintf("(%v, %v)", p.first, p.second)
}

// return all the highly correlated pairs
func ParallelMixing(tsProfiles []TimeSeriesProfile) []IDPair {
	tsNum := len(tsProfiles)

	// one channel for each subvector at the same position to return all its pairs
	pairsChans := make([]chan SubvectorProfile, sketchSize/2)
	for i := 0; i < len(pairsChans); i++ {
		pairsChans[i] = make(chan SubvectorProfile, tsNum)
	}

	for i := 0; i < tsNum; i++ {
		go partition(tsProfiles[i], pairsChans)
	}

	// one channel for each time series to return a list of candidate ids
	idsChans := make([]chan []int, tsNum)
	for i := 0; i < len(idsChans); i++ {
		idsChans[i] = make(chan []int, sketchSize/2)
	}

	for i := 0; i < len(pairsChans); i++ {
		go mapping(pairsChans[i], idsChans)
	}

	// one channel for each time series to return highly correlated pairs (a list of idPairs)
	candidatesPairChans := make([]chan []IDPair, tsNum)
	for i := 0; i < len(candidatesPairChans); i++ {
		candidatesPairChans[i] = make(chan []IDPair, 1)
	}

	for i := 0; i < tsNum; i++ {
		go counter(i, idsChans[i], candidatesPairChans[i])
	}

	// Receive all the candidate correlated pairs
	pairs := []IDPair{}
	candidatesNum := 0
	for i := 0; i < tsNum; i++ {
		tsPair := <-candidatesPairChans[i]
		// Emit all pairs of candidates
		for j := 0; j < len(tsPair); j++ {
			candidatesNum++
			ts1, ts2 := tsPair[j].first, tsPair[j].second
			pearson := computePearson(tsProfiles[ts1], tsProfiles[ts2])
			if pearson >= pearsonThr {
				pairs = append(pairs, IDPair{ts1, ts2})
				// log.Println(ts1, ts2, pearson)
			}
		}
	}
	log.Println("Number of candidate pairs found: ", candidatesNum)
	log.Println("Number of pairs found: ", len(pairs))

	return pairs
}

// partition the sketch of a time series and send them to mapping
func partition(tsProfile TimeSeriesProfile, c []chan SubvectorProfile) {
	tsSize := len(tsProfile.sketch)
	for i := 0; i < tsSize/2; i++ {
		c[i] <- SubvectorProfile{tsProfile.id, tsProfile.sketch[i*2], tsProfile.sketch[i*2+1]}
	}
}

// map same subvector at the same position to the same cell in the grid
func mapping(pairProfileChan <-chan SubvectorProfile, idsChans []chan []int) {
	type pair struct {
		first, second int
	}
	tsNums := len(idsChans)
	pairToIDs := make(map[pair][]int)

	for i := 0; i < tsNums; i++ {
		pairProfile := <-pairProfileChan
		key := pair{int(pairProfile.first) / gridSize, int(pairProfile.second) / gridSize}
		pairToIDs[key] = append(pairToIDs[key], pairProfile.id)
	}

	// TODO: no need to sort actually, but actual runtime difference is uncertain
	for key := range pairToIDs {
		sort.Ints(pairToIDs[key])
	}

	for key := range pairToIDs {
		n := len(pairToIDs[key])
		for i := 0; i < n; i++ {
			candidates := []int{}
			for j := i + 1; j < n; j++ {
				candidates = append(candidates, pairToIDs[key][j])
			}
			idsChans[pairToIDs[key][i]] <- candidates
		}
	}
}

// count number of the same subvectors
func counter(id int, idsC <-chan []int, pairsC chan<- []IDPair) {
	// counting
	count := make(map[int]int)
	for i := 0; i < sketchSize/2; i++ {
		for _, cand := range <-idsC {
			count[cand]++
		}
	}

	// check fraction
	pairs := []IDPair{}
	for candiID, num := range count {
		if float64(num)/float64(sketchSize)*2 >= fractionThr {
			pairs = append(pairs, IDPair{id, candiID})
		}
	}

	pairsC <- pairs
}

// compute Pearson correlation (needs mean, stdev and sequence)
func computePearson(tsProfile1, tsProfile2 TimeSeriesProfile) float64 {
	n := len(tsProfile1.data)
	mean1, mean2 := tsProfile1.mean, tsProfile2.mean
	stdev1, stdev2 := tsProfile1.stdev, tsProfile2.stdev

	sum := 0.0
	for i := 0; i < n; i++ {
		delta1 := tsProfile1.data[i] - mean1
		delta2 := tsProfile2.data[i] - mean2
		sum += delta1 * delta2
	}

	return sum / float64(n) / stdev1 / stdev2
}
