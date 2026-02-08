# TODO App with AI Chatbot - Cloud-Native Deployment

**Status:** ✅ Ready for Cloud Deployment
**Branch:** 003-cloud-native-todo-deploy
**Date:** 2026-02-08

---

## Overview

A production-ready, cloud-native TODO application with AI-powered chatbot capabilities. Fully containerized and ready for deployment to Railway (backend) and Vercel (frontend).

## Quick Links

- **Documentation**: [docs/DEPLOYMENT.md](./docs/DEPLOYMENT.md)
- **Architecture**: [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md)
- **Troubleshooting**: [docs/TROUBLESHOOTING.md](./docs/TROUBLESHOOTING.md)
- **Operations**: [docs/RUNBOOK.md](./docs/RUNBOOK.md)
- **Checklist**: [docs/DEPLOYMENT_CHECKLIST.md](./docs/DEPLOYMENT_CHECKLIST.md)

## Technology Stack

### Frontend
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Deployment**: Vercel

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.11+
- **ORM**: SQLModel
- **Deployment**: Railway (Docker)

### Database
- **Database**: PostgreSQL (Neon Serverless)

### AI/LLM
- **Providers**: OpenAI, Groq, Gemini
- **Architecture**: Multi-agent system

## Local Development

### Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for frontend development)
- Python 3.11+ (for backend development)

### Quick Start with Docker

```bash
# 1. Clone repository
git clone <your-repo-url>
cd "phase 4"

# 2. Set up environment variables
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
# Edit .env files with your values

# 3. Start services with Docker
docker-compose up --build

# 4. Access application
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Development without Docker

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn src.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## Cloud Deployment

### Prerequisites

1. **Accounts**:
   - Railway account (https://railway.app)
   - Vercel account (https://vercel.com)
   - Neon PostgreSQL database
   - LLM API key (Groq/OpenAI/Gemini)

2. **Repository**:
   - GitHub repository with push access
   - All code committed and pushed

### Deployment Steps

#### 1. Deploy Backend to Railway

```bash
# See detailed guide: docs/DEPLOYMENT.md

1. Create Railway project
2. Connect GitHub repository
3. Set root directory to "backend"
4. Configure environment variables:
   - DATABASE_URL
   - BETTER_AUTH_SECRET
   - LLM_PROVIDER
   - GROQ_API_KEY (or other LLM key)
   - FRONTEND_URL (update after frontend deploy)
5. Deploy and get Railway URL
```

#### 2. Deploy Frontend to Vercel

```bash
# See detailed guide: docs/DEPLOYMENT.md

1. Import GitHub repository to Vercel
2. Set root directory to "frontend"
3. Configure environment variables:
   - BACKEND_URL (Railway URL from step 1)
   - BETTER_AUTH_SECRET (must match backend)
   - BETTER_AUTH_URL (Vercel URL)
   - DATABASE_URL
4. Deploy and get Vercel URL
```

#### 3. Update CORS Configuration

```bash
1. Update Railway FRONTEND_URL with Vercel URL
2. Redeploy Railway backend
3. Verify CORS working
```

#### 4. Set Up CI/CD

```bash
1. Add RAILWAY_TOKEN to GitHub secrets
2. Push to main branch
3. GitHub Actions will auto-deploy backend
4. Vercel will auto-deploy frontend
```

**Full deployment guide**: [docs/DEPLOYMENT.md](./docs/DEPLOYMENT.md)

## Project Structure

```
phase 4/
├── backend/                    # FastAPI Backend
│   ├── src/                   # Core application
│   ├── chatbot/               # AI chatbot system
│   ├── Dockerfile             # Backend container
│   ├── railway.json           # Railway config
│   ├── render.yaml            # Render config (alternative)
│   └── .env.example           # Environment template
│
├── frontend/                   # Next.js Frontend
│   ├── app/                   # Next.js app directory
│   ├── components/            # React components
│   ├── lib/                   # Utilities
│   ├── Dockerfile             # Frontend container
│   ├── vercel.json            # Vercel config
│   └── .env.example           # Environment template
│
├── .github/
│   └── workflows/             # CI/CD pipelines
│       ├── backend-test.yml   # Backend tests
│       └── backend-deploy.yml # Backend deployment
│
├── docs/                       # Documentation
│   ├── DEPLOYMENT.md          # Deployment guide
│   ├── ARCHITECTURE.md        # Architecture docs
│   ├── TROUBLESHOOTING.md     # Common issues
│   ├── RUNBOOK.md             # Operations guide
│   └── DEPLOYMENT_CHECKLIST.md # Deployment checklist
│
├── docker-compose.yml          # Local development
└── docker-compose.prod.yml     # Production simulation
```

## Features

### Core Features
- ✅ User authentication (Better Auth)
- ✅ Task CRUD operations
- ✅ Task completion tracking
- ✅ Tag management
- ✅ Reminder scheduling
- ✅ Task analytics

### AI Chatbot Features
- ✅ Natural language task management
- ✅ Multi-agent system (4 specialized agents)
- ✅ Multi-provider support (OpenAI, Groq, Gemini)
- ✅ 15 specialized tools
- ✅ Conversation history
- ✅ Real-time responses

### Deployment Features
- ✅ Docker containerization
- ✅ Multi-stage builds (optimized images)
- ✅ Health checks
- ✅ CI/CD pipelines
- ✅ Environment-based configuration
- ✅ CORS configuration
- ✅ Production-ready logging

## Environment Variables

### Backend (.env)

```env
# Database
DATABASE_URL=postgresql+asyncpg://user:pass@host/db?sslmode=require

