/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  // Optimize for production deployment
  poweredByHeader: false,
  compress: true,
};

export default nextConfig;
