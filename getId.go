package main

import (
	"flag"
	"fmt"
	"log"
	"net/http"
	"net/url"
	"os"
	"strings"

	"github.com/PuerkitoBio/goquery"
)

var (
	httpClient *http.Client
	baseURL    string
	arrID      []string
)

func main() {
	flag.Parse()

	if flag.NArg() < 1 {

		return
	}

	u, err := url.Parse(flag.Arg(0))
	if err != nil {
		panic(err)
	}

	if u.Scheme != "http" && u.Scheme != "https" {
		log.Fatal("Unrecognized URL-scheme: \"" + u.Scheme + "\".\n")
	}
	httpClient = &http.Client{}
	baseURL = u.String()
	CrawlerBlog(u.String())
}

// RequestPage make a http get method and return a goquery.Document
func RequestPage(pageURL string) (doc *goquery.Document) {

	resp, err := httpClient.Get(pageURL)
	if err != nil {
		log.Fatal(err)
	}

	defer resp.Body.Close()
	d, err := goquery.NewDocumentFromReader(resp.Body)
	if err != nil {
		log.Fatal(err)
	}

	return d
}

// CrawlerBlog get all post of all page and export xml file
func CrawlerBlog(strURL string) {
	d := RequestPage(strURL)
	d.Find("#pl-load-more-destination tr").Each(func(i int, s *goquery.Selection) {
		id, _ := s.Attr("data-video-id")
		arrID = append(arrID, id)
		fmt.Println(id)
	})
	saveChannel("channel.txt")

	fmt.Println("Done")
}

// saveXML export one xml file
func saveChannel(fileName string) {
	writeLines(arrID, fileName)
}

func writeLines(lines []string, path string) (err error) {
	var (
		file *os.File
	)

	if file, err = os.Create(path); err != nil {
		return
	}
	defer file.Close()

	for _, item := range lines {
		_, err := file.WriteString(strings.TrimSpace(item) + "\n")
		if err != nil {
			fmt.Println(err)
			break
		}
	}
	return
}

func panicIf(err error) {
	if err != nil {
		panic(err)
	}
}
