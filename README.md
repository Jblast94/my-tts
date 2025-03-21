# TTS Knowledge API

This is a Text-to-Speech Knowledge API service that utilizes PostgreSQL for data storage and Redis for caching.

## Prerequisites

- Docker and Docker Compose
- Node.js (recommended version 14+)

> **Note**: PostgreSQL and Redis do not need to be installed locally as they run in Docker containers.

## Repository Setup

1. Create a GitHub Repository:
   - Go to [GitHub](https://github.com)
   - Click "New repository"
   - Name your repository "my-tts"
   - Choose public or private
   - Do not initialize with README, .gitignore, or license

2. Initialize Local Repository:
```bash
git init
git add .
git commit -m "Initial commit"
```

3. Connect to GitHub:
```bash
git remote add origin https://github.com/YOUR_USERNAME/my-tts.git
git branch -M main
git push -u origin main
```

4. Verify Remote:
```bash
git remote -v
```

## Node.js Installation Guide

### Cleaning Up Existing Node.js Installation
If you're experiencing issues with existing Node.js installations:

1. Windows:
   - Uninstall Node.js from Control Panel
   - Delete these folders if they exist:
     ```
     C:\Program Files\nodejs
     C:\Program Files (x86)\nodejs
     %AppData%\npm
     %AppData%\npm-cache
     ```
   - Remove Node.js paths from System Environment Variables

2. Install Node Version Manager (recommended):
   - Windows: Install [nvm-windows](https://github.com/coreybutler/nvm-windows)
     ```bash
     nvm install 14.21.3
     nvm use 14.21.3
     ```
   - Linux/Mac: Install [nvm](https://github.com/nvm-sh/nvm)
     ```bash
     curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
     nvm install 14.21.3
     nvm use 14.21.3
     ```

3. Verify Installation:
   ```bash
   node --version
   npm --version
   ```

4. Troubleshooting:
   - Clear NPM cache: `npm cache clean --force`
   - Reset NPM: `npm reset`
   - If you get permission errors, avoid using sudo and use nvm instead

## Project Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd my-tts
```

2. Environment Configuration
Copy the `.env.example` file to `.env` and update the values:
```bash
DATABASE_URL=postgresql://postgres:postgres@db:5432/tts_knowledge
REDIS_URL=redis://redis:6379
API_KEY=your-secret-key-here
```

3. Start the Services
```bash
docker-compose up -d
```

## Database Setup

The PostgreSQL database will be automatically created when running the Docker container. The default credentials are:
- Host: localhost
- Port: 5432
- Database: tts_knowledge
- Username: postgres
- Password: postgres

## Redis Configuration

Redis is used for caching and will be available at:
- Host: localhost
- Port: 6379

## API Security

The API is protected using an API key authentication. Make sure to:
1. Change the default API key in the `.env` file
2. Include the API key in your requests using the header: `X-API-Key`

## Development

To start the development server:
```bash
npm install
npm run dev
```

## Production

To build and start for production:
```bash
npm run build
npm start
```

## License

[Add your license information here]
