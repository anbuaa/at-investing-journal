# Personal Investment Journal - Streamlit App

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
