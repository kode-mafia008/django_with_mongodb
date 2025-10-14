import ApiDemo from './components/ApiDemo';
import Link from 'next/link';

export default function Home() {
  return (
    <div className="min-h-screen p-8 bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800">
      <div className="max-w-4xl mx-auto">
        <header className="text-center mb-12">
          <h1 className="text-4xl font-bold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-purple-600">
            Nitman
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            AI Powered Blogging Platform
          </p>
        </header>

        <div className="space-y-6">
          <ApiDemo />

          <div className="bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg shadow-lg p-8 text-white">
            <h2 className="text-2xl font-semibold mb-3">🚀 Try It Out!</h2>
            <p className="mb-6 text-blue-50">
              See the integration in action with a real users list page
            </p>
            <Link
              href="/users"
              className="inline-block bg-white text-blue-600 hover:bg-blue-50 font-semibold py-3 px-8 rounded-lg transition-colors shadow-lg"
            >
              View Users List →
            </Link>
          </div>
        </div>

        <footer className="text-center text-gray-600 dark:text-gray-400 mt-12">
          <p>Built with Next.js 15 + Django 5.2 + TypeScript + TailwindCSS</p>
        </footer>
      </div>
    </div>
  );
}
