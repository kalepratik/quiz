# 🤝 Contributing to dbt Certification Quiz

Thank you for your interest in contributing to the dbt Certification Quiz Application! This document provides guidelines and information for contributors.

## 🎯 How to Contribute

### Types of Contributions

We welcome various types of contributions:

1. **📝 Adding Questions**: Contribute new questions to the question bank
2. **🐛 Bug Reports**: Report issues and bugs
3. **✨ Feature Requests**: Suggest new features
4. **📚 Documentation**: Improve documentation
5. **🎨 UI/UX Improvements**: Enhance the user interface
6. **🔧 Code Improvements**: Optimize code and fix issues

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- Git
- Basic knowledge of dbt (data build tool)
- Familiarity with Markdown

### Setup Development Environment

1. **Fork the repository**
   ```bash
   # Go to the repository on GitHub and click "Fork"
   # Then clone your fork
   git clone https://github.com/YOUR_USERNAME/dbt-certification-quiz.git
   cd dbt-certification-quiz
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python src/core/fast_quiz_server.py
   ```

4. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

## 📝 Adding Questions

### Question Format

Questions should follow this Markdown format:

```markdown
# Question X
**Topic:** [Topic Name]
**Difficulty:** [1-4] ([Easy/Medium/Difficult/Critical])

**Scenario:**
[Question scenario with ASCII diagrams if applicable]

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

### Question Guidelines

1. **Quality**: Questions should be clear, accurate, and educational
2. **Difficulty**: Choose appropriate difficulty level (1-4)
3. **Topics**: Cover various dbt concepts and scenarios
4. **ASCII Diagrams**: Use ASCII diagrams for DAG scenarios
5. **Explanations**: Provide detailed, educational explanations

### Adding Your Question

1. **Edit the file**: `data/questions.md`
2. **Add your question**: Follow the format above
3. **Test locally**: Run the application to verify
4. **Submit**: Create a pull request

### Question Categories

We're looking for questions in these areas:

- **DAG Execution**: Dependency chains, execution order
- **Commands & Flags**: `dbt build`, `--full-refresh`, `--defer`, etc.
- **State Management**: State artifacts, CI/CD scenarios
- **Incremental Models**: Logic, configuration, behavior
- **Snapshots**: Historical tracking, behavior
- **Data Quality**: Production scenarios, troubleshooting
- **Model Contracts**: Cross-project references, validation

## 🐛 Reporting Bugs

### Before Reporting

1. **Check existing issues**: Search for similar issues
2. **Test locally**: Reproduce the issue on your machine
3. **Check documentation**: Review README and docs

### Bug Report Template

```markdown
**Bug Description:**
[Clear description of the bug]

**Steps to Reproduce:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Expected Behavior:**
[What should happen]

**Actual Behavior:**
[What actually happens]

**Environment:**
- OS: [Windows/Mac/Linux]
- Python Version: [3.7/3.8/3.9/etc.]
- Browser: [Chrome/Firefox/Safari/etc.]

**Additional Information:**
[Screenshots, logs, etc.]
```

## ✨ Feature Requests

### Feature Request Template

```markdown
**Feature Description:**
[Clear description of the feature]

**Use Case:**
[Why this feature would be useful]

**Proposed Implementation:**
[How you think it could be implemented]

**Additional Information:**
[Any other relevant details]
```

## 🔧 Code Contributions

### Code Style Guidelines

1. **Python**: Follow PEP 8 style guide
2. **JavaScript**: Use consistent indentation and naming
3. **HTML/CSS**: Follow modern web standards
4. **Comments**: Add comments for complex logic
5. **Documentation**: Update documentation for new features

### Development Workflow

1. **Create feature branch**
   ```bash
   git checkout -b feature/your-feature
   ```

2. **Make changes**
   - Write clean, well-documented code
   - Add tests if applicable
   - Update documentation

3. **Test your changes**
   ```bash
   python src/core/fast_quiz_server.py
   # Test the functionality manually
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature
   ```

6. **Create pull request**
   - Go to your fork on GitHub
   - Click "New Pull Request"
   - Fill out the template

### Commit Message Guidelines

Use conventional commit messages:

- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation changes
- `style:` Code style changes
- `refactor:` Code refactoring
- `test:` Adding or updating tests
- `chore:` Maintenance tasks

## 📋 Pull Request Process

### Before Submitting

1. **Test thoroughly**: Ensure everything works
2. **Update documentation**: Add/update relevant docs
3. **Follow style guidelines**: Check code formatting
4. **Write clear description**: Explain what and why

### Pull Request Template

```markdown
**Description:**
[Brief description of changes]

**Type of Change:**
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactoring
- [ ] Other (please describe)

**Testing:**
- [ ] Tested locally
- [ ] Added/updated tests
- [ ] All tests pass

**Screenshots:**
[If applicable, add screenshots]

**Additional Notes:**
[Any additional information]
```

## 🎯 Review Process

### What We Look For

1. **Functionality**: Does it work as expected?
2. **Code Quality**: Is the code clean and maintainable?
3. **Documentation**: Is it well-documented?
4. **Testing**: Are there appropriate tests?
5. **Style**: Does it follow project guidelines?

### Review Timeline

- **Initial Review**: Within 1-2 days
- **Follow-up**: Within 1 week
- **Final Decision**: Within 2 weeks

## 🏷️ Issue Labels

We use these labels to categorize issues:

- `bug`: Something isn't working
- `enhancement`: New feature or request
- `documentation`: Improvements to documentation
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention is needed
- `question`: Further information is requested

## 📞 Getting Help

### Communication Channels

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Pull Requests**: For code reviews and feedback

### Before Asking for Help

1. **Check documentation**: README, docs folder
2. **Search issues**: Look for similar problems
3. **Try to reproduce**: Ensure you can reproduce the issue
4. **Provide context**: Include relevant information

## 🎉 Recognition

### Contributors

All contributors will be recognized in:

- **README.md**: Contributors section
- **GitHub**: Contributors tab
- **Releases**: Release notes

### Types of Recognition

- **Code Contributors**: Direct code contributions
- **Question Contributors**: Adding questions to the bank
- **Documentation Contributors**: Improving docs
- **Bug Reporters**: Finding and reporting issues

## 📄 Code of Conduct

### Our Standards

- **Be respectful**: Treat everyone with respect
- **Be constructive**: Provide helpful feedback
- **Be inclusive**: Welcome diverse perspectives
- **Be patient**: Understand that everyone learns at their own pace

### Enforcement

- **Warning**: First violation gets a warning
- **Temporary ban**: Repeated violations may result in temporary ban
- **Permanent ban**: Severe violations may result in permanent ban

## 📝 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Thank You

Thank you for contributing to the dbt Certification Quiz Application! Your contributions help make this tool better for the entire dbt community.

---

**Happy Contributing! 🚀**
