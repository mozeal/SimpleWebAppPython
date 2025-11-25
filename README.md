# SimpleWebAppPython - Notes App

A full-featured Flask notes application for testing docker-compose to Kubernetes deployment via K3s AI Manager.

## Features

- ✅ Full CRUD operations (Create, Read, Update, Delete)
- ✅ SQLite database with persistent storage
- ✅ RESTful API endpoints
- ✅ Beautiful, responsive UI
- ✅ Health check endpoint
- ✅ Ready for docker-compose deployment
- ✅ Kubernetes-ready with persistent volumes
- ✅ Load balanced with 2 replicas

## Quick Start (Local Testing)

### Using Docker Compose

```bash
docker-compose up --build
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
   - **Deployment Name**: `notes-app` (or your choice)
   - **Custom Subdomain** (optional): `my-notes`
3. Click **Preview** to see what will be deployed
4. Click **Deploy** and watch the build progress
5. Once complete, click the generated URL to see your app!

### Step 4: Access Your Deployed App

Your app will be available at:
```
https://web-notes-app.artech.cloud
```

Or with custom subdomain:
```
https://web-my-notes.artech.cloud
```

## Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home page with notes interface |
| `/health` | GET | Health check endpoint (JSON) |
| `/api/info` | GET | System information (JSON) |
| `/api/notes` | GET | Get all notes (JSON) |
| `/api/notes` | POST | Create new note (JSON) |
| `/api/notes/<id>` | GET | Get specific note (JSON) |
| `/api/notes/<id>` | PUT | Update note (JSON) |
| `/api/notes/<id>` | DELETE | Delete note |

## API Examples

### Create a Note

```bash
curl -X POST https://web-notes-app.artech.cloud/api/notes \
  -H "Content-Type: application/json" \
  -d '{"title":"My First Note","content":"Hello from the API!"}'
```

### Get All Notes

```bash
curl https://web-notes-app.artech.cloud/api/notes
```

### Update a Note

```bash
curl -X PUT https://web-notes-app.artech.cloud/api/notes/1 \
  -H "Content-Type: application/json" \
  -d '{"title":"Updated Title","content":"Updated content"}'
```

### Delete a Note

```bash
curl -X DELETE https://web-notes-app.artech.cloud/api/notes/1
```

## File Structure

```
SimpleWebAppPython/
├── app.py                  # Flask application with SQLite
├── templates/
│   └── index.html         # Interactive notes UI
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
- **Persistent volume** for SQLite database
- **Automatic health checks** every 30 seconds
- **HTTPS URL** with automatic routing via Traefik
- **Zero-downtime** rolling updates

## Database Persistence

Notes are stored in a SQLite database located at `/data/notes.db` inside the container. This directory is mounted as a Kubernetes PersistentVolume, ensuring your notes persist across:
- Pod restarts
- Deployments updates
- Container crashes

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: SQLite
- **Frontend**: Vanilla JavaScript with modern CSS
- **Container**: Python 3.11 slim
- **Orchestration**: Kubernetes (via K3s)
- **Ingress**: Traefik

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

### Adjust Resource Limits

Edit `docker-compose.yml`:
```yaml
deploy:
  resources:
    limits:
      cpus: '1.0'
      memory: 1024M
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

### Database Not Persisting

**Problem**: Notes disappear after restart
**Solution**: Ensure persistent volume is correctly mounted:
```bash
kubectl get pvc -n <namespace>
# Should show a PVC bound to the volume
```

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
│  SQLite  │    │  SQLite  │
└────┬─────┘    └────┬─────┘
     │               │
     └───────┬───────┘
             ▼
┌─────────────────────────────────────────┐
│  Persistent Volume (notes-data)         │
│  SQLite Database                        │
└─────────────────────────────────────────┘
```

## Development

Run locally with auto-reload:

```bash
export FLASK_ENV=development
python app.py
```

Run tests:

```bash
# Install test dependencies
pip install pytest requests

# Run tests (example)
pytest tests/
```

## License

MIT License - Feel free to use this for learning and testing!

## Support

For issues with the app, open an issue on [GitHub](https://github.com/mozeal/SimpleWebAppPython/issues).

For issues with K3s AI Manager deployment, check the main documentation.

---

**Happy Deploying!** 🚀
