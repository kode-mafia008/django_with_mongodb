'use client';

import { useEffect, useState } from 'react';
import { ApiClient, ApiError } from '@/utils/api';
import Link from 'next/link';

interface User {
  id: number;
  name: string;
  email: string;
  created_at: string;
  updated_at: string;
}

export default function UsersPage() {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let isMounted = true;

    async function fetchUsers() {
      try { 
        const response = await ApiClient.get<{ users: User[]; count: number }>('/users/');
        if (isMounted) {
          console.log(response);
          setUsers(response.users);
        }
      } catch (err) {
        if (isMounted) {
          console.log(err);
          const apiError = err as ApiError;
          setError(apiError.message);
        }
      } finally {
        if (isMounted) {
          setLoading(false);
        }
      }
    }

    fetchUsers();

    return () => {
      isMounted = false;
    };
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600 dark:text-gray-400">Loading users...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800 p-8">
        <div className="max-w-md w-full bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
          <div className="text-center">
            <div className="text-red-500 text-5xl mb-4">⚠️</div>
            <h2 className="text-2xl font-bold mb-2 text-gray-900 dark:text-white">Error</h2>
            <p className="text-red-600 dark:text-red-400 mb-4">{error}</p>
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
              Make sure your Django backend is running on port 8000
            </p>
            <Link
              href="/"
              className="inline-block bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-6 rounded-lg transition-colors"
            >
              Go Back Home
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800 p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <Link
            href="/"
            className="inline-flex items-center text-blue-600 hover:text-blue-700 dark:text-blue-400 mb-4"
          >
            ← Back to Home
          </Link>
          <h1 className="text-4xl font-bold mb-2 bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-purple-600">
            Users Directory
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            {users.length} {users.length === 1 ? 'user' : 'users'} registered
          </p>
        </div>

        {/* Users List */}
        {users.length === 0 ? (
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-12 text-center">
            <div className="text-gray-400 text-6xl mb-4">👥</div>
            <h2 className="text-2xl font-semibold mb-2 text-gray-900 dark:text-white">
              No Users Yet
            </h2>
            <p className="text-gray-600 dark:text-gray-400">
              Create users in Django admin to see them here
            </p>
            <a
              href="http://localhost:8000/admin"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-block mt-4 bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-6 rounded-lg transition-colors"
            >
              Open Django Admin
            </a>
          </div>
        ) : (
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {users.map((user) => (
              <div
                key={user.id}
                className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 hover:shadow-xl transition-shadow"
              >
                <div className="flex items-start justify-between mb-4">
                  <div className="flex-1">
                    <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-1">
                      {user.name}
                    </h3>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      ID: {user.id}
                    </p>
                  </div>
                  <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-500 rounded-full flex items-center justify-center text-white font-bold text-lg">
                    {user.name.charAt(0).toUpperCase()}
                  </div>
                </div>

                <div className="space-y-2">
                  <div className="flex items-center gap-2 text-sm">
                    <span className="text-gray-500 dark:text-gray-400">📧</span>
                    <span className="text-gray-700 dark:text-gray-300 truncate">
                      {user.email}
                    </span>
                  </div>
                  <div className="flex items-center gap-2 text-sm">
                    <span className="text-gray-500 dark:text-gray-400">📅</span>
                    <span className="text-gray-700 dark:text-gray-300">
                      Joined {new Date(user.created_at).toLocaleDateString()}
                    </span>
                  </div>
                </div>

                <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
                  <Link
                    href={`/users/${user.id}`}
                    className="text-blue-600 hover:text-blue-700 dark:text-blue-400 text-sm font-medium"
                  >
                    View Details →
                  </Link>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* API Info */}
        <div className="mt-8 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-6">
          <h3 className="font-semibold text-blue-900 dark:text-blue-300 mb-2">
            ℹ️ API Information
          </h3>
          <p className="text-sm text-blue-800 dark:text-blue-400">
            This page fetches data from <code className="bg-blue-100 dark:bg-blue-900 px-2 py-1 rounded">GET /api/users/</code>
          </p>
          <p className="text-sm text-blue-800 dark:text-blue-400 mt-2">
            Django endpoint: <code className="bg-blue-100 dark:bg-blue-900 px-2 py-1 rounded">http://localhost:8000/api/users/</code>
          </p>
        </div>
      </div>
    </div>
  );
}
