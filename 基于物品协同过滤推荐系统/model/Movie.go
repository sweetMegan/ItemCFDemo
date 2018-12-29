package model

type Movie struct {
	MovieId string `json:"movieid"`
	//评分
	Rating float64 	`json:"rating"`
	//浏览时间
	TimeStamp string `json:"timestamp"`
	//影片名
	Title string `json:"title"`
	//影片类型
	Genres string `json:"genres"`
}
type Pair struct {
	Key   string
	Value float64
}
type PairList []Pair
func (p PairList) Swap(i, j int)      { p[i], p[j] = p[j], p[i] }
func (p PairList) Len() int           { return len(p) }
func (p PairList) Less(i, j int) bool { return p[i].Value < p[j].Value }
