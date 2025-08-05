# ValuAI - UCaaS Business Valuation Tool

[![CI](https://github.com/yourusername/valuai/workflows/CI/badge.svg)](https://github.com/yourusername/valuai/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![Node.js 16+](https://img.shields.io/badge/node-16+-green.svg)](https://nodejs.org/)

An AI-powered business valuation tool specifically designed for UCaaS (Unified Communications as a Service) companies, featuring DCF analysis, market comparables, and intelligent recommendations.

## 🚀 Features

- **DCF Analysis**: Comprehensive Discounted Cash Flow calculations
- **Market Comparables**: Real-time market data integration
- **UCaaS Metrics**: Industry-specific KPIs (MRR, ARPU, Churn, CAC, LTV)
- **AI Recommendations**: OpenAI-powered valuation insights
- **Report Generation**: PDF and Word document exports
- **File Processing**: Excel, CSV, and PDF data import
- **Interactive Dashboard**: Modern React-based UI

## 🏗️ Architecture

### Frontend (React + TypeScript)
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite for fast development
- **Styling**: Tailwind CSS
- **State Management**: React hooks and context
- **Testing**: Jest + React Testing Library

### Backend (Python Flask)
- **Framework**: Flask with SQLAlchemy ORM
- **Database**: SQLite (development) / PostgreSQL (production)
- **AI Integration**: OpenAI API
- **File Processing**: pandas, openpyxl, PyMuPDF
- **Report Generation**: python-docx, reportlab

## 📁 Project Structure

```
valuai/
├── client/                 # Frontend React application
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── pages/        # Page components
│   │   ├── services/     # API services
│   │   └── ...
│   ├── tests/            # Frontend tests
│   └── package.json
├── server/               # Backend Flask application
│   ├── models/          # Data models
│   ├── routes/          # API routes
│   ├── services/        # Business logic
│   ├── tests/           # Backend tests
│   └── requirements.txt
├── docs/                # Documentation
└── README.md
```

## 🚦 Quick Start

### Prerequisites

- **Python 3.13+**
- **Node.js 16+**
- **npm or yarn**
- **Git**

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/valuai.git
   cd valuai
   ```

2. **Setup Backend**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   
   # Install dependencies
   cd server
   pip install -r requirements.txt
   ```

3. **Setup Frontend**
   ```bash
   cd client
   npm install
   ```

4. **Environment Configuration**
   ```bash
   # Copy environment template
   cp server/.env.example server/.env
   
   # Edit .env file with your configuration
   # Add your OpenAI API key and other settings
   ```

5. **Database Setup**
   ```bash
   cd server
   python app.py  # This will create the database tables
   ```

### Running the Application

1. **Start Backend Server**
   ```bash
   cd server
   python app.py
   ```
   Backend will be available at: `http://localhost:5000`

2. **Start Frontend Development Server**
   ```bash
   cd client
   npm run dev
   ```
   Frontend will be available at: `http://localhost:5173` (or next available port)

## 🔧 Development

### Backend Development

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Format code
black .
flake8 .
```

### Frontend Development

```bash
# Run tests
npm test

# Run tests in watch mode
npm run test:watch

# Run tests with coverage
npm run test:coverage

# Build for production
npm run build

# Lint code
npm run lint
```

## 🧪 Testing

### Backend Tests
```bash
cd server
pytest tests/
```

### Frontend Tests
```bash
cd client
npm test
```

### End-to-End Tests
```bash
cd client
npm run test:e2e
```

## 📊 API Documentation

### Core Endpoints

- `GET /api/health` - Health check
- `POST /api/companies` - Create company
- `GET /api/companies/{id}` - Get company details
- `POST /api/valuations/dcf` - Calculate DCF valuation
- `POST /api/valuations/ucaas-metrics` - Calculate UCaaS metrics
- `POST /api/reports/generate` - Generate valuation report

### Example API Usage

```bash
# Create a company
curl -X POST http://localhost:5000/api/companies \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Example UCaaS Co",
    "industry": "UCaaS",
    "revenue": 10000000,
    "growth_rate": 0.25
  }'

# Calculate DCF
curl -X POST http://localhost:5000/api/valuations/dcf \
  -H "Content-Type: application/json" \
  -d '{
    "revenue": 10000000,
    "growth_rate": 0.25,
    "discount_rate": 0.12,
    "terminal_growth_rate": 0.03
  }'
```

## 🚀 Deployment

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build

# Production deployment
docker-compose -f docker-compose.prod.yml up --build
```

### Manual Deployment

1. **Backend (Flask)**
   ```bash
   # Install production dependencies
   pip install gunicorn
   
   # Run with Gunicorn
   gunicorn --bind 0.0.0.0:5000 app:app
   ```

2. **Frontend (Static Files)**
   ```bash
   # Build for production
   npm run build
   
   # Serve with nginx or similar
   ```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow TypeScript/Python type hints
- Write tests for new features
- Follow existing code style
- Update documentation for API changes
- Use conventional commit messages

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for AI integration capabilities
- React and Flask communities
- UCaaS industry data providers

## 📞 Support

