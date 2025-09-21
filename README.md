# CobrejaApp - Django Ninja

Projeto criado para estudar e aprofundar conhecimentos no framework Django Ninja, baseado em Django.
Também serve como referência de arquitetura de projeto para consultas futuras.

Além disso, o projeto explora o conceito de multi-tenancy, onde:

- Um token do tenant é enviado via header da requisição (X-TOKEN).
- Esse token é usado para consultar o Redis e recuperar as informações de acesso do tenant, incluindo dados de banco de dados.
- Com isso, é possível conectar dinamicamente ao banco correto para cada tenant.

para rodar a migrate para todos, será necessário rodar o comando `uv run manage.py migrate_tenants`

# Comandos rápidos

- `uv sync` - instala dependencias
- `uv run manage.py makemigrations` - verifica se existe novas models para migrar
- `uv run manage.py migrate` - roda a migration a nivel local
- `uv run manage.py migrate_tenants` - inicia migrate a nivel do mult tenant, irei controlar via redis

- `uv run pytest -v` - roda os testes
- `uv run manage.py runserver` - inicia a app a nivel local
- `docker compose up -d --build --force-recreate --remove-orphans`- subir infra local para coleta de traces e métricas

# Telemetria

## 1️⃣ Como funciona o OpenTelemetry

OpenTelemetry (OTEL) é um padrão para coletar **traces, métricas e logs** de aplicações.  
Fluxo básico:
`Django App → OTEL SDK → OTEL Collector → Grafana/Prometheus/Tempo`

- **Traces:** sequências de operações (spans) de uma requisição.
- **Metrics:** valores numéricos medidos periodicamente (CPU, memória, disco).
- **Logs:** mensagens de log (opcional).

---

## 2️⃣ Arquivo `otel-config.yaml`

Define como o OTEL Collector recebe, processa e exporta dados:

- **Receivers:** de onde o Collector recebe os dados (`otlp` via HTTP/gRPC).
- **Exporters:** para onde os dados vão (`logging`, `prometheus`, `otlphttp` → Tempo).
- **Pipelines:** ligam receivers a exporters (`traces` e `metrics`).

> O Collector atua como um **agente central**, que processa e envia métricas e traces.

---

## 3️⃣ Serviços do Docker Compose

| Serviço            | Função                                                           | Porta                                                 | Acesso                                                             |
| ------------------ | ---------------------------------------------------------------- | ----------------------------------------------------- | ------------------------------------------------------------------ |
| **otel-collector** | Recebe métricas/traces do Django, processa e envia para backends | 4318 (OTLP HTTP), 4317 (OTLP gRPC), 8888 (Prometheus) | Interno, usado pela aplicação                                      |
| **prometheus**     | Coleta e armazena métricas do Collector                          | 9090                                                  | http://localhost:9090 → Explore métricas como `system_cpu_percent` |
| **grafana**        | Dashboard para métricas e traces                                 | 3000                                                  | http://localhost:3000 → Data sources: Prometheus e Tempo           |
| **tempo**          | Armazena traces do OTEL Collector                                | 3200                                                  | Configurado no Grafana para visualizar spans                       |

---

## 4️⃣ Como visualizar

### Métricas

1. Acesse Prometheus: [http://localhost:9090](http://localhost:9090)
2. Query: `system_cpu_percent`, `system_memory_percent`, `system_disk_percent`
3. Dashboards: Grafana → Painéis → Prometheus como data source.

### Traces

1. Acesse Grafana: [http://localhost:3000](http://localhost:3000)
2. Adicione Tempo como data source: `http://tempo:3200`
3. Explore → Traces → veja spans e duração de cada requisição Django.

---

## 5️⃣ Fluxo resumido

```text
[Request Django Ninja]
        │
        ▼
[OpenTelemetry SDK (Traces/Metrics)]
        │
        ▼
[OTEL Collector]
   ├─> Logging (console)
   ├─> Prometheus (metrics)
   └─> Tempo (traces)
        │
        ▼
     [Grafana]
```

- Traces: visualizados no Grafana via Tempo.
- Metrics: visualizadas no Grafana via Prometheus.
