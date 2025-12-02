# 🎯 dbt Certification Quiz Application

A **production-ready**, modern web-based dbt certification quiz application with comprehensive question coverage, beautiful formatting, enterprise-grade architecture, and full admin panel for user and question management. **Successfully deployed and live!** 🚀

## ✨ Features

### 🎨 User Features
- **🎨 Modern Homepage**: Professional landing page with dark/light mode, responsive design, and SEO optimization
- **🔐 OAuth Authentication**: Google OAuth integration for secure user authentication
- **💳 Payment Integration**: PRO plan upgrade flow with Razorpay integration
- **📊 Quiz System**: 
  - Regular users: Access to 10 easy questions per quiz
  - PRO users: Access to all questions (up to 45 per quiz) including PRO-only content
  - Smart question selection with difficulty filtering
  - Comprehensive review with detailed explanations
- **📈 Dashboard & History**: PRO users get detailed analytics and quiz history
- **📧 Contact Form**: Professional contact form with email notifications
- **📋 Legal Pages**: Complete Privacy Policy, Terms & Conditions, and Cancellation Policy

### 👨‍💼 Admin Features
- **🔐 Admin Panel**: Full-featured admin interface for managing users and questions
- **👥 User Management**:
  - View all users with role, PRO status, and activity
  - Toggle user active/inactive status (preserves data, removes access)
  - Change user roles (Regular, Pro, Admin)
  - Delete users with cascade deletion of all related data
- **📝 Question Management**:
  - View all questions with topic, difficulty, type, and status
  - Toggle question active/inactive status
  - Change question type (Regular/PRO-only)
  - Question statistics and counts
- **🎯 Role-Based Access Control**:
  - Three user roles: Regular, Pro, Admin
  - Admin users have access to all PRO features plus admin panel
  - Regular users limited to 10 questions per quiz
  - PRO users can access up to 45 questions per quiz

## 🏗️ Project Structure

```
dbt-certification-quiz/
├── 📁 backend/                      # Main application backend
│   ├── 📁 config/                  # Configuration management
│   │   └── __init__.py             # Environment-based configuration
│   ├── 📁 data/                     # Data storage
│   │   └── questions.md             # Question bank in Markdown format
│   ├── 📁 models/                   # Database models
│   │   ├── __init__.py              # Database initialization
│   │   ├── user_models.py           # User and Subscription models
│   │   └── quiz_models.py           # Question, QuizAttempt models
│   ├── 📁 routers/                  # Route handlers
│   │   ├── __init__.py              # Blueprint initialization
│   │   ├── main.py                  # Main UI and API routes
│   │   └── admin/                   # Admin routes
│   │       └── __init__.py          # Admin panel routes
│   ├── 📁 services/                 # Business logic layer
│   │   ├── database_service.py      # Database operations
│   │   ├── oauth_service.py         # OAuth authentication
│   │   ├── quiz_service.py          # Quiz logic and question selection
│   │   ├── scoring_service.py       # Scoring and results
│   │   ├── payment_service.py       # Razorpay payment integration
│   │   ├── email_service.py          # Email notifications
│   │   └── pdf_service.py           # PDF generation
│   ├── 📁 templates/                # HTML templates
│   │   ├── base.html                # Base template with navigation
│   │   ├── homepage.html            # Landing page
│   │   ├── index.html               # Quiz interface
│   │   ├── signin.html              # OAuth sign-in
│   │   ├── payment.html             # PRO upgrade page
│   │   ├── dashboard.html           # PRO dashboard
│   │   ├── history.html             # Quiz history
│   │   └── admin.html               # Admin panel
│   ├── 📁 static/                   # Static assets
│   │   └── *.png                    # Logos and favicons
│   ├── 📁 utils/                    # Utility functions
│   │   └── markdown_repository.py   # Markdown parsing utilities
│   ├── 📁 tests/                    # Test suite
│   │   ├── test_routes.py           # Route tests
│   │   └── test_repo.py             # Repository tests
│   └── __init__.py                  # App factory
│
├── 📁 scripts/                      # Utility scripts
│   └── import_questions.py          # Import questions from Markdown
│
├── 📄 main.py                       # Development entry point
├── 📄 wsgi.py                       # Production entry point
├── 📄 requirements.txt              # Python dependencies
├── 📄 render.yaml                   # Render deployment config
├── 📄 env.example                   # Environment variables template
└── 📄 README.md                     # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- PostgreSQL database (for production) or SQLite (for development)
- Google OAuth credentials (for authentication)
- Razorpay account (for payments)

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

3. **Set up environment variables**
   ```bash
   cp env.example .env
   ```
   Edit `.env` and configure:
   ```bash
   # Database
   DATABASE_URL=postgresql://user:password@localhost/dbname
   # Or for SQLite: sqlite:///quiz.db
   
   # Google OAuth
   GOOGLE_CLIENT_ID=your-client-id
   GOOGLE_CLIENT_SECRET=your-client-secret
   
   # Razorpay (optional for development)
   RAZORPAY_KEY_ID=your-key-id
   RAZORPAY_KEY_SECRET=your-key-secret
   
   # Flask
   FLASK_ENV=development
   SECRET_KEY=your-secret-key
   ```

4. **Initialize the database**
   ```bash
   python -c "from backend import create_app; from backend.models import db; app = create_app(); app.app_context().push(); db.create_all()"
   ```

5. **Import questions (optional)**
   ```bash
   python scripts/import_questions.py backend/data/questions.md
   ```

6. **Run the application**
   ```bash
   python main.py
   # Choose option 1 to start development server
   ```
   Or directly:
   ```bash
   flask run
   # Or
   python wsgi.py
   ```

7. **Access the application**
   - **Homepage**: `http://localhost:5000`
   - **Quiz**: `http://localhost:5000/quiz`
   - **Admin Panel**: `http://localhost:5000/admin` (requires Admin role)
   - **Health Check**: `http://localhost:5000/healthz`