- **Documentation**: Check the `/docs` folder
- **Issues**: [GitHub Issues](https://github.com/yourusername/valuai/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/valuai/discussions)

---

**Built with ❤️ for the UCaaS industry**

## Project Structure Analysis

### Current Structure Overview
```
GITHUB AI VALUTION/
├── client/                 # Frontend React application
│   ├── src/
│   │   ├── components/    # Reusable React components
│   │   │   ├── Layout.tsx
│   │   │   ├── ui/       # UI components
│   │   │   └── valuation/ # Valuation-specific components
│   │   ├── pages/        # Page components
│   │   ├── services/     # API and file services
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json      # Frontend dependencies
│   ├── tsconfig.json     # TypeScript configuration
│   ├── vite.config.ts    # Vite configuration
│   └── tailwind.config.js # TailwindCSS configuration
├── server/                # Backend Flask application
│   ├── services/         # Business logic services
│   │   ├── ai_service.py
│   │   ├── market_data.py
│   │   ├── report_generator.py
│   │   ├── ucaas_valuation.py
│   │   └── valuation.py
│   ├── routes/           # API endpoints
│   ├── models/           # Database models
│   ├── database/         # Database configuration
│   ├── app.py           # Main application entry
│   └── requirements.txt  # Python dependencies
├── .vscode/              # VS Code configuration
│   ├── launch.json      # Debug configurations
│   └── tasks.json       # Task definitions
└── README.md            # Project documentation
```

### Strengths

1. **Architecture**
   - Clear separation between frontend and backend
   - Modular service architecture
   - Well-organized component structure
   - Proper separation of concerns

2. **Development Setup**
   - Comprehensive VS Code debugging configuration
   - Task automation ready
   - Modern build tools (Vite)
   - Type safety with TypeScript

3. **Feature Organization**
   - Dedicated valuation components
   - Centralized API services
   - Reusable UI components
   - Clear file naming conventions

### Areas for Improvement

1. **Missing Directories**
   - `/tests` - Add test directories for both frontend and backend
   - `/docs` - Add API and component documentation
   - `/scripts` - Add deployment and utility scripts
   - `/config` - Centralize configuration files

2. **Code Quality Tools**
   - Add ESLint configuration
   - Set up Prettier for code formatting
   - Implement Python linting (flake8/black)
   - Add pre-commit hooks

3. **Development Environment**
   - Add Docker configuration
   - Implement CI/CD pipeline
   - Add environment-specific configurations
   - Improve secret management

4. **Documentation**
   - Add API documentation
   - Include component documentation
   - Add inline code comments
   - Create development guidelines

## Features

- Multi-step valuation wizard
- UCaaS-specific metrics analysis
- DCF (Discounted Cash Flow) calculator
- Market comparables (RingCentral, Vonage, etc.)
- AI-powered valuation recommendations
- PDF/Word report generation

## Tech Stack

### Frontend
- React + TypeScript
- Vite for build tooling
- TailwindCSS for styling
- Chart.js for visualizations

### Backend
- Python Flask
- SQLite database
- OpenAI integration
- ReportLab/python-docx for report generation

## Project Structure

```
.
├── client/              # React frontend
├── server/              # Flask backend
│   ├── app.py          # Main Flask application
│   └── requirements.txt # Python dependencies
└── README.md           # Project documentation
```

## Getting Started

### Backend Setup

1. Create and activate virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   source venv/bin/activate # Unix/macOS
   ```

2. Install dependencies:
   ```bash
   cd server
   pip install -r requirements.txt
   ```

3. Start the Flask server:
   ```bash
   python app.py
   ```

### Frontend Setup

1. Install dependencies:
   ```bash
   cd client
   npm install
   ```

2. Start development server:
   ```bash
   npm run dev
   ```

## Recommended Improvements

### 1. Testing Infrastructure (Priority: High)
```
GITHUB AI VALUTION/
├── client/
│   └── tests/           # Add frontend tests
│       ├── unit/
│       ├── integration/
│       └── e2e/
└── server/
    └── tests/          # Add backend tests
        ├── unit/
        ├── integration/
        └── fixtures/
```

- Implement Jest for frontend testing
- Add pytest for backend testing
- Set up test coverage reporting
- Add GitHub Actions for test automation

### 2. Documentation Enhancement (Priority: Medium)
```
GITHUB AI VALUTION/
└── docs/
    ├── api/           # API documentation
    ├── components/    # Component documentation
    ├── deployment/    # Deployment guides
    └── development/   # Development guidelines
```

- Add OpenAPI/Swagger documentation
- Create component storybook
- Include architectural diagrams
- Add development guidelines

### 3. Development Tools (Priority: High)
```
GITHUB AI VALUTION/
├── .github/          # GitHub workflows
├── .eslintrc.js     # ESLint configuration
├── .prettierrc      # Prettier configuration
├── setup.cfg        # Python linting configuration
└── docker/          # Docker configuration
```

- Set up linting and formatting
- Add pre-commit hooks
- Configure Docker development environment
- Implement CI/CD pipeline

### 4. Security Enhancements (Priority: High)
- Implement proper authentication
- Add request validation
- Set up CORS properly
- Implement rate limiting
- Add security headers
- Implement proper secret management

### 5. Monitoring and Logging (Priority: Medium)
- Add application logging
- Implement error tracking
- Add performance monitoring
- Set up analytics

## Valuation Methodology

The tool uses various methods to value UCaaS businesses:

1. DCF Analysis
   - Revenue growth projections
   - Cost structure analysis
   - Working capital requirements
   - Terminal value calculation

2. Market Comparables
   - Revenue multiples
   - EBITDA multiples
   - Customer metrics
   - Growth rates

3. UCaaS-Specific Metrics
   - MRR (Monthly Recurring Revenue)
   - Churn rate
   - CAC (Customer Acquisition Cost)
   - LTV (Lifetime Value)
   - Gross margins
