# Phase 2 Fix Implementation Plan

## Objective
Transform the current full-stack Next.js implementation into a proper Phase 2 architecture with separated Next.js frontend and FastAPI backend.

---

## Current State Assessment

### What Works
- ✅ FastAPI backend deployed at https://fatima7860-phase3-backend.hf.space
- ✅ Frontend UI components (AuthForm, Dashboard, etc.)
- ✅ Database schema in Neon PostgreSQL
- ✅ Authentication flow (though using Better Auth)
- ✅ Basic task management UI

### What Needs Fixing
- ❌ Frontend uses Next.js API routes instead of FastAPI
- ❌ Frontend uses Better Auth instead of JWT tokens
- ❌ Frontend uses Drizzle ORM (should only be in backend)
- ❌ No API client to communicate with FastAPI
- ❌ FastAPI backend is deployed but not connected

---

## Implementation Steps

### Phase 1: Verify FastAPI Backend (1 hour)

#### Step 1.1: Test Backend Endpoints
```bash
# Test health endpoint
curl https://fatima7860-phase3-backend.hf.space/health

# Test signup endpoint
curl -X POST https://fatima7860-phase3-backend.hf.space/api/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!","name":"Test User"}'

# Test signin endpoint
curl -X POST https://fatima7860-phase3-backend.hf.space/api/signin \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!"}'
```

**Expected Results**:
- Health endpoint returns 200 OK
- Signup creates user and returns JWT token
- Signin authenticates and returns JWT token

**If Backend Fails**:
- Check Hugging Face Space logs
- Verify DATABASE_URL is set correctly
- Verify BETTER_AUTH_SECRET is set
- Restart the Space if needed

---

### Phase 2: Create API Client in Frontend (2 hours)

#### Step 2.1: Create API Client File
**File**: `frontend/lib/api-client.ts`

```typescript
// API client for FastAPI backend
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface ApiResponse<T> {
  data?: T;
  error?: string;
}

class ApiClient {
  private baseUrl: string;
  private token: string | null = null;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
    // Load token from localStorage if available
    if (typeof window !== 'undefined') {
      this.token = localStorage.getItem('auth_token');
    }
  }

  setToken(token: string) {
    this.token = token;
    if (typeof window !== 'undefined') {
      localStorage.setItem('auth_token', token);
    }
  }

  clearToken() {
    this.token = null;
    if (typeof window !== 'undefined') {
      localStorage.removeItem('auth_token');
    }
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    try {
      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        ...options,
        headers,
      });

      if (!response.ok) {
        const error = await response.json();
        return { error: error.detail || 'Request failed' };
      }

      const data = await response.json();
      return { data };
    } catch (error) {
      return { error: 'Network error' };
    }
  }

  // Auth endpoints
  async signup(email: string, password: string, name: string) {
    return this.request('/api/signup', {
      method: 'POST',
      body: JSON.stringify({ email, password, name }),
    });
  }

  async signin(email: string, password: string) {
    return this.request('/api/signin', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
  }

  // Task endpoints
  async getTasks(userId: string) {
    return this.request(`/api/${userId}/tasks`, {
      method: 'GET',
    });
  }

  async createTask(userId: string, task: {
    title: string;
    description?: string;
    priority?: string;
    dueDate?: string;
  }) {
    return this.request(`/api/${userId}/tasks`, {
      method: 'POST',
      body: JSON.stringify(task),
    });
  }

  async updateTask(userId: string, taskId: string, updates: any) {
    return this.request(`/api/${userId}/tasks/${taskId}`, {
      method: 'PUT',
      body: JSON.stringify(updates),
    });
  }

  async deleteTask(userId: string, taskId: string) {
    return this.request(`/api/${userId}/tasks/${taskId}`, {
      method: 'DELETE',
    });
  }

  async toggleTaskComplete(userId: string, taskId: string) {
    return this.request(`/api/${userId}/tasks/${taskId}/complete`, {
      method: 'PATCH',
    });
  }
}

export const apiClient = new ApiClient(API_BASE_URL);
```

#### Step 2.2: Add Environment Variable
**File**: `frontend/.env.local`
```env
NEXT_PUBLIC_API_URL=https://fatima7860-phase3-backend.hf.space
```

**File**: `frontend/.env.example`
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

### Phase 3: Update Authentication Components (2 hours)

