'use client';

import { useState } from 'react';
import { ApiClient, ApiError } from '@/utils/api';

export default function ApiDemo() {
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const testApiCall = async () => {
    setLoading(true);
    setError(null);
    setResponse(null);

    try {
      // Example: Try to fetch from your Django backend
      // Replace '/users/' with an actual endpoint from your Django app
      const data = await ApiClient.get('/admin/');
      setResponse(data);
    } catch (err) {
      const apiError = err as ApiError;
      setError(apiError.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
      <h2 className="text-2xl font-semibold mb-4">🧪 API Test</h2>
      
      <p className="text-gray-600 dark:text-gray-400 mb-4">
        Test the connection to your Django backend. Make sure Django is running on port 8000.
      </p>

      <button
        onClick={testApiCall}
        disabled={loading}
        className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-semibold py-2 px-6 rounded-lg transition-colors"
      >
        {loading ? 'Testing...' : 'Test API Connection'}
      </button>

      {error && (
        <div className="mt-4 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
          <h3 className="font-semibold text-red-800 dark:text-red-300 mb-2">Error:</h3>
          <p className="text-red-700 dark:text-red-400">{error}</p>
          <p className="text-sm text-red-600 dark:text-red-500 mt-2">
            Make sure your Django backend is running on <code>http://localhost:8000</code>
          </p>
        </div>
      )}

      {response && (
        <div className="mt-4 p-4 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg">
          <h3 className="font-semibold text-green-800 dark:text-green-300 mb-2">Success! ✓</h3>
          <p className="text-green-700 dark:text-green-400 mb-2">
            Connection to Django backend is working!
          </p>
          <details className="mt-2">
            <summary className="cursor-pointer text-sm text-green-600 dark:text-green-500 hover:underline">
              View Response
            </summary>
            <pre className="mt-2 p-2 bg-gray-100 dark:bg-gray-700 rounded text-xs overflow-auto">
              {JSON.stringify(response, null, 2)}
            </pre>
          </details>
        </div>
      )}

      <div className="mt-6 pt-6 border-t border-gray-200 dark:border-gray-700">
        <h3 className="font-semibold mb-2">Example API Usage:</h3>
        <div className="space-y-2 text-sm">
          <div>
            <p className="text-gray-600 dark:text-gray-400 mb-1">Create a new Django API endpoint:</p>
            <code className="block bg-gray-100 dark:bg-gray-700 p-2 rounded">
              {`# In your Django views.py\nfrom django.http import JsonResponse\n\ndef api_example(request):\n    return JsonResponse({'message': 'Hello from Django!'})`}
            </code>
          </div>
          <div>
            <p className="text-gray-600 dark:text-gray-400 mb-1">Call it from Next.js:</p>
            <code className="block bg-gray-100 dark:bg-gray-700 p-2 rounded">
              {`const data = await ApiClient.get('/example/');\nconsole.log(data.message); // "Hello from Django!"`}
            </code>
          </div>
        </div>
      </div>
    </div>
  );
}
