# frontend.Dockerfile

FROM node:22.17.1

WORKDIR /app

# Copy only dependency descriptors first
COPY ./frontend/library/package*.json ./

# Install dependencies
RUN npm install --omit=optional

# Install Angular CLI globally
RUN npm install -g @angular/cli@20.1.1

# Copy application code
COPY ./frontend/library /app

EXPOSE 4200

CMD ["ng", "serve", "--host", "0.0.0.0"]
