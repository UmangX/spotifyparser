package umangx

import (
	"fmt"
	"net/http"
	"strings"

	"github.com/PuerkitoBio/goquery"
)

type PLaylist struct {
	Url       string
	TrackName []string
	TrackTag  []string
}

func PLaylistEmptyConstructor() PLaylist {
	p := PLaylist{}
	return p
}

func PLaylistConstructor(url string) PLaylist {
	p := PLaylist{}
	p.Url = url
	p.Generate()
	return p
}

func Extracttag(tag string) string {
	start := strings.Index(tag, "track:") + len("track:")
	end := strings.LastIndex(tag, "-")
	newtag := tag[start:end]
	return newtag
}

func CheckError(e error) {
	if e != nil {
		panic(e)
	}
}

func (p PLaylist) PrintTracks() {
	for _, name := range p.TrackName {
		fmt.Println(name)
	}
}

func (p *PLaylist) Generate() {
	res, err := http.Get(p.Url)
	CheckError(err)
	//defer is used for cleanup it executes at the end
	defer res.Body.Close()
	if res.StatusCode != 200 {
		fmt.Println(res.StatusCode)
	}
	doc, err := goquery.NewDocumentFromReader(res.Body)
	CheckError(err)
	doc.Find("p[data-encore-id='listRowTitle']").Each(func(i int, ele *goquery.Selection) {
		p.TrackName = append(p.TrackName, ele.Find("span").Text())
		tag, isValid := ele.Attr("id")
		if isValid {
			p.TrackTag = append(p.TrackTag, Extracttag((tag)))
		}
	})
}
