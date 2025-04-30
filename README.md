# Crypto Analyzer — Real-Time Crypto Trading Insights

A full-stack, event-driven crypto analyzer platform.
Built for high performance, real-time insights, and seamless developer experience.
Everything runs in **Docker** — no local installation hell!

---

## 🛠 Technologies Used

- **FastAPI** (async API + WebSocket server)
- **gRPC** (background price ingestion)
- **MongoDB** (user and trades storage)
- **Redis** (real-time caching)
- **MinIO** (object storage, S3 compatible)
- **Prometheus & Grafana** (monitoring and observability)
- **Docker Compose** (container orchestration)

---

## 🚀 Project Goals

- Real-time crypto trading data ingestion and analysis
- Scalable WebSocket-based updates to clients
- Clean authentication with JWT tokens
- Async Python everywhere (no blocking code)
- Developer-friendly local environment
- High-availability architecture patterns

---

## 📦 How to Run (Local Dev Setup)

```bash
# 1. Clone the repository
git clone git@github.com:sindilevich/crypto-analyzer.git
cd crypto-analyzer

# 2. Start services
docker-compose up --build
```

Visit:

- API: http://localhost:8180
- WebSocket: ws://localhost:8180/ws
- MongoDB: port `27017`
- Redis: port `6379`
- MinIO: http://localhost:9000 (minioadmin:minioadmin)
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000

## 🤝 Contributing

This is a hands-on learning project, designed for fun, experimentation, and building cloud-native muscle memory.
Feel free to fork, hack, break, and improve it!

## 📜 License

MIT License (open and free forever).

## 🔗 Useful Links

Setting up the uvicorn logger: https://stackoverflow.com/a/77007723

How to initialize a global object or variable and reuse it in every FastAPI endpoint? https://stackoverflow.com/a/76322910