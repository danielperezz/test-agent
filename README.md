# Simple Example Marketplace Agent

A minimal example agent demonstrating the complete MLRun marketplace agent lifecycle.

## What's Included

This example contains everything needed to create, package, and deploy a marketplace agent:

```
example-marketplace-agent/
├── simple_agent/          # Agent code (FastAPI application)
│   ├── __init__.py       # Package initialization
│   └── main.py           # Main application logic
├── item.yaml             # Marketplace metadata
├── requirements.txt      # Python dependencies
├── usage_example.ipynb   # Complete usage guide
└── README.md            # This file
```

## Agent Features

The simple example agent is a FastAPI-based service that demonstrates:

### 1. **Environment Variables**
- `SERVICE_NAME` (required): Service identifier used in logs and responses
- `LOG_LEVEL` (optional, default: INFO): Logging level (DEBUG, INFO, WARNING, ERROR)
- `PORT` (optional, default: 8080): Port the application listens on

### 2. **Secrets**
- `API_KEY` (required): API key for authenticating requests
- `DATABASE_PASSWORD` (optional): Optional database credential

### 3. **Endpoints**
- `GET /` - Service information
- `GET /health` - Health check
- `POST /echo` - Echo service with API key validation

## Quick Start

### 1. Package the Agent

```bash
cd example-marketplace-agent
tar -czf simple-example-agent.tar.gz simple_agent/
```

### 2. Use the Jupyter Notebook

Open `usage_example.ipynb` and follow the step-by-step guide:

1. Package the agent code
2. Load agent metadata from `item.yaml`
3. Upload source archive to MLRun
4. Import the agent
5. Deploy with configuration
6. Test the deployed service
7. Redeploy (fast with caching!)

## Configuration Examples

### Minimal Deployment (Required Only)

```python
agent.deploy(
    project="my-project",
    source_url=source_url,
    API_KEY="my-secret-key",           # Required secret
    SERVICE_NAME="my-service",         # Required env var
)
```

### Full Deployment (All Options)

```python
agent.deploy(
    project="my-project",
    source_url=source_url,
    gateway_config={
        "name": "my-gateway",
        "authentication_mode": "none",
        "path": "/",
    },
    # Required
    API_KEY="my-secret-key",
    SERVICE_NAME="my-service",
    # Optional
    DATABASE_PASSWORD="db-password",
    LOG_LEVEL="DEBUG",
    PORT="8080",
)
```

## Testing the Agent

### Health Check

```bash
curl https://<agent-url>/health
```

### Echo Endpoint

```bash
curl -X POST https://<agent-url>/echo \
  -H "X-API-Key: my-secret-key" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!", "uppercase": false}'
```

## Customization Guide

### Modify Agent Behavior

Edit `simple_agent/main.py` to customize:
- Add new endpoints
- Change processing logic
- Add external API integrations
- Implement custom authentication

### Update Configuration

Edit `item.yaml` to:
- Change default values
- Add new inputs (env vars/secrets)
- Update metadata (name, version, description)
- Modify build/deploy settings

### Add Dependencies

Edit `requirements.txt` to add Python packages:
```
fastapi==0.115.0
uvicorn==0.30.6
your-new-package==1.0.0
```

## Architecture Notes

### Secrets vs Environment Variables

- **Secrets** (`type: secret`): Stored in Kubernetes secrets, available as env vars in pod
  - Use for: API keys, passwords, tokens, credentials
  - Access: `os.getenv("SECRET_NAME")`
  - Storage: Project-level K8s secret (shared across functions)

- **Environment Variables** (`type: env`): Set directly as env vars
  - Use for: Non-sensitive configuration (service names, log levels, ports)
  - Access: `os.getenv("VAR_NAME")`
  - Storage: Function spec

### Image Caching

First deployment:
1. Builds base image with requirements (~5-10 min)
2. Adds source code
3. Deploys application

Subsequent deployments:
1. Reuses cached base image (~1 min)
2. Adds updated source code
3. Deploys application

Force rebuild: Use `force_rebuild=True` to skip cache.

### API Gateway

The agent creates an API gateway for external access:
- Default: No gateway (internal only)
- Enable: Set `create_default_api_gateway=True` or provide `gateway_config`
- Custom: Pass `gateway_config` dict with authentication, path, etc.

## Troubleshooting

### "Missing mandatory configurations"
- Ensure all required inputs are provided during deployment
- Check `item.yaml` for `required: true` inputs without defaults

### "Invalid API key"
- Verify the `X-API-Key` header matches the deployed `API_KEY`
- Check pod logs for authentication attempts

### Build failures
- Verify `requirements.txt` packages are available on PyPI
- Check base image compatibility (`python:3.11-slim`)
- Review build logs in MLRun UI

### Slow deployments
- First deploy is always slow (building base image)
- Subsequent deploys should be fast (caching)
- Use `force_rebuild=False` (default) to enable caching

## References

- [MLRun Documentation](https://docs.mlrun.org/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Marketplace Agent API](../../mlrun/marketplace/agent.py)

## License

Apache License 2.0 (same as MLRun)
