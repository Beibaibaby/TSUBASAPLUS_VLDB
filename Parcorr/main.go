package main

import (
	"flag"
	"log"
	"os"
	"time"

	"github.com/sbinet/npyio"
)

func main() {
	// allTimeSeries := [][]float64{
	// 	{0, 7, 9, 5, 2, 8, 1, 7, 7, 5, 8, 9, 4, 8, 9, 8, 1, 1, 7, 4, 9, 7, 8, 7, 9, 8, 7, 7, 4, 8, 0, 1, 5, 3, 2, 7, 3, 6, 7, 0, 5, 6, 1, 9, 3, 4, 4, 4, 1, 0, 7, 0, 2, 1, 9, 3, 4, 8, 7, 3, 2, 7, 8, 4, 4, 2, 4, 5, 0, 2, 7, 8, 3, 6, 2, 4, 7, 2, 7, 0, 0, 3, 0, 2, 3, 8, 4, 4, 3, 1, 7, 0, 5, 0, 2, 8, 5, 9, 9, 4},
	// 	{9, 7, 6, 8, 0, 9, 5, 7, 2, 2, 3, 6, 3, 8, 0, 7, 5, 7, 6, 0, 5, 9, 4, 8, 8, 5, 0, 7, 1, 6, 7, 2, 9, 9, 3, 6, 0, 9, 8, 6, 3, 9, 9, 4, 1, 7, 1, 2, 3, 5, 2, 2, 6, 9, 9, 9, 8, 4, 4, 4, 2, 3, 5, 7, 3, 1, 6, 8, 5, 7, 5, 1, 2, 2, 9, 0, 0, 7, 4, 1, 0, 7, 7, 5, 8, 9, 3, 7, 3, 7, 3, 8, 6, 6, 8, 1, 4, 9, 2, 4},
	// 	{1, 2, 4, 4, 8, 5, 2, 1, 7, 5, 4, 8, 3, 5, 9, 7, 7, 2, 3, 8, 1, 1, 8, 9, 4, 9, 7, 1, 5, 2, 7, 3, 6, 6, 0, 3, 5, 3, 5, 0, 8, 2, 7, 3, 0, 2, 3, 2, 5, 4, 1, 4, 6, 2, 1, 9, 6, 5, 3, 0, 0, 8, 9, 0, 3, 6, 4, 9, 8, 4, 3, 1, 5, 5, 3, 1, 2, 4, 2, 8, 0, 6, 3, 3, 1, 2, 4, 5, 1, 5, 9, 2, 1, 5, 1, 4, 4, 3, 3, 0},
	// 	{2, 5, 4, 5, 9, 3, 0, 4, 8, 1, 9, 1, 2, 5, 2, 1, 4, 7, 7, 1, 0, 0, 4, 3, 0, 8, 0, 1, 0, 1, 3, 2, 9, 2, 5, 0, 0, 8, 1, 7, 7, 4, 4, 1, 0, 4, 9, 9, 2, 5, 1, 3, 9, 1, 3, 0, 9, 8, 9, 8, 0, 5, 3, 6, 0, 8, 5, 0, 2, 0, 5, 1, 4, 0, 5, 8, 3, 9, 1, 1, 0, 4, 6, 0, 5, 4, 3, 7, 8, 4, 7, 7, 5, 1, 6, 9, 2, 6, 4, 8},
	// 	{3, 2, 7, 8, 3, 5, 4, 1, 2, 9, 4, 3, 0, 3, 1, 0, 3, 3, 8, 9, 8, 2, 0, 7, 2, 3, 8, 1, 6, 0, 5, 5, 7, 4, 8, 2, 1, 5, 1, 3, 5, 5, 4, 5, 7, 9, 1, 0, 6, 7, 6, 0, 9, 5, 4, 7, 8, 2, 1, 9, 5, 6, 2, 1, 6, 1, 4, 3, 8, 9, 4, 2, 3, 5, 2, 3, 1, 7, 9, 9, 9, 3, 9, 3, 8, 1, 5, 0, 9, 1, 0, 4, 2, 2, 2, 9, 5, 7, 5, 7},
	// 	{4, 7, 0, 5, 0, 2, 9, 3, 1, 4, 3, 1, 6, 7, 7, 2, 7, 5, 5, 6, 9, 2, 3, 4, 5, 4, 2, 1, 6, 5, 8, 7, 9, 3, 3, 9, 1, 2, 2, 9, 2, 4, 9, 6, 0, 7, 5, 7, 6, 9, 4, 8, 8, 7, 0, 1, 7, 3, 9, 3, 9, 1, 6, 9, 5, 6, 2, 5, 8, 6, 1, 9, 2, 7, 4, 2, 6, 3, 1, 2, 4, 9, 9, 6, 4, 5, 7, 4, 6, 5, 2, 2, 9, 6, 2, 7, 5, 0, 1, 9},
	// 	{3, 6, 8, 9, 5, 4, 9, 6, 0, 4, 7, 7, 4, 8, 8, 0, 7, 8, 4, 9, 6, 7, 1, 7, 5, 2, 1, 4, 5, 4, 1, 4, 6, 5, 8, 9, 8, 1, 4, 3, 3, 2, 5, 8, 7, 6, 2, 1, 4, 2, 9, 7, 4, 2, 0, 9, 5, 7, 0, 2, 1, 0, 9, 6, 2, 1, 6, 0, 7, 7, 5, 3, 1, 7, 0, 5, 9, 5, 6, 2, 9, 4, 9, 8, 8, 8, 9, 6, 5, 8, 3, 9, 0, 7, 5, 4, 0, 5, 6, 5},
	// 	{0, 4, 9, 2, 6, 8, 8, 0, 9, 5, 4, 5, 4, 1, 1, 3, 9, 3, 4, 2, 5, 3, 3, 0, 1, 4, 1, 6, 5, 9, 1, 9, 1, 0, 8, 3, 0, 8, 8, 2, 9, 9, 3, 2, 1, 9, 3, 1, 5, 2, 5, 6, 0, 8, 1, 6, 5, 9, 7, 9, 6, 5, 0, 7, 8, 6, 5, 9, 3, 0, 8, 0, 6, 3, 5, 5, 6, 2, 9, 0, 4, 6, 1, 6, 6, 8, 5, 1, 9, 0, 4, 2, 3, 5, 2, 5, 5, 6, 3, 6},
	// 	{1, 4, 8, 2, 6, 3, 9, 0, 1, 5, 8, 5, 6, 9, 3, 0, 4, 5, 2, 5, 7, 2, 6, 6, 9, 2, 3, 4, 9, 8, 1, 2, 6, 4, 5, 6, 3, 5, 5, 0, 6, 3, 7, 4, 6, 8, 8, 3, 9, 0, 8, 0, 8, 5, 4, 6, 8, 8, 5, 3, 1, 8, 4, 6, 0, 4, 2, 2, 8, 9, 7, 3, 9, 9, 4, 4, 5, 5, 7, 7, 8, 9, 4, 9, 8, 9, 1, 3, 8, 6, 1, 7, 5, 2, 2, 4, 3, 6, 3, 0},
	// 	{6, 7, 6, 7, 3, 8, 4, 6, 6, 7, 1, 6, 6, 0, 6, 2, 9, 5, 6, 4, 7, 5, 3, 7, 7, 5, 3, 4, 1, 6, 4, 2, 9, 8, 2, 1, 3, 5, 6, 6, 3, 9, 8, 4, 8, 4, 9, 7, 6, 1, 3, 0, 4, 9, 0, 6, 9, 3, 2, 4, 0, 7, 5, 5, 3, 9, 6, 3, 6, 5, 0, 5, 3, 0, 8, 4, 6, 9, 7, 5, 0, 0, 1, 0, 2, 9, 9, 1, 6, 6, 0, 4, 1, 8, 3, 0, 6, 3, 8, 6},
	// }
	// timeSeriesNum := len(allTimeSeries)

	// listOfFiles, err := os.ReadDir("Data")
	// if err != nil {
	// 	panic(err)
	// }

	// for _, file := range listOfFiles {
	// 	if strings.HasSuffix(file.Name(), ".txt") {
	// 		fmt.Println(file.Name())
	// 	}
	// }

	gridSizePtr := flag.Int("gridSize", 1, "Size of grid cell [Default: 1]")
	fractionThrPtr := flag.Float64("fractionThr", 0.5, "Fraction of grids of collocation [Default: 0.5]")

	flag.Parse()

	gridSize = *gridSizePtr
	fractionThr = *fractionThrPtr
	log.Println("gridSize:", gridSize, "fractionThr:", fractionThr)

	f, err := os.Open("Data/samples/data_prepared.npy")
	if err != nil {
		log.Fatal(err)
	}
	defer f.Close()
	log.Print("File opened: ", f.Name())

	var rawTimeSeries []float64
	r, err := npyio.NewReader(f)
	if err != nil {
		log.Fatal(err)
	}
	shape := r.Header.Descr.Shape
	err = r.Read(&rawTimeSeries)
	if err != nil {
		log.Fatal(err)
	}

	allTimeSeries := make([][]float64, shape[0])
	for i := 0; i < shape[0]; i++ {
		allTimeSeries[i] = make([]float64, shape[1])
		startPos := i * shape[1]
		copy(allTimeSeries[i], rawTimeSeries[startPos:startPos+shape[1]])
	}

	allTimeSeries = allTimeSeries[10:100]
	log.Println("Data loaded. Shape:", len(allTimeSeries), len(allTimeSeries[0]))
	log.Println()

	var (
		start      time.Time
		duration   time.Duration
		accuracies []float64
	)

	// Special processing for the first windows
	log.Println("ParCorr Start...")
	start = time.Now()
	computedPairs, randomMatrix, slidingRandomMatrixSum, tsProfiles := firstParcorrSearch(allTimeSeries)
	duration = time.Since(start)
	log.Println("ParCorr Finished. Costs ", duration)

	log.Println("Linear Search Start...")
	start = time.Now()
	gtPairs := singleLinearSearch(allTimeSeries, 0)
	duration = time.Since(start)
	log.Println("Linear Search Finished. Costs ", duration)

	accuracy := computeAccuracyFromPairs(computedPairs, gtPairs, len(allTimeSeries))
	accuracies = append(accuracies, accuracy)
	log.Println("Accuracy is", accuracy)
	log.Println()

	// Search the following windows
	timeSeriesSize := len(allTimeSeries[0])
	windowNum := (timeSeriesSize-windowSize)/basicWindowSize + 1
	for i := 1; i < windowNum; i++ {
		log.Println("Window:", i)

		log.Println("ParCorr Start...")
		start = time.Now()
		computedPairs, randomMatrix, slidingRandomMatrixSum, tsProfiles = singleParcorrSearch(allTimeSeries, i*basicWindowSize, randomMatrix, slidingRandomMatrixSum, tsProfiles)
		duration = time.Since(start)
		log.Println("ParCorr Finished. Costs ", duration)

		log.Println("Linear Search Start...")
		start = time.Now()
		gtPairs = singleLinearSearch(allTimeSeries, i*basicWindowSize)
		duration = time.Since(start)
		log.Println("Linear Search Finished. Costs ", duration)

		accuracy = computeAccuracyFromPairs(computedPairs, gtPairs, len(allTimeSeries))
		accuracies = append(accuracies, accuracy)
		log.Println("Accuracy is", accuracy)
		log.Println()
	}

	sum := 0.0
	for _, accuracy := range accuracies {
		sum += accuracy
	}
	log.Println("Overall Accuracy is: ", sum/float64(len(accuracies)))
}
