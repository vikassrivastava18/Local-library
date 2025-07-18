FROM node:22

WORKDIR /app

COPY ./frontend/library/package*.json ./
RUN npm install --omit=optional

RUN npm install -g @angular/cli

COPY ./frontend/library /app

EXPOSE 4200

CMD ["ng", "serve", "--host", "0.0.0.0"]
