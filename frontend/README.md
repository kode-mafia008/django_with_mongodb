# Next.js + Django Integration Frontend

This Next.js application is integrated with a Django backend, allowing you to make API calls without dealing with CORS issues or full URLs.

## 🚀 Quick Start

### Prerequisites

- Node.js 20.x or higher
- Django backend running on `http://localhost:8000`

### Installation

```bash
# Install dependencies
npm install

# Run the development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to see the application.

## 📚 How It Works

### API Proxy Configuration

The `next.config.ts` file is configured to proxy all `/api/*` requests to the Django backend:

```typescript
async rewrites() {
  return [
    {
      source: '/api/:path*',
      destination: 'http://localhost:8000/api/:path*',
    },
  ];
}
```

This means when you make a request to `/api/users/`, Next.js forwards it to `http://localhost:8000/api/users/`.

### Making API Calls

Use the `ApiClient` utility from `utils/api.ts`:

```typescript
import { ApiClient } from '@/utils/api';

// GET request
const users = await ApiClient.get('/users/');

// POST request
const newUser = await ApiClient.post('/users/', {
  name: 'John Doe',
  email: 'john@example.com'
});

// PUT request
const updatedUser = await ApiClient.put('/users/1/', {
  name: 'Jane Doe'
});

// PATCH request
const patchedUser = await ApiClient.patch('/users/1/', {
  email: 'jane@example.com'
});

// DELETE request
await ApiClient.delete('/users/1/');
```

### Error Handling

The `ApiClient` automatically handles errors and provides detailed information:

```typescript
try {
  const data = await ApiClient.get('/users/');
} catch (error) {
  const apiError = error as ApiError;
  console.error(apiError.message);
  console.error(apiError.status);
  console.error(apiError.details);
}
```

## 🔧 Configuration

### Environment Variables

Create a `.env.local` file (not tracked by git):

```bash
# Optional: Used for server-side API calls if needed
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### CORS Settings

The Django backend is already configured to accept requests from `http://localhost:3000`. No additional CORS configuration is needed in the frontend.

## 📁 Project Structure

```
frontend/
├── app/
│   ├── components/
│   │   └── ApiDemo.tsx      # Example API integration component
│   ├── page.tsx              # Main page
│   └── layout.tsx
├── utils/
│   └── api.ts                # API client utility
├── next.config.ts            # Next.js configuration with API proxy
└── package.json
```

## 🎨 Features

- ✅ **TypeScript** - Full type safety
- ✅ **TailwindCSS** - Modern styling
- ✅ **API Proxy** - No CORS issues
- ✅ **Error Handling** - Comprehensive error management
- ✅ **Session Support** - Automatic cookie/session handling

## 🔗 Integration with Django

### 1. Django Backend Must Be Running

Ensure your Django backend is running:

```bash
cd ..
python manage.py runserver
```

### 2. Create Django API Endpoints

Example Django view:

```python
# views.py
from django.http import JsonResponse

def api_users(request):
    if request.method == 'GET':
        users = [
            {'id': 1, 'name': 'John Doe'},
            {'id': 2, 'name': 'Jane Smith'}
        ]
        return JsonResponse({'users': users})
```

### 3. Call from Next.js

```typescript
// In your component
const users = await ApiClient.get('/users/');
```

## 🛠️ Development

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Run linter
npm run lint
```

## 📦 Building for Production

1. Update `next.config.ts` to use environment variables:

```typescript
async rewrites() {
  return [
    {
      source: '/api/:path*',
      destination: `${process.env.DJANGO_API_URL || 'http://localhost:8000'}/api/:path*`,
    },
  ];
}
```

2. Build the application:

```bash
npm run build
```

## 🤝 Contributing

1. Make changes in the `app/` directory for UI components
2. Update `utils/api.ts` for API utilities
3. Test with the Django backend running

## 📖 Learn More

- [Next.js Documentation](https://nextjs.org/docs)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [TypeScript Documentation](https://www.typescriptlang.org/docs/)

## 🐛 Troubleshooting

### API calls failing

- Ensure Django is running on `http://localhost:8000`
- Check Django CORS settings in `settings.py`
- Verify the API endpoint exists in Django

### CORS errors

- Django backend should have `corsheaders` configured
- Check `CORS_ALLOWED_ORIGINS` in Django settings
- Ensure middleware is properly ordered
