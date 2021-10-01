package main

import (
	"fmt"
	"flag"
	"log"
	"net/http"
)

func main() {
	root := flag.String("r", ".", "web root directory")
	port := flag.Int("p", 8080, "server listen port")
	flag.Parse()
	fs := http.FileServer(http.Dir(*root))
	http.Handle("/", fs)
	log.Printf("listening on :%d", *port)
	err := http.ListenAndServe(fmt.Sprintf(":%d", *port), nil)
	if err != nil {
		log.Fatal(err)
	}
}
