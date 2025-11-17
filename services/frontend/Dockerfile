FROM node:25.2-slim

ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"

WORKDIR /frontend

COPY package.json pnpm-lock.yaml ./

RUN npm install -g pnpm

RUN pnpm install --frozen-lockfile --shamefully-hoist

RUN pnpm approve-builds

COPY . .

CMD ["pnpm", "run", "build"]
