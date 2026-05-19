FROM node:24-alpine

WORKDIR /app/frontend

# Install dependencies
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm ci --legacy-peer-deps || npm install

# Copy source code
COPY frontend/ ./

# Build for production
RUN npm run build || true

# Expose port
EXPOSE 3000

# Start dev server (or production server)
CMD ["npm", "run", "dev"]
