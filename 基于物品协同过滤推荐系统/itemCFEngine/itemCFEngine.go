package itemCFEngine

import (
	"zhqGo/基于物品协同过滤推荐系统/model"
	"strconv"
	"math"
	"sort"
	"encoding/json"
)

var train = make(map[string]map[string]model.Movie)
var W = make(map[string]map[string]float64)
var moviesData = make(map[string]model.Movie)

func CreateTrain(data [][]string) (map[string]map[string]model.Movie) {
	for _, item := range data {
		movie := model.Movie{}
		userid := ""
		for i, value := range item {
			//userId,movieId,rating,timestamp
			switch i {
			case 0:
				{
					userid = value
					if _, ok := train[userid]; !ok {
						train[userid] = make(map[string]model.Movie)
					}
				}
			case 1:
				{
					movie.MovieId = value
				}
			case 2:
				{
					rating, _ := strconv.ParseFloat(value, 32)
					movie.Rating = rating
				}
			case 3:
				{
					movie.TimeStamp = value
				}
			}
		}
		// 用户浏览过的物品的集合
		train[userid][movie.MovieId] = movie
	}
	return train
}

//创建用户-物品倒排表
func ItemSimilariy() (map[string]map[string]float64) {
	//同时喜欢物品i和物品j的用户数
	C := make(map[string]map[string]float64)
	// 喜欢物品i的用户数
	N := make(map[string]float64)
	for _, items := range train {
		//i: movieId
		for i, movie := range items {
			N[i] += movie.Rating
			for j, _ := range items {
				if i == j {
					continue
				}
				if _, ok := C[i]; !ok {
					C[i] = make(map[string]float64)
				}
				C[i][j] += 1 / math.Log(1+float64(len(items))*1.0)
			}
		}
	}
	for i, related_Items := range C {
		Max := 0.0
		for j, cij := range related_Items {
			if _, ok := W[i]; !ok {
				W[i] = make(map[string]float64)
			}
			W[i][j] = cij / float64(math.Sqrt(N[i]*N[j]))
			if W[i][j] > Max {
				Max = W[i][j]
			}
		}
		if Max != 0 {
			W[i] = norm(W[i], Max)
		}
	}
	return W
}

/*物品归一化*/
func norm(wi map[string]float64, Max float64) (map[string]float64) {
	res := make(map[string]float64)
	for j, value := range wi {
		res[j] = value / Max
	}
	return res
}

/*
*K:与物品j最相近的K个物品的
*/
func Recommendation(userId string, K int) ([]byte) {
	rank := make(map[string]float64)
	//ru 用户浏览过的物品
	ru := train[userId]
	for movieId, _ := range ru {
		// 将与物品i相近的物品排序
		//1、 将字典转切片
		temp := make(model.PairList, len(W[movieId]))
		for k, v := range W[movieId] {
			temp = append(temp, model.Pair{k, v})
		}
		sort.Sort(sort.Reverse(temp))
		//2、取出与物品i最相近的前K个物品j,加入到推荐列表
		if K >= len(temp)-1 {
			K = len(temp) - 1
		}
		for _, pair := range temp[:K] {
			//物品j
			j := pair.Key
			//物品j与i的相似度
			wj := pair.Value
			//用户浏览过物品j,不推荐
			//todo 这里不用ru判断，ru是昨天为止的用户浏览历史记录，应以当前的浏览记录为准
			if _, ok := ru[j]; ok {
				continue
			}
			//计算推荐度
			pi := 1.0
			rank[j] += pi * wj
		}
	}
	recommendList := make(model.PairList, 0)
	for k, v := range rank {
		recommendList = append(recommendList, model.Pair{k, v})
	}
	//todo recommendList在redis中缓存半小时，半小时内用户加载更多不重新计算，如果是用户刷推荐或者半小时后，才需要删除recommendList,重新计算
	sort.Sort(sort.Reverse(recommendList))
	return analyzeRecommand(recommendList)
}

/*
*创建电影列表数据
*/
func CreateMoviesData(movies [][]string) (map[string]model.Movie) {
	for _, item := range movies {
		movie := model.Movie{}
		movieid := ""
		for i, value := range item {
			//movieId,title,genres
			switch i {
			case 0:
				{
					movieid = value
					movie.MovieId = value
				}
			case 1:
				{
					movie.Title = value
				}
			case 2:
				{
					movie.Genres = value
				}
			}
		}
		// 用户浏览过的物品的集合
		moviesData[movieid] = movie
	}
	return moviesData
}

/*
*解析推荐结果
*/
func analyzeRecommand(recommandList model.PairList) ([]byte) {
	count := 20
	res := make([]model.Movie, 0)
	if count >= len(recommandList)-1 {
		count = len(recommandList) - 1
	}
	for _, pair := range recommandList[:count] {
		movieId := pair.Key
		if _, ok := moviesData[movieId]; ok {
			res = append(res, moviesData[movieId])
		}
	}
	response, _ := json.Marshal(res)
	return response
	//return string(response)
}
