package api

import "net/http"

func NewRouter() http.Handler {
    mux := http.NewServeMux()
    mux.HandleFunc("/environment", GetEnvironment)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     es
                                                                                                                                                                                                                                                                                                                                               age models

type Environment struct {
    Name    string `json:"name"`
    Cluster string `json:"cluster"`
}
