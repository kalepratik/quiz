# 🎯 dbt Certification Quiz Application

A **production-ready**, modern web-based dbt certification quiz application with comprehensive question coverage, beautiful formatting, and enterprise-grade architecture. **Successfully deployed and live!** 🚀

## ✨ Features

- **🎨 Modern Homepage**: Professional landing page with dark/light mode, responsive design, and SEO optimization
- **35+ Questions**: Comprehensive dbt certification coverage with realistic scenarios
- **Rich Text Formatting**: ASCII diagrams, code highlighting, bold text, and proper formatting
- **Smart Question Selection**: Flexible difficulty and count options with intelligent fallback
- **Modern UI**: Beautiful, responsive web interface with React-style components
- **Comprehensive Review**: Detailed feedback after quiz completion with explanations
- **Self-Contained Questions**: Each question is complete and independent
- **Production-Ready**: App factory pattern, proper configuration management, health checks
- **Testing**: Comprehensive test coverage for routes and repository
- **Tooling**: Code formatting, linting, and type checking
- **Render Optimized**: Optimized for Render hosting with caching, performance, and SEO

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/kalepratik/quiz.git
   cd quiz
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python main.py
   ```
   Choose option 1 to start the development server

4. **Run tests**
   ```bash
   python main.py
   ```
   Choose option 2 to run the test suite

5. **Open your browser**
   - **Homepage**: `http://localhost:8000` - Modern landing page with features and pricing
   - **Quiz Interface**: `http://localhost:8000/quiz` - Direct access to the quiz
   - **Health Check**: `http://localhost:8000/healthz` - Application health status

### 🌐 Live Demo

