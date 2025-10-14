/**
 * API utility functions for making requests to the Django backend
 * All API calls use relative paths which are proxied to the Django backend via next.config.ts
 */

export interface ApiError {
  message: string;
  status: number;
  details?: any;
}

export class ApiClient {
  /**
   * Make a GET request to the Django backend
   */
  static async get<T>(endpoint: string): Promise<T> {
    try {
      const response = await fetch(`/api${endpoint}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include', // Important for session/cookie-based auth
      });

      if (!response.ok) {
        throw await this.handleError(response);
      }

      return response.json();
    } catch (error) {
      throw this.handleRequestError(error);
    }
  }

  /**
   * Make a POST request to the Django backend
   */
  static async post<T>(endpoint: string, data: any): Promise<T> {
    try {
      const response = await fetch(`/api${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw await this.handleError(response);
      }

      return response.json();
    } catch (error) {
      throw this.handleRequestError(error);
    }
  }

  /**
   * Make a PUT request to the Django backend
   */
  static async put<T>(endpoint: string, data: any): Promise<T> {
    try {
      const response = await fetch(`/api${endpoint}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw await this.handleError(response);
      }

      return response.json();
    } catch (error) {
      throw this.handleRequestError(error);
    }
  }

  /**
   * Make a PATCH request to the Django backend
   */
  static async patch<T>(endpoint: string, data: any): Promise<T> {
    try {
      const response = await fetch(`/api${endpoint}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw await this.handleError(response);
      }

      return response.json();
    } catch (error) {
      throw this.handleRequestError(error);
    }
  }

  /**
   * Make a DELETE request to the Django backend
   */
  static async delete<T>(endpoint: string): Promise<T> {
    try {
      const response = await fetch(`/api${endpoint}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
      });

      if (!response.ok) {
        throw await this.handleError(response);
      }

      // Some DELETE requests don't return a body
      const text = await response.text();
      return text ? JSON.parse(text) : ({} as T);
    } catch (error) {
      throw this.handleRequestError(error);
    }
  }

  /**
   * Handle API errors
   */
  private static async handleError(response: Response): Promise<ApiError> {
    let details;
    try {
      details = await response.json();
    } catch {
      details = await response.text();
    }

    return {
      message: `API Error: ${response.status} ${response.statusText}`,
      status: response.status,
      details,
    };
  }

  /**
   * Handle request errors (network issues, etc.)
   */
  private static handleRequestError(error: any): ApiError {
    if (error.message && error.status) {
      return error as ApiError;
    }

    return {
      message: error.message || 'An unexpected error occurred',
      status: 0,
      details: error,
    };
  }
}

// Example usage:
// const users = await ApiClient.get<User[]>('/users/');
// const newUser = await ApiClient.post<User>('/users/', { name: 'John' });