#### Step 3.1: Update AuthForm Component
**File**: `frontend/components/AuthForm.tsx`

Replace Better Auth calls with API client:

```typescript
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { apiClient } from '@/lib/api-client';

export default function AuthForm({ mode }: { mode: 'signin' | 'signup' }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      let result;
      if (mode === 'signup') {
        result = await apiClient.signup(email, password, name);
      } else {
        result = await apiClient.signin(email, password);
      }

      if (result.error) {
        setError(result.error);
        return;
      }

      if (result.data) {
        // Store token and user info
        apiClient.setToken(result.data.token);
        localStorage.setItem('user', JSON.stringify(result.data.user));

        // Redirect to dashboard
        router.push('/dashboard');
      }
    } catch (err) {
      setError('An unexpected error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {mode === 'signup' && (
        <div>
          <label htmlFor="name" className="block text-sm font-medium">
            Name
          </label>
          <input
            id="name"
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
            className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2"
          />
        </div>
      )}

      <div>
        <label htmlFor="email" className="block text-sm font-medium">
          Email
        </label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2"
        />
      </div>

      <div>
        <label htmlFor="password" className="block text-sm font-medium">
          Password
        </label>
        <input
          id="password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2"
        />
      </div>

      {error && (
        <div className="text-red-600 text-sm">{error}</div>
      )}

      <button
        type="submit"
        disabled={loading}
        className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:opacity-50"
      >
        {loading ? 'Loading...' : mode === 'signup' ? 'Sign Up' : 'Sign In'}
      </button>
    </form>
  );
}
```

#### Step 3.2: Update Dashboard Page
**File**: `frontend/app/dashboard/page.tsx`

```typescript
'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { apiClient } from '@/lib/api-client';

interface User {
  id: string;
  name: string;
  email: string;
}

interface Task {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  priority?: string;
  dueDate?: string;
}

export default function Dashboard() {
  const [user, setUser] = useState<User | null>(null);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    // Check if user is logged in
    const userStr = localStorage.getItem('user');
    if (!userStr) {
      router.push('/sign-in');
      return;
    }

    const userData = JSON.parse(userStr);
    setUser(userData);

    // Load tasks
    loadTasks(userData.id);
  }, [router]);

  const loadTasks = async (userId: string) => {
    setLoading(true);
    const result = await apiClient.getTasks(userId);
    if (result.data) {
      setTasks(result.data);
    }
    setLoading(false);
  };

  const handleLogout = () => {
    apiClient.clearToken();
    localStorage.removeItem('user');
    router.push('/');
  };

  if (!user) {
    return <div>Loading...</div>;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-xl font-bold">Welcome, {user.name}</h1>
          <button
            onClick={handleLogout}
            className="text-red-600 hover:text-red-800"
          >
            Logout
          </button>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 py-8">
        <h2 className="text-2xl font-bold mb-4">Your Tasks</h2>

        {loading ? (
          <div>Loading tasks...</div>
        ) : tasks.length === 0 ? (
          <div>No tasks yet. Create your first task!</div>
        ) : (
          <div className="space-y-2">
            {tasks.map((task) => (
              <div
                key={task.id}
                className="bg-white p-4 rounded-lg shadow"
              >
                <h3 className="font-semibold">{task.title}</h3>
                {task.description && (
                  <p className="text-gray-600 text-sm">{task.description}</p>
                )}
                <div className="mt-2 text-sm text-gray-500">
                  Status: {task.completed ? 'Completed' : 'Pending'}
                </div>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
```

---

### Phase 4: Remove Next.js API Routes (1 hour)

#### Step 4.1: Delete API Route Files
```bash
# Remove Next.js API routes
rm -rf frontend/app/api/auth
rm -rf frontend/app/api/tasks
```

#### Step 4.2: Remove Better Auth Dependencies
**File**: `frontend/package.json`

Remove these dependencies:
- `better-auth`
- `drizzle-orm`
- `@neondatabase/serverless`

```bash
cd frontend
npm uninstall better-auth drizzle-orm @neondatabase/serverless
```

#### Step 4.3: Remove Better Auth Files
```bash
rm frontend/lib/auth.ts
rm frontend/lib/auth-client.ts
rm frontend/lib/db.ts
rm frontend/lib/schema.ts
rm -rf frontend/drizzle
```

---

### Phase 5: Update Environment Variables (30 minutes)