**The application is now deployed and available at:**
- **Live Demo**: [https://dbt-certification-quiz.onrender.com](https://dbt-certification-quiz.onrender.com)

*Your fully functional dbt certification quiz application with 35+ questions, modern homepage, rich text formatting, and comprehensive review system.*

## 🚀 Deployment

### Render Hosting (Recommended)

The application is optimized for Render hosting with:

#### **Performance Optimizations**
- **Caching Headers**: Static assets cached for 1 year, templates for 1 hour
- **CDN Resources**: External CSS/JS libraries served from CDN
- **Health Checks**: `/healthz` endpoint for monitoring
- **Auto-scaling**: Handles traffic spikes automatically

#### **SEO & Accessibility**
- **Meta Tags**: Complete SEO optimization
- **Social Cards**: Open Graph and Twitter Card support
- **Accessibility**: ARIA labels, focus management, reduced motion
- **Mobile Optimized**: Responsive design for all devices

#### **Deployment Configuration**
- **render.yaml**: Optimized configuration file included
- **Environment Variables**: Production-ready settings
- **Error Handling**: Graceful fallbacks and logging
- **Zero-downtime**: Automatic deployments with health checks

## 🏗️ Production-Ready Architecture

### App Factory Pattern
- Clean separation of concerns
- Environment-based configuration
- Blueprint-based routing
- Service layer for business logic

### Configuration Management
- Environment-specific configs (Development, Production, Testing)
- Secure secret management
- Configurable application settings

### Health Monitoring
- `/healthz` endpoint for monitoring
- Structured logging throughout
- Error handling and validation

## 🎨 Modern Homepage

The application now features a **professional landing page** that showcases the quiz capabilities:

### 🌟 Homepage Features
- **Dark/Light Mode Toggle**: Persistent theme switching with localStorage
- **Responsive Design**: Perfect on desktop, tablet, and mobile devices
- **SEO Optimized**: Meta tags, descriptions, and social media cards
- **Performance Optimized**: CDN resources, preloading, and caching
- **Accessibility**: ARIA labels, focus management, and reduced motion support
- **Interactive Elements**: Smooth animations, hover effects, and FAQ accordions
- **Professional Branding**: Modern design with dbt-themed styling

### 🎯 Homepage Sections
1. **Hero Section**: Compelling headline with sample question preview
2. **Features Grid**: 6 feature cards highlighting key benefits
3. **Pricing Section**: Free vs Pro plan comparison
4. **FAQ Section**: Expandable questions with smooth animations
5. **Professional Footer**: Complete with links and branding

### 🚀 Performance Features
- **CDN Resources**: Tailwind CSS and Font Awesome from CDN
- **Preloading**: DNS prefetch and preconnect for faster loading
- **Caching**: Optimized cache headers for static assets
- **Error Handling**: Graceful fallbacks for theme and localStorage
- **Loading States**: Smooth page transitions and loading animations

## 📚 Usage Guide

### Quiz Configuration

1. **Select Number of Questions**: Choose from 5, 10, 15, 20, or enter a custom number (up to 45)
2. **Choose Difficulty Level**:
   - **Easy**: Basic dbt concepts and commands
   - **Medium**: Intermediate scenarios and workflows
   - **Difficult**: Advanced concepts and edge cases
   - **Critical**: Complex troubleshooting scenarios
   - **No Preference**: Random questions from all difficulty levels

### Smart Question Selection

The application intelligently handles question selection:
- If you request more questions than available in your chosen difficulty, it will:
  1. Take all available questions from your selected difficulty
  2. Fill the remaining slots with random questions from other difficulties
- This ensures you always get the requested number of questions

### Question Format

Questions are stored in Markdown format (`data/questions.md`) with:
- **Scenario**: Detailed context and setup
- **Question**: Clear, specific question
- **Options**: 5 multiple-choice options
- **Explanation**: Detailed explanation of the correct answer
- **ASCII Diagrams**: Visual DAG representations
- **Code Blocks**: Properly formatted dbt commands and syntax

## 🏗️ Complete Project Structure & File Purposes

```
dbt-certification-quiz/
├── 📁 data/                          # Data storage directory
│   └── 📄 questions.md               # 35 dbt certification questions in Markdown format
│                                      # Contains all quiz questions with scenarios, options, and explanations
│
├── 📁 src/                           # Source code directory
│   └── 📁 quiz_app/                  # Main application package
│       ├── 📄 __init__.py            # App factory - creates and configures Flask application
│       ├── 📄 config.py              # Configuration management - environment-specific settings
│       ├── 📄 routes.py              # Blueprint routes - API endpoints and web routes
│       ├── 📁 repo/                  # Repository layer - data access
│       │   ├── 📄 __init__.py        # Repository package initialization
│       │   └── 📄 markdown_repository.py  # Parses questions.md and provides data access
│       └── 📁 services/              # Business logic layer
│           ├── 📄 __init__.py        # Services package initialization
│           ├── 📄 quiz_service.py    # Quiz business logic - question selection and management
│           └── 📄 scoring_service.py # Scoring logic - calculates results and statistics
│
├── 📁 tests/                         # Test suite directory
│   ├── 📄 __init__.py                # Test package initialization
│   ├── 📄 test_routes.py             # Tests for API endpoints and web routes
│   └── 📄 test_repo.py               # Tests for repository layer and data parsing
│
├── 📁 templates/                     # HTML templates directory
│   └── 📄 index.html                 # Main web interface - quiz UI with JavaScript functionality
│
├── 📁 static/                        # Static assets directory
│   └── 📄 android-chrome-512x512.png # App favicon - displayed in browser tabs
│
├── 📁 docs/                          # Documentation directory
│   ├── 📄 DEPLOYMENT.md              # Deployment guide - production deployment instructions
│   └── 📄 TOPICS.md                  # Complete dbt certification topics tracking (80+ topics)
│
├── 📄 wsgi.py                        # Production entry point - WSGI application for deployment
├── 📄 main.py                        # Development entry point - CLI interface for local development
├── 📄 pyproject.toml                 # Project configuration - tooling, packaging, and dependencies
├── 📄 requirements.txt               # Python dependencies - packages needed to run the application
├── 📄 render.yaml                    # Render deployment configuration - production deployment settings
├── 📄 env.example                    # Environment template - example environment variables
├── 📄 .gitignore                     # Git ignore rules - files to exclude from version control
├── 📄 LICENSE                        # MIT License - open source license terms
├── 📄 CONTRIBUTING.md                # Contribution guidelines - how to contribute to the project
├── 📄 PROJECT_SUMMARY.md             # Project overview - high-level project description
└── 📄 README.md                      # Main documentation - comprehensive project guide
```

### 📁 **Directory Purposes**

#### **📁 data/**
- **Purpose**: Stores all application data
- **Contents**: Markdown files containing quiz questions
- **Usage**: Questions are parsed by `markdown_repository.py` to create the quiz database

#### **📁 src/**
- **Purpose**: Contains all application source code
- **Architecture**: Follows clean architecture principles with clear separation of concerns
- **Structure**: Organized into logical packages (quiz_app, repo, services)

#### **📁 src/quiz_app/**
- **Purpose**: Main application package implementing Flask app factory pattern
- **Components**: Configuration, routing, and application initialization
- **Benefits**: Modular, testable, and production-ready architecture

#### **📁 src/quiz_app/repo/**
- **Purpose**: Data access layer (Repository pattern)
- **Responsibility**: Parses Markdown files and provides clean data interface
- **Benefits**: Separates data access from business logic

#### **📁 src/quiz_app/services/**
- **Purpose**: Business logic layer
- **Responsibility**: Handles quiz logic, question selection, and scoring
- **Benefits**: Centralized business rules and reusable logic

#### **📁 tests/**
- **Purpose**: Comprehensive test suite
- **Coverage**: Tests routes, repository, and core functionality
- **Benefits**: Ensures code quality and prevents regressions

#### **📁 templates/**
- **Purpose**: HTML templates for web interface
- **Technology**: Uses Flask's Jinja2 templating engine
- **Features**: Responsive design with modern JavaScript functionality

#### **📁 static/**
- **Purpose**: Static assets (CSS, JavaScript, images)
- **Usage**: Served directly by web server for performance
- **Contents**: Favicon and other static resources

#### **📁 docs/**
- **Purpose**: Project documentation
- **Contents**: Deployment guides, topic tracking, and technical documentation
- **Benefits**: Centralized knowledge base for contributors and users

### 📄 **File Purposes**

#### **📄 Core Application Files**

**`wsgi.py`**
- **Purpose**: Production entry point
- **Usage**: Deployed to production servers (Render, Heroku, etc.)
- **Features**: WSGI-compliant application with proper logging

**`main.py`**
- **Purpose**: Development entry point with CLI interface
- **Features**: Interactive menu for running app, tests, and development tasks
- **Usage**: `python main.py` for local development

**`src/quiz_app/__init__.py`**
- **Purpose**: App factory - creates and configures Flask application
- **Features**: Environment-based configuration, blueprint registration
- **Benefits**: Clean separation of app creation and configuration

**`src/quiz_app/config.py`**
- **Purpose**: Configuration management
- **Features**: Environment-specific settings (Development, Production, Testing)
- **Benefits**: Secure secret management and flexible configuration

**`src/quiz_app/routes.py`**
- **Purpose**: Web routes and API endpoints
- **Features**: RESTful API design, error handling, JSON responses
- **Endpoints**: Quiz configuration, question serving, statistics

#### **📄 Data Layer Files**

**`data/questions.md`**
- **Purpose**: Question database in Markdown format
- **Contents**: 35 dbt certification questions with scenarios, options, explanations
- **Format**: Structured Markdown with consistent formatting
- **Benefits**: Human-readable, version-controlled, easy to edit

**`src/quiz_app/repo/markdown_repository.py`**
- **Purpose**: Parses Markdown questions and provides data access
- **Features**: Question parsing, difficulty filtering, option shuffling
- **Benefits**: Clean data interface for business logic layer

#### **📄 Business Logic Files**

**`src/quiz_app/services/quiz_service.py`**
- **Purpose**: Quiz business logic and question management
- **Features**: Smart question selection, difficulty handling, statistics
- **Benefits**: Centralized quiz logic and reusable functionality

**`src/quiz_app/services/scoring_service.py`**
- **Purpose**: Scoring and result calculation
- **Features**: Score computation, performance analysis, result formatting
- **Benefits**: Separated scoring logic for maintainability

#### **📄 Frontend Files**

**`templates/index.html`**
- **Purpose**: Main web interface
- **Features**: Responsive design, interactive quiz, real-time feedback
- **Technology**: HTML5, CSS3, JavaScript, Bootstrap
- **Benefits**: Modern, accessible, and mobile-friendly interface

**`static/android-chrome-512x512.png`**
- **Purpose**: Application favicon
- **Usage**: Displayed in browser tabs and bookmarks
- **Benefits**: Professional branding and user recognition

#### **📄 Testing Files**

**`tests/test_routes.py`**
- **Purpose**: Tests for web routes and API endpoints
- **Coverage**: Route functionality, error handling, response formats
- **Benefits**: Ensures API reliability and prevents breaking changes

**`tests/test_repo.py`**
- **Purpose**: Tests for repository layer
- **Coverage**: Markdown parsing, data access, question filtering
- **Benefits**: Validates data layer functionality and edge cases

#### **📄 Configuration Files**

**`pyproject.toml`**
- **Purpose**: Project configuration and tooling
- **Features**: Black formatting, Ruff linting, MyPy type checking
- **Benefits**: Automated code quality and consistent formatting

**`requirements.txt`**
- **Purpose**: Python dependencies
- **Contents**: Flask, Gunicorn, Markdown parser, and other packages
- **Usage**: `pip install -r requirements.txt` for dependency installation

**`render.yaml`**
- **Purpose**: Render deployment configuration
- **Features**: Build commands, environment variables, deployment settings
- **Benefits**: Automated production deployment

**`env.example`**
- **Purpose**: Environment variables template
- **Usage**: Copy to `.env` and configure for local development
- **Benefits**: Secure configuration management

#### **📄 Documentation Files**

**`README.md`**
- **Purpose**: Main project documentation
- **Contents**: Features, setup instructions, usage guide, architecture overview
- **Benefits**: Comprehensive project introduction and user guide

**`CONTRIBUTING.md`**
- **Purpose**: Contribution guidelines
- **Contents**: How to contribute, coding standards, pull request process
- **Benefits**: Clear guidance for community contributions

**`docs/DEPLOYMENT.md`**
- **Purpose**: Deployment instructions
- **Contents**: Production deployment steps, configuration, troubleshooting
- **Benefits**: Reliable production deployment process

**`docs/TOPICS.md`**
- **Purpose**: dbt certification topics tracking
- **Contents**: 80+ topics with coverage status and priority areas
- **Benefits**: Systematic topic coverage and contribution guidance

**`PROJECT_SUMMARY.md`**
- **Purpose**: High-level project overview
- **Contents**: Project goals, architecture summary, key features
- **Benefits**: Quick project understanding for stakeholders

**`LICENSE`**
- **Purpose**: MIT open source license
- **Benefits**: Clear usage rights and contribution terms

**`.gitignore`**
- **Purpose**: Git ignore rules
- **Contents**: Files to exclude from version control (cache, logs, etc.)
- **Benefits**: Clean repository and security

## 🔧 Technical Stack

### Backend
- **Python 3.7+**: Core application logic
- **Flask 2.3.3**: Web server framework with app factory pattern
- **Gunicorn**: Production WSGI server
- **Markdown**: Question storage format
- **Python-dotenv**: Environment management

### Frontend
- **HTML5/CSS3**: Modern, responsive design
- **JavaScript**: Interactive quiz functionality
- **Rich Text Formatting**: Custom CSS for code blocks and diagrams

### Development & Testing
- **Pytest**: Testing framework
- **Black**: Code formatting
- **Ruff**: Fast Python linter
- **MyPy**: Static type checking
- **Pre-commit**: Git hooks for code quality

### Data Management
- **Repository Pattern**: Clean data access layer
- **Service Layer**: Business logic separation
- **Flexible Selection**: Smart question distribution across difficulties
- **Self-Contained**: Each question includes full context

## 🎉 Success Metrics

- ✅ **Live Deployment**: Successfully deployed and accessible at https://dbt-certification-quiz.onrender.com
- ✅ **Production Ready**: App factory pattern, proper configuration, health checks
- ✅ **Rich Formatting**: ASCII diagrams and code highlighting working
- ✅ **Smart Selection**: Flexible question selection implemented
- ✅ **Modern UI**: Professional, responsive interface
- ✅ **Comprehensive Coverage**: All major dbt certification topics (see [docs/TOPICS.md](docs/TOPICS.md) for complete list)
- ✅ **Testing**: Comprehensive test coverage for routes and repository
- ✅ **Code Quality**: Black, Ruff, MyPy tooling configured
- ✅ **Open Source**: Ready for community contributions

## 🎯 Question Coverage & Topics

### 📊 **Current Status**
- **Total Questions:** 35
- **Topics Covered:** 25/80+ (31% complete)
- **Coverage Status:** 🔄 In Progress

### 🔥 **High Priority Areas (Need Questions)**
- **dbt Cloud Setup and Configuration** (4 topics)
- **Advanced Testing** (Custom Tests, Test Configurations - 13 topics)
- **Advanced Deployment and Job Structures** (9 topics)
- **Continuous Integration and Orchestration** (8 topics)
- **Environment Management and Variables** (5 topics)

### ⚡ **Medium Priority Areas**
- **dbt Mesh and Multi-Project Collaboration** (10 topics)
- **Model Versions and Governance** (4 topics)
- **Advanced Jinja and Macros** (3 topics)
- **Cross-Project References and Orchestration** (9 topics)
- **Advanced Materialization Strategies** (11 topics)

### ✅ **Well Covered Areas (25 topics)**
- Models, Sources, Tests, Documentation, Deployment
- Snapshots, Materializations, Incremental Models
- State Management, Model Contracts, Packages
- Seeds, Jinja, Macros, Variables, Hooks, Profiles
- Exposures, Metrics, Semantic Layer, Audit
- Performance, Security, Version Control, Monitoring

### 📚 **Complete Topic List**
For a detailed breakdown of all 80+ dbt certification topics and their coverage status, see [docs/TOPICS.md](docs/TOPICS.md).

### 🎯 **Difficulty Levels**
- **Easy (Level 1)**: Basic dbt commands, simple model concepts
- **Medium (Level 2)**: Intermediate commands, model dependencies
- **Difficult (Level 3)**: Advanced state management, complex scenarios
- **Critical (Level 4)**: Troubleshooting, production deployment

## 🚀 Deployment

### ✅ **Successfully Deployed and Live!**

Your application is now **live and fully functional** at [https://dbt-certification-quiz.onrender.com](https://dbt-certification-quiz.onrender.com)

🎉 **Status: Production Ready & Deployed Successfully**

### Production Deployment

The application uses a production-ready deployment configuration:

- **WSGI Entry Point**: `wsgi.py` with proper logging
- **Gunicorn Server**: Production-grade WSGI server
- **Environment Configuration**: Production settings with proper secret management
- **Health Checks**: `/healthz` endpoint for monitoring
- **Structured Logging**: Proper log formatting for production
- **App Factory Pattern**: Clean, scalable architecture

### Deployment Options

#### **Option 1: Render (Current - Free)**
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn wsgi:app`
- **Environment**: Production with proper configuration

#### **Option 2: Heroku**
```bash
heroku create your-app-name
git push heroku main
heroku open
```

#### **Option 3: Other Cloud Providers**
- AWS Elastic Beanstalk
- Google App Engine
- Azure App Service
- DigitalOcean App Platform

## 🧪 Testing

### Run Tests
```bash
python main.py
# Choose option 2 to run tests
```

Or directly:
```bash
pytest tests/ -v
```

### Test Coverage
- **Routes**: API endpoints and UI routes
- **Repository**: Data access layer
- **Services**: Business logic
- **Configuration**: Environment settings

## 🔧 Development

### Code Quality
```bash
# Format code
black src/ tests/

# Lint code
ruff check src/ tests/

# Type checking
mypy src/
```

### Environment Setup
1. Copy `env.example` to `.env`
2. Update environment variables as needed
3. Set `FLASK_ENV=development` for local development

## 📞 Support

If you have questions or need help:
- Open an issue on GitHub
- Check the documentation in the `docs/` folder
- Review the question bank in `data/questions.md`
- Check the test suite for usage examples

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
