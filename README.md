# SimpleWebAppPython

A simple Flask web application for testing docker-compose to Kubernetes deployment.

## Features

- ✅ Simple Flask web server
- ✅ Health check endpoint
- ✅ API endpoint with system info
- ✅ Beautiful UI showing deployment status
- ✅ Ready for docker-compose deployment
- ✅ Kubernetes-ready with health checks

## Quick Start (Local Testing)

### Using Docker Compose

```bash
docker-compose up
```

Visit: http://localhost:8080

### Using Python Directly

```bash
pip install -r requirements.txt
python app.py
```

Visit: http://localhost:8080

## Deploy to Kubernetes via K3s AI Manager

### Step 1: Access Your Ubuntu Deployment

1. Open K3s AI Manager
2. Navigate to **Deployments**
3. Click **Configure** on your Ubuntu deployment
4. Access the terminal

### Step 2: Clone This Repository

```bash
cd ~
git clone https://github.com/mozeal/SimpleWebAppPython.git
cd SimpleWebAppPython
```

### Step 3: Deploy via docker-compose

1. In the Ubuntu Configure modal, click **"Deploy docker-compose"**
2. Fill in the form:
   - **Compose File Path**: `/home/ubuntu/SimpleWebAppPython/docker-compose.yml`
   - **Deployment Name**: `simple-webapp` (or your choice)
   - **Custom Subdomain** (optional): `my-app`
3. Click **Preview** to see what will be deployed
4. Click **Deploy** and watch the build progress
5. Once complete, click the generated URL to see your app!

### Step 4: Access Your Deployed App

Your app will be available at:
```
https://web-simple-webapp.artech.cloud
```

Or with custom subdomain:
```
https://web-my-app.artech.cloud
```

## Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home page with deployment info |
| `/health` | GET | Health check endpoint (JSON) |
| `/api/info` | GET | System information (JSON) |

## File Structure

```
SimpleWebAppPython/
├── app.py                  # Flask application
├── templates/
│   └── index.html         # Home page template
├── requirements.txt        # Python dependencies
├── Dockerfile             # Container image definition
├── docker-compose.yml     # Deployment configuration
└── README.md              # This file
```

## What Gets Deployed?

When you deploy this app using docker-compose:

- **2 replicas** of the web service (load balanced)
- **512MB RAM** limit per pod
- **0.5 CPU** limit per pod
- **Automatic health checks** every 30 seconds
- **HTTPS URL** with automatic routing via Traefik
- **Zero-downtime** rolling updates

## Customization

### Change Port

Edit `docker-compose.yml`:
```yaml
ports:
  - "3000:3000"  # External:Internal
environment:
  PORT: 3000
```

### Change Replicas

Edit `docker-compose.yml`:
```yaml
deploy:
  replicas: 3  # Increase for higher availability
```

### Add Environment Variables

Edit `docker-compose.yml`:
```yaml
environment:
  FLASK_ENV: production
  MY_CUSTOM_VAR: value
```

## Troubleshooting

### Build Fails

**Problem**: Image build fails with "file not found"
**Solution**: Ensure all files exist in the repository:
```bash
ls -la ~/SimpleWebAppPython/
# Should show: app.py, Dockerfile, docker-compose.yml, requirements.txt, templates/
```

### App Won't Start

**Problem**: Pods crash or won't start
**Solution**: Check logs in K3s AI Manager:
1. Click deployment status
2. View logs
3. Look for errors in application startup

### Can't Access URL

**Problem**: URL returns 404 or connection error
**Solution**:
1. Wait 30 seconds after deployment completes (DNS propagation)
2. Check pod status - should show "2/2 Running"
3. Verify HTTPS (not HTTP) in URL

## Architecture

This app demonstrates a production-ready deployment pattern:

```
┌─────────────────────────────────────────┐
│  User Browser                           │
└──────────────┬──────────────────────────┘
               │ HTTPS
               ▼
┌─────────────────────────────────────────┐
│  Traefik Ingress Controller             │
│  (Automatic HTTPS, Load Balancing)      │
└──────────────┬──────────────────────────┘
               │
        ┌──────┴──────┐
        │             │
        ▼             ▼
┌──────────┐    ┌──────────┐
│  Pod 1   │    │  Pod 2   │
│  Flask   │    │  Flask   │
│  App     │    │  App     │
└──────────┘    └──────────┘
```

## License

MIT License - Feel free to use this for learning and testing!

## Support

For issues with the app, open an issue on [GitHub](https://github.com/mozeal/SimpleWebAppPython/issues).

For issues with K3s AI Manager deployment, check the main documentation.

---

**Happy Deploying!** 🚀
