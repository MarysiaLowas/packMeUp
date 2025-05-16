# GitHub Actions CI/CD Workflows

This directory contains GitHub Actions workflows for CI/CD pipelines.

## CI/CD Pipeline

The main CI/CD pipeline is defined in `workflows/ci-cd.yml` and consists of the following jobs:

### Frontend

1. **frontend-lint**: Lints the frontend code using ESLint
2. **frontend-tests**: Runs unit tests with Vitest and E2E tests with Playwright
3. **frontend-build**: Builds the production-ready frontend application

### Backend

1. **backend-lint**: Lints the backend code using Ruff and performs type checking with mypy
2. **backend-tests**: Runs backend tests using pytest

### Deployment

The `deploy` job will run when:
- A push is made to the `master` branch
- The workflow is manually triggered using the workflow_dispatch event

## Composite Actions

The pipeline uses composite actions to simplify the workflow:

- **setup-frontend**: Sets up Node.js and installs frontend dependencies
- **setup-backend**: Sets up Python, uv, and installs backend dependencies

## Trigger Methods

The workflow can be triggered in two ways:
1. **Automatically**: When changes are pushed to the `master` branch
2. **Manually**: Through the GitHub Actions UI with the ability to specify the deployment environment