#### Step 5.1: Frontend Environment Variables
**File**: `frontend/.env.local`
```env
# API Backend URL
NEXT_PUBLIC_API_URL=https://fatima7860-phase3-backend.hf.space
```

#### Step 5.2: Vercel Environment Variables
In Vercel dashboard, update:
- Remove: `DATABASE_URL_NEON`, `BETTER_AUTH_SECRET`, `BETTER_AUTH_URL`
- Add: `NEXT_PUBLIC_API_URL=https://fatima7860-phase3-backend.hf.space`

---

### Phase 6: Testing (2 hours)

#### Step 6.1: Local Testing
```bash
# Start frontend
cd frontend
npm run dev

# Test flows:
1. Sign up new user
2. Sign in existing user
3. View dashboard
4. Create task
5. Update task
6. Delete task
7. Toggle task completion
8. Logout
```

#### Step 6.2: API Testing
```bash
# Test each endpoint with curl
# Verify JWT tokens work
# Verify user isolation
# Verify error handling
```

#### Step 6.3: Integration Testing
- Test authentication flow end-to-end
- Test task CRUD operations
- Test authorization (cross-user access prevention)
- Test error scenarios

---

### Phase 7: Deployment (1 hour)

#### Step 7.1: Update Repository
```bash
git add .
git commit -m "Fix Phase 2: Connect frontend to FastAPI backend

- Remove Next.js API routes
- Add API client for FastAPI communication
- Update authentication to use JWT tokens
- Remove Better Auth and Drizzle ORM
- Connect to deployed FastAPI backend"

git push origin 003-cloud-native-todo-deploy
```

#### Step 7.2: Deploy to Vercel
- Push changes to trigger deployment
- Verify environment variables
- Test production deployment

#### Step 7.3: Update Documentation
- Update README with correct architecture
- Update deployment status
- Document API endpoints
- Add troubleshooting guide

---

## Success Criteria

### Functional Requirements
- ✅ User can sign up and receive JWT token
- ✅ User can sign in and receive JWT token
- ✅ User can view their tasks
- ✅ User can create new tasks
- ✅ User can update tasks
- ✅ User can delete tasks
- ✅ User can toggle task completion
- ✅ Users cannot access other users' tasks
- ✅ JWT tokens expire after 24 hours

### Technical Requirements
- ✅ Frontend only contains UI components
- ✅ All business logic is in FastAPI backend
- ✅ Frontend communicates with backend via REST API
- ✅ JWT authentication works end-to-end
- ✅ No Next.js API routes for business logic
- ✅ No database access from frontend

### Performance Requirements
- ✅ API responses < 2 seconds
- ✅ Authentication < 1 second
- ✅ Task operations < 1 second

---

## Rollback Plan

If something goes wrong:

1. **Keep current branch**: Don't delete 003-cloud-native-todo-deploy
2. **Create new branch**: `003-phase2-fix`
3. **Test thoroughly** before merging
4. **Keep old deployment** until new one is verified
5. **Document issues** for future reference

---

## Timeline

| Phase | Duration | Dependencies |
|-------|----------|--------------|
| 1. Verify Backend | 1 hour | None |
| 2. Create API Client | 2 hours | Phase 1 |
| 3. Update Auth | 2 hours | Phase 2 |
| 4. Remove API Routes | 1 hour | Phase 3 |
| 5. Update Env Vars | 30 min | Phase 4 |
| 6. Testing | 2 hours | Phase 5 |
| 7. Deployment | 1 hour | Phase 6 |
| **Total** | **~10 hours** | |

---

## Risk Assessment

### High Risk
- ❗ Backend might not be accessible on Hugging Face
- ❗ Database connection might fail
- ❗ JWT token format might not match

### Medium Risk
- ⚠️ CORS issues between Vercel and Hugging Face
- ⚠️ Environment variables might be misconfigured
- ⚠️ User data migration needed

### Low Risk
- ℹ️ UI components need minor updates
- ℹ️ TypeScript types need adjustment
- ℹ️ Documentation needs updates

---

## Next Steps

1. **Confirm approach** with stakeholder
2. **Create new branch** for Phase 2 fix
3. **Start with Phase 1** (verify backend)
4. **Proceed sequentially** through phases
5. **Test thoroughly** at each step
6. **Deploy when ready**

---

**Status**: Ready to implement
**Estimated Time**: 10 hours
**Risk Level**: Medium
**Recommended**: Yes
