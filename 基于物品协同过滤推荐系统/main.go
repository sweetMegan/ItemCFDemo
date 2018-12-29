package main

import (
	"os"
	"bufio"
	"fmt"
	"log"
	"strings"
	"zhqGo/基于物品协同过滤推荐系统/itemCFEngine"
	"net/http"
)

func main() {
	fileName := "./data/ml-latest-small/ratings.csv"
	movies := readCSV("./data/ml-latest-small/movies.csv",",",true)
	itemCFEngine.CreateMoviesData(movies)
	data := readCSV(fileName, ",", true)
	//fmt.Println(data)
	itemCFEngine.CreateTrain(data)
	//fmt.Println(train)
	itemCFEngine.ItemSimilariy()
	//fmt.Println("--------",w["1"])
	//itemCFEngine.Recommendation("1",20)
	//开个服务
	http.HandleFunc("/test",getRecommendation)
	fmt.Println("服务已启动")
	err := http.ListenAndServe(":8080",nil)
	if err != nil {
		fmt.Println(err)
	}
}
func getRecommendation(w http.ResponseWriter, r *http.Request)  {
	userid := r.FormValue("userid")
	fmt.Println(userid)
	res := itemCFEngine.Recommendation(userid,20)
	w.Write(res)
}
/*
*读取CSV文件
*fileName:文件路径
*sep:分隔符
*hasHeader:是否包含标题
*/
func readCSV(fileName string, sep string, hasHeader bool) ([][]string) {
	data := [][]string{}
	file, err := os.Open(fileName)
	fmt.Println("fileName:", fileName)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()
	// Read CSV file
	scanner := bufio.NewScanner(file)
	//i := 0
	for scanner.Scan() {
		//读一行
		line := scanner.Text()
		//如果是标题，读取下一行
		if hasHeader {
			hasHeader = false
			continue
		}
		//按分隔符，分割数据
		fields := strings.Split(line, sep)
		data = append(data, fields)
	}
	return data
}
