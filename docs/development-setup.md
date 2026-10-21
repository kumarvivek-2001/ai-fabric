# AI Fabric — Development Setup

## 1. Prerequisites

The development environment uses:

- Ubuntu on WSL2
- Python 3
- Git
- Docker Desktop with Ubuntu WSL integration
- Docker Compose

Verify installed tools before starting development.

```bash
python3 --version
git --version
docker version
docker compose version
```

If a command fails, resolve that prerequisite before continuing.

## 2. Project Directory

The project is located at:

`/home/vivek/ai-fabric`

Open the Ubuntu terminal and run:

```bash
cd ~/ai-fabric
```

## 3. Python Virtual Environment

Create an isolated Python environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

If virtual-environment creation fails because a required package is missing, inspect the error before installing anything.

After activation, the terminal usually displays `(.venv)`.

## 4. Dependency Management

Python dependencies will be recorded in `requirements.txt`.

Install dependencies only after the file has been created:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 5. Environment Variables and Secrets

Provider credentials must be supplied through environment variables or an appropriate local environment file.

- Never commit API keys or tokens.
- Keep local secrets out of version control.
- Provide a safe example configuration without real credentials.

## 6. Docker

Docker is used to package and run the application consistently.

Verify that Docker works from Ubuntu:

```bash
docker version
docker run hello-world
```

The project will receive a Dockerfile and, if needed, a Compose configuration during implementation.

## 7. Testing

Automated tests will be added alongside the application.

The setup instructions will be updated after the commands have been tested against the actual project.

## 8. Deployment

Nebius is the intended deployment target. Deployment instructions will be documented after the application works locally and the required account access, model endpoint, and compute resources are confirmed.

## 9. Current Status

This document describes the planned development workflow. Application dependencies, tests, and deployment configuration may not yet exist.
