package main

import (
	"log"
	"math"
	"sort"
)

type Pair struct {
	Key   string
	Value float64
	Reason map[string]float64

}
type PairList []Pair
func (p PairList) Swap(i, j int) { p[i], p[j] = p[j], p[i] }
func (p PairList) Len() int      { return len(p) }
func (p PairList) Less(i, j int) bool {
	if p[i].Value == p[j].Value {
		//value相同比较key值
		return p[i].Key < p[j].Key
	}
	return p[i].Value < p[j].Value
}

type Recommand struct {
	Pair
	Reason map[string]float64
}
type Train map[string][]string
type Matrix map[string]map[string]float64

func main() {
	train := make(Train)
	train["A"] = []string{"a", "b", "d"}
	train["B"] = []string{"b", "c", "e"}
	train["C"] = []string{"c", "d"}
	train["D"] = []string{"b", "c", "d"}
	train["E"] = []string{"a", "d"}

	w := ItemSimilariy(train)
	for k, v := range w {
		log.Println("======")
		log.Println(k)
		log.Println(v)
		/*
		2018/12/26 16:06:22 ======
			2018/12/26 16:06:22 a
		2018/12/26 16:06:22 map[d:0.5768530264741151 b:0.2944888920518062]
		2018/12/26 16:06:22 ======
		2018/12/26 16:06:22 b
		2018/12/26 16:06:22 map[e:0.4164701851078906 a:0.2944888920518062 d:0.4164701851078906 c:0.4808983469629878]
		2018/12/26 16:06:22 ======
		2018/12/26 16:06:22 d
		2018/12/26 16:06:22 map[c:0.47099852381392604 a:0.5768530264741151 b:0.4164701851078906]
		2018/12/26 16:06:22 ======
		2018/12/26 16:06:22 c
		2018/12/26 16:06:22 map[e:0.4164701851078906 d:0.47099852381392604 b:0.4808983469629878]
		2018/12/26 16:06:22 ======
		2018/12/26 16:06:22 e
		2018/12/26 16:06:22 map[c:0.4164701851078906 b:0.4164701851078906]
		*/
	}
	r := Recommendation(train,w,"A",10)
	log.Println(r)
	/*
	2018/12/26 17:48:57 [{c 0.4808983469629878} {e 0.4164701851078906}]
	*/
	r2 := Recommendation2(train,w,"A",10)
	log.Println(r2)
	/*
	2018/12/28 15:45:11 [{c 0.4808983469629878 map[b:0.4808983469629878]} {e 0.4164701851078906 map[b:0.4164701851078906]}]
	*/
}

func ItemSimilariy(train Train) (Matrix) {
	//同时喜欢物品i和物品j的用户数
	C := make(map[string]map[string]float64)
	// 喜欢物品i的用户数
	N := make(map[string]float64)
	for _, items := range train {
		for _, i := range items {
			N[i] += 1
			for _, j := range items {
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
	W := make(Matrix)
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
func Recommendation(train Train, W Matrix, userId string, K int) (PairList) {
	rank := make(map[string]float64)
	//ru 用户浏览过的物品
	ru := train[userId]
CreateRank:
	for _, movieId := range ru {
		// 将与物品i相近的物品排序
		//1、 将字典转切片
		temp := make(PairList, len(W[movieId]))
		for k, v := range W[movieId] {
			temp = append(temp, Pair{Key:k, Value:v})
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
			for _, item := range ru {
				if item == j {
					continue CreateRank
				}
			}
			//计算推荐度
			pi := 1.0
			rank[j] += pi * wj
		}
	}
	recommendList := make(PairList, 0)
	for k, v := range rank {
		recommendList = append(recommendList,Pair{Key:k, Value:v})
	}
	sort.Sort(sort.Reverse(recommendList))
	return recommendList
}
//带解释的推荐算法
func Recommendation2(train Train, W Matrix, userId string, K int) (PairList) {
	rank := make(map[string]Recommand)
	//ru 用户浏览过的物品
	ru := train[userId]
CreateRank:
	for _, movieId := range ru {
		// 将与物品i相近的物品排序
		//1、 将字典转切片
		temp := make(PairList, len(W[movieId]))
		for k, v := range W[movieId] {
			temp = append(temp, Pair{Key:k, Value:v})
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
			for _, item := range ru {
				if item == j {
					continue CreateRank
				}
			}
			//计算推荐度
			pi := 1.0
			if _,ok := rank[j];ok {
				log.Println("有推荐理由")
				//已经有推荐理由
				recommand := rank[j]
				recommand.Value += pi * wj
				rank[j] = recommand
			}else {
				log.Println("没有推荐理由")
				//没有推荐理由
				recommand := Recommand{}
				//推荐理由
				reason := make(map[string]float64)
				reason[movieId] = pi * wj
				recommand.Value += pi * wj
				recommand.Reason = reason
				rank[j] = recommand
			}

		}
	}
	recommendList := make(PairList, 0)
	for k, rec := range rank {
		v := rec.Value
		log.Println(rec.Reason)
		recommendList = append(recommendList,Pair{Key:k, Value:v,Reason:rec.Reason})
	}
	sort.Sort(sort.Reverse(recommendList))
	return recommendList
}