## 🗄️ Database Schema

### Users Table
- `id`: Primary key
- `email`: Unique email address
- `name`: User's full name
- `google_id`: Google OAuth ID
- `is_pro`: Boolean flag for PRO access
- `role`: User role ('regular', 'pro', 'admin')
- `is_active`: Active/inactive status
- `created_at`, `updated_at`: Timestamps

### Questions Table
- `id`: Primary key
- `question_id`: Unique question identifier
- `question_text`: Full question text with scenario
- `options`: JSON array of answer options
- `correct_answer`: 0-based index of correct answer
- `explanation`: Detailed explanation
- `difficulty_level`: 1 (Easy) to 4 (Critical)
- `topic_category`: Question topic/category
- `is_active`: Active/inactive status
- `is_pro_only`: PRO-only flag
- `created_at`, `updated_at`: Timestamps

### Quiz Attempts Table
- `id`: Primary key
- `user_id`: Foreign key to users
- `question_count`: Number of questions in quiz
- `difficulty`: Difficulty level used
- `correct_answers`: Number of correct answers
- `total_questions`: Total questions attempted
- `percentage`: Score percentage
- `is_pro_quiz`: Whether PRO questions were included
- `created_at`: Timestamp

### Subscriptions Table
- `id`: Primary key
- `user_id`: Foreign key to users
- `razorpay_payment_id`: Payment ID from Razorpay
- `razorpay_order_id`: Order ID from Razorpay
- `amount`: Payment amount in paise
- `currency`: Currency code (INR)
- `status`: Payment status
- `subscription_start`, `subscription_end`: Subscription period
- `created_at`, `updated_at`: Timestamps

## 👨‍💼 Admin Panel

### Access
- Only users with `role='admin'` can access the admin panel
- Default admin: `kpratik64@gmail.com` (set during initial setup)
- Admin users automatically have PRO access

### Features

#### User Management
- **View Users**: See all users with ID, name, email, role, PRO status, active status, and quiz attempts
- **Toggle Active Status**: Activate/deactivate users (preserves data, removes access)
- **Change Role**: Update user role (Regular, Pro, Admin)
- **Delete User**: Permanently delete user and all related data (quiz attempts, subscriptions)

#### Question Management
- **View Questions**: See all questions with ID, text, topic, difficulty, type, and status
- **Toggle Active Status**: Activate/deactivate questions
- **Change Type**: Switch between Regular and PRO-only
- **Statistics**: View total, regular, and PRO-only question counts

### API Endpoints

#### User Management
- `GET /api/admin/users` - Get all users
- `POST /api/admin/user/<id>/update-role` - Update user role
- `POST /api/admin/user/<id>/toggle-active` - Toggle user active status
- `DELETE /api/admin/user/<id>/delete` - Delete user

#### Question Management
- `GET /api/admin/questions` - Get all questions
- `POST /api/admin/question/<id>/toggle-active` - Toggle question active status
- `POST /api/admin/question/<id>/update-type` - Update question type

## 🎯 Question Segregation

### Regular Users
- Can access **only regular questions** (is_pro_only=False)
- Limited to **10 questions per quiz**
- See only easy questions (difficulty level 1) by default

### PRO Users
- Can access **all questions** (both regular and PRO-only)
- Can take **up to 45 questions per quiz**
- Access to all difficulty levels (Easy, Medium, Difficult, Critical)

