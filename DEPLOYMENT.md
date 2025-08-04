# Deployment Guide for Investment Journal App

## Quick Deployment Options

### 1. Streamlit Community Cloud (Recommended - Free)

1. **Prepare Repository:**
   - Create a new GitHub repository
   - Upload all files from this package
   - Ensure `requirements.txt` is in the root directory

2. **Deploy:**
   - Go to https://share.streamlit.io
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Choose `investment_journal_app.py` as the main file
   - Click "Deploy"

3. **Access:**
   - Your app will be available at: `https://[username]-[repository-name].streamlit.app`

### 2. Heroku Deployment

1. **Prerequisites:**
   - Install Heroku CLI
   - Create Heroku account

2. **Deploy:**
   ```bash
   # Login to Heroku
   heroku login

   # Create new app
   heroku create your-investment-journal

   # Set buildpack
   heroku buildpacks:set heroku/python

   # Deploy
   git init
   git add .
   git commit -m "Initial commit"
   git push heroku main
   ```

3. **Configuration:**
   - The `Procfile` and `setup.sh` are already configured
   - App will run on the assigned Heroku URL

### 3. Self-Hosted Deployment

1. **Server Requirements:**
   - Ubuntu/CentOS server with Python 3.8+
   - At least 512MB RAM
   - Port 8501 open (or configure custom port)

2. **Installation:**
   ```bash
   # Update system
   sudo apt update && sudo apt upgrade -y

   # Install Python and pip
   sudo apt install python3 python3-pip -y

   # Upload your files to server
   scp -r investment-journal/ user@your-server:/home/user/

   # Navigate to directory
   cd /home/user/investment-journal/

   # Install requirements
   pip3 install -r requirements.txt

   # Run application
   streamlit run investment_journal_app.py --server.port=8501 --server.address=0.0.0.0
   ```

3. **Production Setup (with PM2):**
   ```bash
   # Install PM2
   npm install -g pm2

   # Create ecosystem file
   echo 'module.exports = {
     apps: [{
       name: "investment-journal",
       script: "streamlit",
       args: "run investment_journal_app.py --server.port=8501 --server.address=0.0.0.0",
       cwd: "/home/user/investment-journal/",
       instances: 1,
       autorestart: true,
       watch: false,
       max_memory_restart: "1G"
     }]
   }' > ecosystem.config.js

   # Start with PM2
   pm2 start ecosystem.config.js
   pm2 save
   pm2 startup
   ```

### 4. Docker Deployment

1. **Create Dockerfile:**
   ```dockerfile
   FROM python:3.9-slim

   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt

   COPY . .

   EXPOSE 8501

   CMD ["streamlit", "run", "investment_journal_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
   ```

2. **Build and Run:**
   ```bash
   docker build -t investment-journal .
   docker run -p 8501:8501 investment-journal
   ```

## Environment Variables (Optional)

For production deployments, you can set these environment variables:

```bash
export STREAMLIT_SERVER_PORT=8501
export STREAMLIT_SERVER_ADDRESS=0.0.0.0
export STREAMLIT_SERVER_HEADLESS=true
export STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
```

## SSL/HTTPS Setup

For production deployments, use a reverse proxy like Nginx:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
```

## Troubleshooting

1. **Port Issues:** Change port in config.toml or command line
2. **Memory Issues:** Reduce data processing or upgrade server
3. **Package Conflicts:** Use virtual environment
4. **Theme Not Loading:** Clear browser cache and restart app

## Performance Tips

1. Use caching with `@st.cache_data` for expensive operations
2. Limit data size for better performance
3. Use session state efficiently
4. Consider database integration for large datasets

## Security Considerations

1. Never commit sensitive data to repositories
2. Use environment variables for configuration
3. Implement authentication if needed
4. Regular backups of user data
5. Keep dependencies updated
