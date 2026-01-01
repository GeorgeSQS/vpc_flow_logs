# VPC Flow Log Application - Separated Services

This project simulates an e-commerce application traffic flow to generate VPC Flow Logs. It is split into two distinct services: Frontend and Backend.

**Traffic Flow:**
user -> Load Balancer (or Browser) -> Frontend Service -> Backend API Service

## Structure

- `frontend_app/`: FastAPI app serving unstyled Jinja2 templates (Port 8000 by default).
- `backend_app/`: FastAPI app serving REST API (Port 8001 by default).

## Local Usage

1. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Run Backend** (Terminal 1)

   ```bash
   cd backend_app
   uvicorn app.main:app --host 0.0.0.0 --port 8001
   ```

3. **Run Frontend** (Terminal 2)

   ```bash
   cd frontend_app
   # Point to the Backend URL
   export BACKEND_HOST="http://localhost:8001"
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

4. **Access**
   Open `http://localhost:8000`. Interaction with the UI will generate HTTP calls from the Frontend Container to the Backend Container.

## Deployment on VM (GCP)

For VPC Flow Log generation between two services (or simulating it on one VM):

### 1. Setup

Install requirements on the VM:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Running Services

You can run them as background processes.

**Start Backend (Port 8001):**

```bash
cd backend_app
nohup uvicorn app.main:app --host 0.0.0.0 --port 8001 > backend.log 2>&1 &
```

**Start Frontend (Port 8000):**

```bash
cd frontend_app
export BACKEND_HOST="http://127.0.0.1:8001"
# OR use the Internal IP of another VM if deployed separately
nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 > frontend.log 2>&1 &
```

### 3. Load Balancer Configuration

Configure the Load Balancer to point to the **Frontend** Service.

- **Backend Service**: Instance Group pointing to Port 8000.
- **Health Check**: Path `/health` (Port 8000).

The Frontend will automatically generate internal traffic "backend-wards" (to port 8001) whenever a user accesses it.
