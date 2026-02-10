// API client for FastAPI backend communication
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface ApiResponse<T> {
  data?: T;
  error?: string;
}

interface User {
  id: string;
  email: string;
  name: string;
}

interface TokenResponse {
  access_token: string;
  token_type: string;
}

interface AuthResponse {
  token: TokenResponse;
  user: User;
}

interface Task {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  priority?: string;
  dueDate?: string;
  userId: string;
  createdAt: string;
  updatedAt: string;
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
      localStorage.removeItem('user');
    }
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };

    // Merge any additional headers from options
    if (options.headers) {
      const optionsHeaders = options.headers as Record<string, string>;
      Object.assign(headers, optionsHeaders);
    }

    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    try {
      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        ...options,
        headers,
      });

      if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'Request failed' }));
        return { error: error.detail || error.message || 'Request failed' };
      }

      const data = await response.json();
      return { data };
    } catch (error) {
      console.error('API request error:', error);
      return { error: 'Network error. Please check your connection.' };
    }
  }

  // Auth endpoints
  async signup(email: string, password: string, name: string): Promise<ApiResponse<AuthResponse>> {
    return this.request<AuthResponse>('/api/signup', {
      method: 'POST',
      body: JSON.stringify({ email, password, name }),
    });
  }

  async signin(email: string, password: string): Promise<ApiResponse<AuthResponse>> {
    return this.request<AuthResponse>('/api/signin', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
  }

  // Task endpoints
  async getTasks(userId: string): Promise<ApiResponse<Task[]>> {
    return this.request<Task[]>(`/api/${userId}/tasks`, {
      method: 'GET',
    });
  }

  async createTask(
    userId: string,
    task: {
      title: string;
      description?: string;
      priority?: string;
      dueDate?: string;
    }
  ): Promise<ApiResponse<Task>> {
    return this.request<Task>(`/api/${userId}/tasks`, {
      method: 'POST',
      body: JSON.stringify(task),
    });
  }

  async getTask(userId: string, taskId: string): Promise<ApiResponse<Task>> {
    return this.request<Task>(`/api/${userId}/tasks/${taskId}`, {
      method: 'GET',
    });
  }

  async updateTask(
    userId: string,
    taskId: string,
    updates: Partial<Task>
  ): Promise<ApiResponse<Task>> {
    return this.request<Task>(`/api/${userId}/tasks/${taskId}`, {
      method: 'PUT',
      body: JSON.stringify(updates),
    });
  }

  async deleteTask(userId: string, taskId: string): Promise<ApiResponse<{ message: string }>> {
    return this.request<{ message: string }>(`/api/${userId}/tasks/${taskId}`, {
      method: 'DELETE',
    });
  }

  async toggleTaskComplete(userId: string, taskId: string): Promise<ApiResponse<Task>> {
    return this.request<Task>(`/api/${userId}/tasks/${taskId}/complete`, {
      method: 'PATCH',
    });
  }
}

export const apiClient = new ApiClient(API_BASE_URL);
export type { User, Task, AuthResponse };
