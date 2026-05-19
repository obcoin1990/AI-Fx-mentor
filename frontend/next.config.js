/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  images: {
    unoptimized: true,
  },
  i18n: {
    locales: ['en', 'ar', 'zh'],
    defaultLocale: 'en',
  },
};

module.exports = nextConfig;
