package api

import (
    "encoding/json"
    "net/http"

    "github.com/noemialves/k8s-self-service-platform/internal/models"
)

func GetEnvironment(w http.ResponseWriter, r *http.Request) {
    env := models.Environment{Name: "dev", Cluster: "minikube"}
    json.NewEncoder(w).Encode(env)
}
