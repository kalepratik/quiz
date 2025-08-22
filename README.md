# 🎯 dbt Certification Quiz Application

A **production-ready**, modern web-based dbt certification quiz application with comprehensive question coverage, beautiful formatting, and enterprise-grade architecture. **Successfully deployed and live!** 🚀

## ✨ Features

- **45+ Questions**: Comprehensive dbt certification coverage
- **Rich Text Formatting**: ASCII diagrams, code highlighting, bold text
- **Smart Question Selection**: Flexible difficulty and count options with intelligent fallback
- **Modern UI**: Beautiful, responsive web interface with React-style components
- **Comprehensive Review**: Detailed feedback after quiz completion
- **Self-Contained Questions**: Each question is complete and independent
- **Production-Ready**: App factory pattern, proper configuration management, health checks
- **Testing**: Comprehensive test coverage for routes and repository
- **Tooling**: Code formatting, linting, and type checking

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
   Navigate to `http://localhost:8000`

### 🌐 Live Demo

**The application is now deployed and available at:**
- **Live Demo**: [https://dbt-certification-quiz.onrender.com](https://dbt-certification-quiz.onrender.com)

*Your fully functional dbt certification quiz application with 45+ questions, rich text formatting, and comprehensive review system.*

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

## 🏗️ Clean Project Structure

```
dbt-certification-quiz/
├── 📁 data/
│   └── 📄 questions.md              # 45+ dbt certification questions
├── 📁 src/
│   └── 📁 quiz_app/
│       ├── 📄 __init__.py           # App factory
│       ├── 📄 config.py             # Configuration management
│       ├── 📄 routes.py             # Blueprint routes
│       ├── 📁 repo/
│       │   ├── 📄 __init__.py
│       │   └── 📄 markdown_repository.py
│       └── 📁 services/
│           ├── 📄 __init__.py
│           ├── 📄 quiz_service.py
│           └── 📄 scoring_service.py
├── 📁 tests/
│   ├── 📄 __init__.py
│   ├── 📄 test_routes.py
│   └── 📄 test_repo.py
├── 📁 templates/
│   └── 📄 index.html                # Main web interface
├── 📁 static/
│   └── 📄 android-chrome-512x512.png # App favicon
├── 📁 docs/
│   └── 📄 DEPLOYMENT.md             # Deployment guide
├── 📄 wsgi.py                       # Production entry point
├── 📄 main.py                       # Development entry point
├── 📄 pyproject.toml                # Tooling & packaging
├── 📄 requirements.txt              # Dependencies
├── 📄 render.yaml                   # Production deployment
├── 📄 env.example                   # Environment template
├── 📄 .gitignore                    # Git ignore rules
├── 📄 LICENSE                       # MIT License
├── 📄 CONTRIBUTING.md               # Contribution guidelines
├── 📄 PROJECT_SUMMARY.md            # Project overview
└── 📄 README.md                     # Main documentation
```

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
- ✅ **Comprehensive Coverage**: All major dbt certification topics
- ✅ **Testing**: Comprehensive test coverage for routes and repository
- ✅ **Code Quality**: Black, Ruff, MyPy tooling configured
- ✅ **Open Source**: Ready for community contributions

## 🎯 Question Categories

### Easy (Level 1)
- Basic dbt commands (`dbt run`, `dbt test`)
- Simple model concepts
- Basic DAG understanding

### Medium (Level 2)
- Intermediate commands (`dbt build`, `--select`)
- Model dependencies
- State management basics

### Difficult (Level 3)
- Advanced state management (`state:modified+`)
- Complex DAG scenarios
- Performance optimization

### Critical (Level 4)
- Troubleshooting complex issues
- Production deployment scenarios
- Advanced debugging techniques

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
