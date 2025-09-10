/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  
  // Environment variables
  env: {
    CUSTOM_KEY: 'mobinet-nextgen-basic',
    API_BASE_URL: process.env.NODE_ENV === 'production' 
      ? 'https://api.mobinet.fpt.vn/v2' 
      : 'https://dev-api.mobinet.fpt.vn/v2',
  },

  // Image optimization
  images: {
    domains: ['api.mobinet.fpt.vn', 'dev-api.mobinet.fpt.vn'],
    formats: ['image/webp', 'image/avif'],
  },

  // Redirects
  async redirects() {
    return [
      {
        source: '/',
        destination: '/dashboard',
        permanent: false,
      },
    ]
  },

  // Headers for security
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'Referrer-Policy',
            value: 'origin-when-cross-origin',
          },
        ],
      },
    ]
  },

  // Webpack configuration
  webpack: (config, { buildId, dev, isServer, defaultLoaders, webpack }) => {
    // Add custom webpack config here
    config.resolve.alias = {
      ...config.resolve.alias,
      '@': require('path').resolve(__dirname, './src'),
    }
    
    return config
  },
}

module.exports = nextConfig

