# Create additional files needed for deployment package

# 1. Create requirements.txt
requirements_content = '''streamlit>=1.28.0
pandas>=1.5.0
plotly>=5.15.0
datetime
'''

with open('requirements.txt', 'w') as f:
    f.write(requirements_content)

# 2. Create config.toml for theme configuration
config_content = '''[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[server]
headless = true
port = 8501
'''

with open('config.toml', 'w') as f:
    f.write(config_content)

# 3. Create README.md for deployment instructions
readme_content = '''# Personal Investment Journal - Streamlit App

A comprehensive personal investment tracking application built with Streamlit, featuring Indian Rupee (₹) currency support and dark/light mode toggle.

## Features

- 📊 **Dashboard**: Portfolio overview with key metrics and performance charts
- ➕ **Transaction Entry**: Log investments with detailed rationales
- 📈 **Portfolio Review**: Current holdings and performance analysis
- 🔍 **Investment Analysis**: Compare rationales with outcomes for learning
- 💾 **Data Management**: Import/export CSV data
- 🌙 **Theme Toggle**: Switch between dark and light modes
- 💰 **INR Currency**: All amounts formatted in Indian Rupees

## Installation & Setup

### Local Development
1. Clone or download this repository
2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   streamlit run investment_journal_app.py
   ```

### Deployment Options

#### 1. Streamlit Community Cloud (Free)
1. Push your code to a GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Select your repository and deploy

#### 2. Heroku Deployment
1. Create a `Procfile` with: `web: streamlit run investment_journal_app.py --server.port=$PORT --server.address=0.0.0.0`
2. Create a `setup.sh` file (see deployment files)
3. Deploy to Heroku

#### 3. Self-Hosted
1. Upload files to your web server
2. Install Python and pip
3. Install requirements: `pip install -r requirements.txt`
4. Run: `streamlit run investment_journal_app.py --server.port=8501 --server.address=0.0.0.0`

## File Structure
```
investment-journal/
├── investment_journal_app.py    # Main application
├── requirements.txt             # Python dependencies
├── config.toml                 # Streamlit configuration
├── README.md                   # This file
├── Procfile                    # For Heroku deployment
└── setup.sh                    # Setup script for deployment
```

## Usage

1. **Add Transactions**: Record your buy/sell decisions with rationales
2. **Monitor Portfolio**: Track current value and performance
3. **Analyze Decisions**: Compare your initial rationale with actual outcomes
4. **Export Data**: Download your data for backup or external analysis
5. **Switch Themes**: Toggle between light and dark modes for comfortable viewing

## Sample Data

The app includes sample Indian stock and mutual fund data to help you get started:
- TCS (Tata Consultancy Services)
- SBI Bluechip Fund
- Infosys Limited

## Currency Format

All amounts are displayed in Indian Rupee format with proper comma separators:
- ₹1,00,000 (1 Lakh)
- ₹10,00,000 (10 Lakhs)
- ₹1,00,00,000 (1 Crore)

## Themes

- **Light Mode**: Clean white background with dark text
- **Dark Mode**: Dark background with light text
- Toggle available in the sidebar

## Data Security

- All data is stored locally in your browser session
- No external servers or databases required
- Export functionality for data backup

## Support

For issues or questions, please check the Streamlit documentation or community forums.

## License

This project is open source and available under the MIT License.
'''

with open('README.md', 'w', encoding='utf-8') as f:
    f.write(readme_content)

# 4. Create Procfile for Heroku deployment
procfile_content = '''web: streamlit run investment_journal_app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true
'''

with open('Procfile', 'w') as f:
    f.write(procfile_content)

# 5. Create setup.sh for deployment
setup_content = '''#!/bin/bash

# Setup script for deployment
mkdir -p ~/.streamlit/

echo "\\
[server]\\n\\
headless = true\\n\\
port = $PORT\\n\\
enableCORS = false\\n\\
\\n\\
[theme]\\n\\
primaryColor = '#FF6B6B'\\n\\
backgroundColor = '#FFFFFF'\\n\\
secondaryBackgroundColor = '#F0F2F6'\\n\\
textColor = '#262730'\\n\\
" > ~/.streamlit/config.toml
'''

with open('setup.sh', 'w') as f:
    f.write(setup_content)

# 6. Create .gitignore
gitignore_content = '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Streamlit
.streamlit/
'''

with open('.gitignore', 'w') as f:
    f.write(gitignore_content)

# 7. Create deployment instructions
deployment_guide = '''# Deployment Guide for Investment Journal App

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
'''

with open('DEPLOYMENT.md', 'w', encoding='utf-8') as f:
    f.write(deployment_guide)

print("✅ Complete deployment package created!")
print("\nFiles created:")
print("- investment_journal_app.py (Main application)")
print("- requirements.txt (Python dependencies)")
print("- config.toml (Streamlit configuration)")
print("- README.md (Documentation)")
print("- Procfile (Heroku deployment)")
print("- setup.sh (Setup script)")
print("- .gitignore (Git ignore file)")
print("- DEPLOYMENT.md (Deployment guide)")
print("\n🚀 Ready for deployment to any hosting provider!")

# Create a simple zip creator for download
import zipfile
import os

def create_deployment_package():
    files_to_zip = [
        'investment_journal_app.py',
        'requirements.txt',
        'config.toml',
        'README.md',
        'Procfile',
        'setup.sh',
        '.gitignore',
        'DEPLOYMENT.md'
    ]
    
    with zipfile.ZipFile('investment_journal_deployment.zip', 'w') as zipf:
        for file in files_to_zip:
            if os.path.exists(file):
                zipf.write(file)
    
    return 'investment_journal_deployment.zip'

zip_file = create_deployment_package()
print(f"\n📦 Deployment package created: {zip_file}")
print("   Download this file to deploy your application anywhere!")