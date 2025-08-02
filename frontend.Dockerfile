FROM node:20-alpine

WORKDIR /app

COPY ./frontend/library/package*.json ./
RUN npm install

# Copy application code
COPY ./frontend/library /app

# Expose the Vue dev server port
EXPOSE 8080

# Enable file watching in Docker (important for hot reload)
ENV CHOKIDAR_USEPOLLING=true

# Start the Vue dev server
CMD ["npm", "run", "serve", "--", "--host", "0.0.0.0"]