# Authentication
BETTER_AUTH_SECRET=your_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# LLM Provider
LLM_PROVIDER=groq
GROQ_API_KEY=your_api_key

# CORS
FRONTEND_URL=https://your-app.vercel.app

# Server (Railway provides this)
PORT=8000
```

### Frontend (.env)

```env
# Backend API
BACKEND_URL=https://your-backend.railway.app

# Authentication
BETTER_AUTH_SECRET=your_secret_key
BETTER_AUTH_URL=https://your-app.vercel.app

# Database
DATABASE_URL=postgresql://user:pass@host/db?sslmode=require
```

**Important**: `BETTER_AUTH_SECRET` must match between backend and frontend!

## API Endpoints

### Authentication
- `POST /api/signup` - Register user
- `POST /api/signin` - Sign in user

### Tasks
- `GET /api/{user_id}/tasks` - List tasks
- `POST /api/{user_id}/tasks` - Create task
- `GET /api/{user_id}/tasks/{id}` - Get task
- `PUT /api/{user_id}/tasks/{id}` - Update task
- `DELETE /api/{user_id}/tasks/{id}` - Delete task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Complete task

### Chat
- `POST /api/{user_id}/chat` - Send chat message
- `GET /api/{user_id}/chat/history` - Get conversation history

### System
- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /docs` - API documentation

## Testing

### Local Testing with Docker

```bash
# Build and start containers
docker-compose up --build

# Test backend health
curl http://localhost:8000/health

# Test frontend
curl -I http://localhost:3000

# Test API documentation
open http://localhost:8000/docs

# Stop containers
docker-compose down
```

### Production Testing

```bash
# Test backend health
curl https://your-backend.railway.app/health

# Test frontend
curl -I https://your-app.vercel.app

# Test API documentation
open https://your-backend.railway.app/docs
```

## Monitoring

### Railway (Backend)
- Dashboard: https://railway.app/dashboard
- Metrics: CPU, Memory, Network
- Logs: Structured JSON logs

### Vercel (Frontend)
- Dashboard: https://vercel.com/dashboard
- Analytics: Web Vitals, Performance
- Logs: Build and runtime logs

### Neon (Database)
- Console: https://console.neon.tech
- Monitoring: Connections, Queries, Storage

## Cost Estimation

- **Railway**: $5-10/month (free tier: $5 credit)
- **Vercel**: Free (Hobby tier)
- **Neon**: Free (existing database)
- **LLM API**: Variable (pay-per-use)
- **Total**: $5-10/month + LLM usage

## Security

- ✅ HTTPS enforced everywhere
- ✅ JWT authentication
- ✅ Password hashing
- ✅ CORS configured
- ✅ Rate limiting enabled
- ✅ Input validation
- ✅ SQL injection prevention
- ✅ XSS protection

## Troubleshooting

Common issues and solutions: [docs/TROUBLESHOOTING.md](./docs/TROUBLESHOOTING.md)

**Quick fixes:**

- **Backend won't start**: Check DATABASE_URL and LLM API key
- **Frontend won't connect**: Verify BACKEND_URL and CORS configuration
- **Authentication fails**: Ensure BETTER_AUTH_SECRET matches
- **Docker build fails**: Run `docker system prune -a` and rebuild

## Support

- **Documentation**: See [docs/](./docs/) directory
- **Issues**: Check [TROUBLESHOOTING.md](./docs/TROUBLESHOOTING.md)
- **Operations**: See [RUNBOOK.md](./docs/RUNBOOK.md)

## License

[Your License Here]

## Contributors

- Development: [Your Name]
- Documentation: Claude Code
- Deployment: [Your Name]

---

**Ready to deploy?** Follow the [Deployment Guide](./docs/DEPLOYMENT.md) to get started!