### Question Distribution
- **Total Questions**: 35
- **Regular Questions**: 10 (Easy difficulty)
- **PRO-only Questions**: 25 (Medium, Difficult, Critical)

## 🔐 Authentication & Authorization

### User Roles
1. **Regular**: Basic access, 10 questions per quiz, regular questions only
2. **Pro**: PRO access, up to 45 questions per quiz, all questions
3. **Admin**: Full access including admin panel, all PRO features

### Access Control
- **Authentication**: Google OAuth required for all protected routes
- **Authorization**: Role-based access control (RBAC)
- **Active Status**: Inactive users cannot log in (data preserved)
- **Session Management**: Flask sessions with secure token handling

## 💳 Payment Integration

### Razorpay Setup
1. Create Razorpay account at [razorpay.com](https://razorpay.com)
2. Get API keys from dashboard
3. Configure environment variables:
   ```bash
   RAZORPAY_KEY_ID=your-key-id
   RAZORPAY_KEY_SECRET=your-key-secret
   ```

### Payment Flow
1. User clicks "Upgrade to PRO"
2. Razorpay payment form displayed
3. Payment processed via Razorpay
4. User upgraded to PRO on successful payment
5. Subscription record created in database

## 📧 Email Configuration

### Gmail Setup
1. Enable 2-Step Verification
2. Generate App Password
3. Configure environment variables:
   ```bash
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USERNAME=your-email@gmail.com
   SMTP_PASSWORD=your-app-password
   FROM_EMAIL=your-email@gmail.com
   TO_EMAIL=admin@example.com
   ```

## 🚀 Deployment

### Render (Recommended)

1. **Create Render Account**: Sign up at [render.com](https://render.com)

2. **Create New Web Service**:
   - Connect your GitHub repository
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn wsgi:app`

3. **Configure Environment Variables**:
   - Add all variables from `.env` file
   - Set `FLASK_ENV=production`

4. **Database Setup**:
   - Create PostgreSQL database on Render
   - Add `DATABASE_URL` to environment variables

5. **Deploy**: Render will automatically deploy on push to main branch

### Environment Variables for Production
```bash
DATABASE_URL=postgresql://user:pass@host:5432/dbname
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-client-secret
RAZORPAY_KEY_ID=your-key-id
RAZORPAY_KEY_SECRET=your-key-secret
FLASK_ENV=production
SECRET_KEY=your-secret-key
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

## 🧪 Testing

### Run Tests
```bash
pytest backend/tests/ -v
```

### Test Coverage
- Route tests: API endpoints and UI routes
- Repository tests: Data access layer
- Service tests: Business logic
- Integration tests: End-to-end flows

## 🔧 Development

### Code Quality
```bash
# Format code
black backend/ scripts/

# Lint code
ruff check backend/ scripts/

# Type checking
mypy backend/
```

### Database Migrations
For schema changes, create migration scripts in `scripts/` directory.

### Adding Questions
1. Add questions to `backend/data/questions.md` in Markdown format
2. Run import script:
   ```bash
   python scripts/import_questions.py backend/data/questions.md
   ```

## 📚 Question Format

Questions are stored in Markdown format with the following structure:

```markdown
# Question 1

**Topic:** dbt Models
**Difficulty:** 2 (Medium)
**Is PRO Only:** false

**Scenario:**
Your project has a model that needs to...

**Question:**
What command would you use to...

**Options:**
A. dbt run
B. dbt compile
C. dbt test
D. dbt seed

**Correct Answer:** A

**Explanation:**
The correct answer is A because...
```

## 🎯 Features Roadmap

### Completed ✅
- [x] Admin panel with user and question management
- [x] Role-based access control (Regular, Pro, Admin)
- [x] User active/inactive toggle
- [x] Question active/inactive toggle
- [x] Question type management (Regular/PRO-only)
- [x] Question segregation by user type
- [x] User deletion with cascade
- [x] Custom confirmation and alert popups
- [x] Repository restructuring

### Future Enhancements 🚀
- [ ] Bulk question import/export
- [ ] Question search and filtering
- [ ] Advanced analytics dashboard
- [ ] Email notifications for admin actions
- [ ] Question versioning
- [ ] User activity logs
- [ ] Export quiz results to PDF
- [ ] API rate limiting
- [ ] Two-factor authentication

## 🤝 Contributing

We welcome contributions! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For questions or issues:
- Open an issue on GitHub
- Check the documentation
- Review the question bank in `backend/data/questions.md`

## 🎉 Acknowledgments

- Built with Flask and modern Python practices
- Uses PostgreSQL for reliable data storage
- Integrated with Google OAuth and Razorpay
- Deployed on Render for production hosting

---

**Made with ❤️ for the dbt community**
