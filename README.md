# 🎯 dbt Certification Quiz Application

A comprehensive web-based quiz application designed to help users prepare for dbt (data build tool) certification exams. Features a modern, interactive interface with rich text formatting, flexible question selection, and detailed explanations.

## ✨ Features

### 🎨 **Modern Web Interface**
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Rich Text Formatting**: Beautiful rendering of questions with:
  - ASCII diagrams for DAG representations
  - Code blocks and inline code highlighting
  - Bold text and section formatting
  - Clean typography and spacing

### 🎯 **Flexible Quiz Configuration**
- **Question Count Selection**: Choose from 5, 10, 15, 20, or 30 questions, or enter a custom number
- **Difficulty Levels**: 
  - Easy: Basic concepts and commands
  - Medium: Intermediate concepts and scenarios
  - Difficult: Advanced concepts and edge cases
  - Critical: Complex scenarios and troubleshooting
  - **No Preference**: Random questions from all difficulty levels

### 🧠 **Smart Question Selection**
- **Primary Selection**: Gets as many questions as possible from the selected difficulty level
- **Fallback Selection**: Automatically fills remaining slots with random questions from other difficulty levels
- **No Limitations**: Request more questions than available in a single difficulty

### 📊 **Comprehensive Review System**
- **Detailed Results**: Shows each question with your answer and the correct answer
- **Explanations**: Provides detailed explanations for all questions
- **Score Tracking**: Displays your final score and performance
- **Review Mode**: Review all questions after completion

### 📚 **Rich Question Bank**
- **45+ Questions**: Comprehensive coverage of dbt topics
- **Markdown Format**: Human-readable question format with rich formatting
- **Topics Covered**:
  - DAG Execution and Dependencies
  - Commands and Flags (`--full-refresh`, `--defer`, `--state`)
  - State Management and CI/CD
  - Incremental Models and Snapshots
  - Data Quality and Production Scenarios

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- Modern web browser

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/dbt-certification-quiz.git
   cd dbt-certification-quiz
   ```

2. **Run the application**
   ```bash
   # Option 1: Use the batch file (Windows)
   .\start_server.bat
   
   # Option 2: Run directly with Python
   python src/core/fast_quiz_server.py
   ```

3. **Open your browser**
   - Navigate to: `http://localhost:8000`
   - The application will open automatically in your default browser

## 📖 Usage Guide

### 1. **Configure Your Quiz**
- Select the number of questions you want to attempt
- Choose your preferred difficulty level
- Click "Start Quiz" to begin

### 2. **Take the Quiz**
- Read each question carefully
- Select your answer from the multiple-choice options
- Use the navigation buttons to move between questions
- Submit when you're ready to see your results

### 3. **Review Your Results**
- See your final score and performance
- Review each question with explanations
- Understand where you went wrong
- Learn from detailed explanations

## 🏗️ Project Structure

```
dbt certification/
├── data/
│   ├── questions.md          # Main question bank in Markdown format
│   └── questions.csv         # Legacy CSV format (for reference)
├── src/
│   └── core/
│       ├── fast_quiz_server.py           # Main Flask server
│       └── markdown_question_repository.py # Question repository logic
├── templates/
│   └── index.html            # Web interface template
├── static/                   # Static assets
├── docs/                     # Documentation
├── main.py                   # Entry point for CLI mode
├── start_server.bat          # Windows batch file for easy startup
└── README.md                 # This file
```

## 🛠️ Technical Details

### **Backend**
- **Framework**: Flask (Python)
- **Question Repository**: Custom Markdown parser with flexible selection logic
- **API Endpoints**: RESTful API for quiz configuration and data retrieval

### **Frontend**
- **HTML5/CSS3**: Modern, responsive design
- **Vanilla JavaScript**: No external dependencies
- **Rich Text Rendering**: Custom formatting for questions and explanations

### **Question Format**
Questions are stored in Markdown format with the following structure:
```markdown
# Question X
**Topic:** [Topic Name]
**Difficulty:** [1-4] ([Easy/Medium/Difficult/Critical])

**Scenario:**
[Question scenario with ASCII diagrams]

**Question:**
[The actual question]

**Options:**
A. [Option A]
B. [Option B]
C. [Option C]
D. [Option D]
E. [Option E]

**Correct Answer:** [A-E]

**Explanation:**
[Detailed explanation of the correct answer]
```

## 🎯 Question Categories

### **DAG Execution & Dependencies**
- Understanding dependency chains
- Model execution order
- Failure handling and cascading effects

### **Commands & Flags**
- `dbt build` variations
- `--full-refresh` behavior
- `--defer` and `--state` usage
- `--fail-fast` and other flags

### **State Management & CI/CD**
- State artifacts and comparison
- Slim CI implementation
- Production deployment strategies

### **Advanced Topics**
- Incremental models and logic
- Snapshots and historical tracking
- Data quality and production scenarios
- Model contracts and cross-project references

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### **Adding Questions**
1. Edit `data/questions.md`
2. Follow the existing question format
3. Include ASCII diagrams for DAG scenarios
4. Provide clear explanations

### **Improving Features**
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

### **Reporting Issues**
- Use GitHub Issues to report bugs
- Include steps to reproduce
- Provide system information

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- Built for dbt certification preparation
- Inspired by the dbt community
- Designed for practical learning and assessment

## 📞 Support

If you have questions or need help:
- Open an issue on GitHub
- Check the documentation in the `docs/` folder
- Review the question bank in `data/questions.md`

---

**Happy Learning! 🎓**

*This application is designed to help you prepare for dbt certification exams. Use it as a study tool to reinforce your understanding of dbt concepts and best practices.*
