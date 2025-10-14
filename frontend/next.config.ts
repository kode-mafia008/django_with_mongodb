import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async rewrites() {
    // Use Docker service name 'nitman' when in container, localhost otherwise
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';
    return [
      {
        source: '/api/:path*/',
        destination: `${apiUrl}/api/:path*/`,
      },
      {
        source: '/api/:path*',
        destination: `${apiUrl}/api/:path*/`,
      },
    ];
  },
};

export default nextConfig;
