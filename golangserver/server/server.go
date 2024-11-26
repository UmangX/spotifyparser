package main

import (
	"fmt"
	"net/http"
	"os"
	"os/exec"
	"umangx/server/umangx"

	"github.com/gin-gonic/gin"
)

func CheckError(e error) {
	if e != nil {
		panic(e)
	}
}

func PlaylistGen(p umangx.PLaylist, url string) map[string]interface{} {
	p.Url = url
	p.Generate()
	data := make(map[string]interface{})
	for i := 0; i < len(p.TrackName); i++ {
		data[p.TrackName[i]] = p.TrackTag[i]
	}
	return data
}

// this is too slow uses around 4-5 secs per query
func TrackDownloadUrl(tag string) string {
	url := "https://open.spotify.com/track/" + tag
	out, err := exec.Command("spotdl", "url", url).Output()
	CheckError(err)
	return string(out)
}

func main() {
	//"https://open.spotify.com/playlist/2STXSQxH7rsNpGgJw5pHii"

	p := umangx.PLaylist{}
	TrackDownloadUrl("10Nmj3JCNoMeBQ87uw5j8k")

	r := gin.Default()
	r.Static("/static", "./static")

	//handling the files is the key : name the files in tags of spotify
	//develop a ranking the for the files like a queue
	r.GET("/storage/:tag", func(ctx *gin.Context) {
		filename := ctx.Param("tag ")
		filepath := "./static/" + filename + ".mp3"
		if _, err := os.Stat(filepath); err == nil {
			fmt.Println("file exists")
			ctx.File(filepath)
		} else {
			// make this concurrent move the file next in the queue
			fmt.Println("file doesn't exist")
		}
	})

	r.GET("/playlist/:tag", func(ctx *gin.Context) {
		tag := ctx.Param("tag")
		url := "https://open.spotify.com/playlist/" + tag
		trackList := PlaylistGen(p, url)
		ctx.JSON(http.StatusOK, trackList)
	})

	r.GET("/link/:tag", func(ctx *gin.Context) {
		tag := ctx.Param("tag")
		out := TrackDownloadUrl(tag)
		ctx.JSON(http.StatusOK, gin.H{
			"link": out,
		})
	})
	r.Run(":8000")
}

//what does the interface means and why does it matter for it to work
