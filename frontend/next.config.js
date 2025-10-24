/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  output: 'standalone', // ✅ Mode standalone pour réduire la taille
  swcMinify: true, // ✅ Minification avec SWC (plus rapide)
  
  // Configuration pour la production
  experimental: {
    optimizePackageImports: ['framer-motion', '@headlessui/react', '@heroicons/react'],
  },
  
  // Optimisation des images
  images: {
    domains: [],
    formats: ['image/webp'],
  },
  
  // Variables d'environnement (ne pas inclure de rewrites en production)
  async rewrites() {
    // Seulement en développement local
    if (process.env.NODE_ENV === 'development') {
      return [
        {
          source: '/api/:path*',
          destination: 'http://localhost:8000/api/:path*',
        },
      ];
    }
    return [];
  },
};

module.exports = nextConfig;

