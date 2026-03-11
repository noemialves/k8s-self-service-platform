package main

import (
    "log"
    "net/http"
    "github.com/noemialves/k8s-self-service-platform/internal/api"
)

func main() {
    router := api.NewRouter()
    log.Println("API server starting on :8080")
    log.Fatal(http.ListenAndServe(":8080", router))
}
