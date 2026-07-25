# k8s-self-service-platform

API Python para uma plataforma self-service de deploy em Kubernetes.

## Rodar localmente

```sh
python3 -m app
```

Por padrao, a API sobe em `0.0.0.0:8080`.

Tambem e possivel configurar host e porta:

```sh
HOST=127.0.0.1 PORT=8080 python3 -m app
```

## Endpoints

- `GET /environment`: retorna o ambiente atual.
- `POST /namespace`: valida e retorna o namespace solicitado.

Exemplo:

```sh
curl -X POST http://localhost:8080/namespace \
  -H "Content-Type: application/json" \
  -d '{"name":"platform-dev"}'
```

## Testes

```sh
python3 -m unittest discover -s tests
```

## Docker

```sh
docker build -f deploy/docker/Dockerfile -t k8s-self-service-platform:latest .
docker run --rm -p 8080:8080 k8s-self-service-platform:latest
```

