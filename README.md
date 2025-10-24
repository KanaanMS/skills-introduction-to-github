# Cloud AI SaaS Coursework Reference Implementation

This repository tracks the implementation of the 5CCSACCA Cloud Computing for Artificial Intelligence coursework. The goal is to deliver a Software-as-a-Service platform that exposes two AI workloads through FastAPI:

1. **Vision Service** &mdash; powered by Ultralytics YOLO (e.g. `yolo11n`) to analyse uploaded images.
2. **Language Service** &mdash; powered by Microsoft's BitNet large language model to generate text from natural language prompts.

Both services must operate within a 4 CPU / 16&nbsp;GB RAM budget and will ultimately be orchestrated with Docker and Docker Compose.

## Repository Layout

```
.
├── docs/                  # Auxiliary documentation (roadmaps, cost notes, etc.)
├── src/                   # FastAPI application and service wrappers
│   ├── main.py            # FastAPI entrypoint
│   ├── models/            # Pydantic schemas shared across the API
│   └── services/          # Service abstractions for YOLO and BitNet
├── tests/                 # Pytest-based test suite
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation (this file)
```

Additional assets (e.g. diagrams or screenshots) can be added to `docs/` as the project evolves through each coursework stage.

## Getting Started

> 🆕 **First time with these tools?**
>
> Work through the step-by-step [Beginner Checklist](docs/beginner-guide.md) before returning to the sections below. It walks through installing Git/Python/Docker, cloning the repo, creating feature branches, and launching the FastAPI server for the very first time.

### 1. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

> **Note**
> The BitNet model is not distributed through PyPI. When you are ready to integrate the official weights, follow the instructions in the [BitNet repository](https://github.com/microsoft/BitNet) to install the package from source. The current codebase provides a deterministic mock fallback so you can exercise the API before integrating the full model.

### 3. Run the FastAPI application

```bash
uvicorn src.main:app --reload
```

Open <http://127.0.0.1:8000/docs> to explore the automatically generated API documentation and run sample requests.

### 4. Execute the automated tests

```bash
pytest
```

The tests validate that the mock BitNet integration, YOLO service fallback, and FastAPI routes are correctly wired. As you replace the mocks with real models, expand the tests to cover your new behaviours.

## Available API Endpoints

| Method | Path | Description |
| ------ | ---- | ----------- |
| `GET` | `/` | Friendly welcome message and quick docs link. |
| `GET` | `/health` | Reports which backends are active for the vision and language services. |
| `POST` | `/vision/predict` | Accepts an image upload (`multipart/form-data`) and returns YOLO detections. |
| `POST` | `/llm/generate` | Accepts a JSON body with a `prompt` field and returns BitNet-generated text. |

Consult the interactive documentation at `/docs` for sample request/response payloads, parameter validation rules, and schema definitions.

## Development Workflow

The coursework must follow **GitFlow**. Recommended branch naming conventions:

- `feature/stage-01-vision-prototype`
- `feature/stage-02-containerisation`
- `feature/stage-03-fastapi`
- ...and so on through `stage-11`.

Each stage should land through a pull request targeting `develop`, after which the stabilised milestones are merged into `main`.

### Suggested Stage Roadmap

| Stage | Focus | Repository Touchpoints |
| ----- | ----- | ---------------------- |
| 1 | Baseline inference | `src/services/vision.py`, tests validating YOLO predictions |
| 2 | Containerisation | `Dockerfile`, `docker-compose.yml`, update README deployment steps |
| 3 | API exposure | `src/main.py`, FastAPI routers, authentication stubs |
| 4 | Persistence | Database module, migrations, schema documentation |
| 5 | Firebase storage | Firebase client wrapper, new endpoints, security updates |
| 6 | Asynchronous processing | RabbitMQ service, Docker Compose orchestration |
| 7 | Authentication | Firebase auth integration, role-based access |
| 8 | Cost estimation | `docs/costs.md`, README summary, video discussion notes |
| 9 | Monitoring | Observability stack (e.g. Prometheus + Grafana) |
| 10 | Testing strategy | Comprehensive Pytest suite, coverage reports |
| 11 | Security hardening | Threat modelling, environment hardening, secrets management |

Use GitHub Issues or Projects to track the subtasks discovered in each stage. Update the README and documentation after every completed milestone.

## Deployment Targets

Docker assets will be added in Stage 2. The final submission must support:

1. **Build:** `docker compose build`
2. **Run:** `docker compose up`
3. **Test:** `docker compose run --rm api pytest`

If the architecture grows beyond these commands, include helper scripts in a `scripts/` folder and document them here.

## Video Preparation Checklist

The final five-minute video (plus one-minute demo) must address:

1. System overview and design decisions
2. Architecture and technology stack (including Docker Compose topologies)
3. Model configuration and training considerations
4. Development workflow and Git logs
5. CI/CD automation strategy
6. Cost estimation for up to 200,000 concurrent users
7. Testing, security, and monitoring measures
8. Identified limitations
9. Sustainability considerations
10. References in IEEE format

Capture short clips or screenshots during development to streamline video production later.

## Next Steps

- Flesh out the YOLO inference logic with real model weights and sample images.
- Replace the BitNet mock response with the actual Microsoft implementation.
- Add Docker and Docker Compose definitions.
- Introduce persistence, messaging, authentication, and monitoring in line with the coursework stages.
- Expand the automated test coverage as each new component arrives.

Feel free to open GitHub Issues to document assumptions, open questions, or work items as you progress.

