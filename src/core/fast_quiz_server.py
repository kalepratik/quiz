#!/usr/bin/env python3
"""
Enhanced Fast dbt Certification Quiz Server
Uses CSV-based question repository for easy review and maintenance.
Features:
- Interactive prompts for quiz configuration
- Random question selection from CSV repository
- Difficulty categorization (1-4)
- Easy addition of new questions via CSV
"""

import http.server
import socketserver
import webbrowser
import os
import json
import time
import socket
from pathlib import Path
import sys

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent))
from core.markdown_question_repository import MarkdownQuestionRepository

PORT = 8000

def find_available_port(start_port=8000, max_attempts=10):
    """Find an available port starting from start_port"""
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            continue
    return None

class FastQuizServer:
    def __init__(self):
        self.question_repo = MarkdownQuestionRepository('data/questions.md', 'data/questions.csv')
        self.quiz_config = None
    
    def get_quiz_config(self, num_questions, difficulty):
        """Get quiz configuration with questions from repository"""
        questions = self.question_repo.get_questions(num_questions, difficulty)
        
        # Handle difficulty name for no preference case
        if difficulty == 0 or difficulty == 5:
            difficulty_name = "Mixed"
        else:
            difficulty_name = ["Easy", "Medium", "Difficult", "Critical"][difficulty - 1]
        
        return {
            "numQuestions": num_questions,
            "difficulty": difficulty,
            "difficultyName": difficulty_name,
            "timestamp": time.time(),
            "questions": questions
        }
    
    def prompt_quiz_config(self):
        """Interactive prompts for quiz configuration"""
        print("\n🎯 dbt Certification Quiz Configuration")
        print("=" * 40)
        
        # Show available questions
        stats = self.question_repo.get_question_stats()
        print(f"📊 Available questions in repository:")
        print(f"   📚 Easy (1): {stats['easy']} questions")
        print(f"   📚 Medium (2): {stats['medium']} questions")
        print(f"   📚 Difficult (3): {stats['difficult']} questions")
        print(f"   📚 Critical (4): {stats['critical']} questions")
        print(f"   📊 Total: {stats['total']} questions")
        print()
        
        # Get number of questions
        while True:
            try:
                num_questions = int(input("How many questions do you want? (1-45): "))
                if 1 <= num_questions <= 45:
                    break
                else:
                    print("❌ Please enter a number between 1 and 45")
            except ValueError:
                print("❌ Please enter a valid number")
        
        # Get difficulty level with validation
        print("\n🎯 Difficulty Levels:")
        print("   1 - Easy: Basic concepts and commands")
        print("   2 - Medium: Intermediate concepts and scenarios")
        print("   3 - Difficult: Advanced concepts and edge cases")
        print("   4 - Critical: Complex scenarios and troubleshooting")
        print("   5 - No Preference: Random questions from all difficulty levels")
        print()
        
        while True:
            try:
                difficulty = int(input("Select difficulty level (1-5): "))
                if 1 <= difficulty <= 5:
                    if difficulty == 5:
                        # No preference - use all questions
                        difficulty = 0  # Special value for no preference
                        difficulty_level = "all"
                        available_questions = sum(len(questions) for questions in self.question_repo.questions.values())
                    else:
                        difficulty_level = self.question_repo.get_difficulty_level(difficulty)
                        available_questions = len(self.question_repo.questions[difficulty_level])
                    
                    if available_questions == 0:
                        if difficulty == 0:
                            print("❌ No questions available in the repository")
                        else:
                            print(f"❌ No questions available for difficulty {difficulty} ({difficulty_level})")
                        print("   Please select a different difficulty level.")
                        continue
                    
                    # No need to limit questions - the repository will handle mixing from other difficulties
                    pass
                    
                    break
                else:
                    print("❌ Please enter a number between 1 and 5")
            except ValueError:
                print("❌ Please enter a valid number")
        
        self.quiz_config = self.get_quiz_config(num_questions, difficulty)
        return self.quiz_config

def create_html_interface():
    """Create HTML interface"""
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Enhanced dbt Quiz</title>
    <link rel="icon" type="image/png" href="/static/android-chrome-512x512.png">
    <link rel="icon" type="image/png" sizes="512x512" href="/static/android-chrome-512x512.png">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            text-align: center;
            color: white;
            margin-bottom: 40px;
        }
        .header h1 { font-size: 2.5rem; font-weight: 700; margin-bottom: 10px; }
        .header p { font-size: 1.1rem; opacity: 0.9; }
        .quiz-container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }
        .quiz-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .quiz-content { padding: 40px; }
        .question { margin-bottom: 30px; }
        .question-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 2px solid #f7fafc;
        }
        .question-number {
            font-size: 1.1rem;
            font-weight: 600;
            color: #4299e1;
            background: #ebf8ff;
            padding: 8px 16px;
            border-radius: 20px;
        }
        .question-topic {
            font-size: 0.9rem;
            color: #718096;
            background: #f7fafc;
            padding: 6px 12px;
            border-radius: 12px;
        }
        .question-text {
            font-size: 1.3rem;
            font-weight: 600;
            color: #2d3748;
            margin-bottom: 25px;
            line-height: 1.6;
            white-space: pre-line;
        }
        
        .code-inline {
            background: #f7fafc;
            color: #2d3748;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            font-size: 0.9rem;
            border: 1px solid #e2e8f0;
            font-weight: normal;
        }
        
        .question-content-container {
            background: #ffffff;
            border: 2px solid #e2e8f0;
            border-radius: 12px;
            padding: 25px;
            margin-bottom: 20px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        }
        
        .question-content-container .scenario-section {
            margin-bottom: 20px;
        }
        
        .question-content-container .scenario-title {
            font-size: 1.1rem;
            font-weight: 600;
            color: #2b6cb0;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .question-content-container .scenario-title::before {
            content: '';
            font-size: 1.2rem;
        }
        
        .question-content-container .scenario-text {
            font-size: 1rem;
            color: #2d3748;
            line-height: 1.6;
            margin-bottom: 15px;
        }
        
        .question-content-container .question-section {
            margin-top: 20px;
        }
        
        .question-content-container .question-title {
            font-size: 1.1rem;
            font-weight: 600;
            color: #2b6cb0;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .question-content-container .question-title::before {
            content: '';
            font-size: 1.2rem;
        }
        
        .question-content-container .question-text {
            font-size: 1rem;
            color: #2d3748;
            line-height: 1.6;
        }
        
        .ascii-diagram {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 15px;
            margin: 10px 0;
            font-family: 'Courier New', monospace;
            font-size: 0.9rem;
            line-height: 1.4;
            white-space: pre;
            overflow-x: auto;
            color: #2d3748;
        }
        .options {
            display: flex;
            flex-direction: column;
            gap: 12px;
        }
        .option {
            display: flex;
            align-items: center;
            padding: 20px;
            border: 2px solid #e2e8f0;
            border-radius: 12px;
            background: white;
            cursor: pointer;
            transition: all 0.2s ease;
            text-align: left;
        }
        .option:hover {
            border-color: #4299e1;
            background: #ebf8ff;
            transform: translateY(-1px);
        }
        .option.selected {
            border-color: #4299e1;
            background: #ebf8ff;
            box-shadow: 0 4px 12px rgba(66, 153, 225, 0.2);
        }
        .option-letter {
            font-weight: 600;
            color: #718096;
            margin-right: 16px;
            min-width: 24px;
            text-align: center;
        }
        .option-text {
            flex: 1;
            font-size: 1rem;
            color: #2d3748;
            line-height: 1.5;
        }
        .navigation {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #e2e8f0;
        }
        .nav-btn {
            padding: 12px 24px;
            border: none;
            border-radius: 8px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .prev-btn { background: #e2e8f0; color: #4a5568; }
        .next-btn { background: #4299e1; color: white; }
        .submit-btn { background: #48bb78; color: white; }
        .nav-btn:hover:not(:disabled) { transform: translateY(-1px); }
        .nav-btn:disabled { opacity: 0.5; cursor: not-allowed; }
        .progress { text-align: center; margin-bottom: 20px; color: #718096; }
        .results { text-align: center; padding: 40px; }
        .score { font-size: 3rem; font-weight: 700; color: #4299e1; margin-bottom: 20px; }
        .score-text { font-size: 1.2rem; color: #718096; margin-bottom: 30px; }
        .restart-btn {
            padding: 16px 32px;
            background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
        }
                 .restart-btn:hover { transform: translateY(-2px); box-shadow: 0 10px 30px rgba(72, 187, 120, 0.3); }
         
         .config-form {
             max-width: 600px;
             margin: 0 auto;
             padding: 20px;
         }
         
         .config-section {
             margin-bottom: 32px;
         }
         
         .config-label {
             display: block;
             font-weight: 600;
             color: #374151;
             margin-bottom: 12px;
             font-size: 0.875rem;
         }
         
         .config-hint {
             margin-top: 8px;
             font-size: 0.75rem;
             color: #6b7280;
         }
         
         /* Question Pills */
         .question-pills {
             display: flex;
             flex-wrap: wrap;
             gap: 8px;
             align-items: center;
         }
         
         .question-pill {
             padding: 8px 16px;
             border-radius: 9999px;
             border: 1px solid #d1d5db;
             background: white;
             color: #1f2937;
             font-size: 0.875rem;
             cursor: pointer;
             transition: all 0.2s ease;
             font-weight: 500;
         }
         
         .question-pill:hover {
             background: #f9fafb;
             border-color: #9ca3af;
         }
         
         .question-pill.active {
             background: #059669;
             color: white;
             border-color: #059669;
             box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
         }
         
         .custom-input-container {
             position: relative;
         }
         
         .custom-input {
             width: 112px;
             padding: 8px 12px;
             border-radius: 9999px;
             border: 1px solid #d1d5db;
             font-size: 0.875rem;
             text-align: center;
             outline: none;
             transition: border-color 0.2s ease;
         }
         
         .custom-input:focus {
             border-color: #059669;
             box-shadow: 0 0 0 3px rgba(5, 150, 105, 0.1);
         }
         
         .custom-label {
             position: absolute;
             top: -8px;
             left: 16px;
             background: white;
             padding: 0 4px;
             font-size: 0.625rem;
             color: #6b7280;
         }
         
         /* Difficulty Grid */
         .difficulty-grid {
             display: grid;
             grid-template-columns: repeat(2, 1fr);
             gap: 8px;
         }
         
         @media (min-width: 640px) {
             .difficulty-grid {
                 display: flex;
                 flex-wrap: wrap;
                 gap: 8px;
             }
         }
         
         .difficulty-btn {
             padding: 8px 16px;
             border-radius: 8px;
             border: 1px solid #d1d5db;
             background: white;
             color: #1f2937;
             font-size: 0.875rem;
             cursor: pointer;
             transition: all 0.2s ease;
             font-weight: 500;
         }
         
         .difficulty-btn:hover {
             background: #f9fafb;
             border-color: #9ca3af;
         }
         
         .difficulty-btn.active {
             background: #4f46e5;
             color: white;
             border-color: #4f46e5;
             box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
         }
         
         /* Total Stats */
         .total-stats {
             border-radius: 12px;
             border: 1px solid #e5e7eb;
             background: #f9fafb;
             padding: 16px;
             display: flex;
             align-items: center;
             justify-content: space-between;
         }
         
         .total-info {
             flex: 1;
         }
         
         .total-label {
             font-size: 0.875rem;
             color: #6b7280;
             margin-bottom: 4px;
         }
         
         .total-value {
             font-size: 1.5rem;
             font-weight: 600;
             color: #111827;
         }
         
         .total-source {
             font-size: 0.75rem;
             color: #6b7280;
             text-align: right;
         }
         
         /* Start Button */
         .start-container {
             padding-top: 8px;
         }
         
         .start-btn {
             width: 100%;
             padding: 12px 24px;
             background: #059669;
             color: white;
             border: none;
             border-radius: 12px;
             font-size: 1rem;
             font-weight: 500;
             cursor: pointer;
             transition: all 0.2s ease;
             display: inline-flex;
             align-items: center;
             justify-content: center;
             gap: 8px;
         }
         
         .start-btn:hover {
             background: #047857;
             transform: translateY(-1px);
             box-shadow: 0 4px 12px rgba(5, 150, 105, 0.3);
         }
         
         .start-btn:disabled {
             background: #d1d5db;
             color: #6b7280;
             cursor: not-allowed;
             transform: none;
             box-shadow: none;
         }
         
         .review-section {
            margin-top: 30px;
            padding-top: 30px;
            border-top: 2px solid #e2e8f0;
        }
        
        .review-question {
            background: #f8fafc;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            border-left: 4px solid #4299e1;
        }
        
        .review-question.correct {
            border-left-color: #48bb78;
        }
        
        .review-question.incorrect {
            border-left-color: #f56565;
        }
        
        .review-question-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        
        .review-question-number {
            font-weight: 600;
            color: #2d3748;
        }
        
        .review-status {
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 600;
        }
        
        .review-status.correct {
            background: #c6f6d5;
            color: #22543d;
        }
        
        .review-status.incorrect {
            background: #fed7d7;
            color: #742a2a;
        }
        
        .review-answer {
            margin: 10px 0;
            padding: 10px;
            border-radius: 8px;
            font-weight: 500;
        }
        
        .review-answer.user-answer {
            background: #e2e8f0;
            border-left: 3px solid #718096;
        }
        
        .review-answer.correct-answer {
            background: #c6f6d5;
            border-left: 3px solid #48bb78;
        }
        
        .review-explanation {
            margin-top: 15px;
            padding: 15px;
            background: #ebf8ff;
            border-radius: 8px;
            border-left: 3px solid #4299e1;
        }
        
        .review-explanation-title {
            font-weight: 600;
            color: #2b6cb0;
            margin-bottom: 8px;
        }
        
        .loading { text-align: center; padding: 60px; color: white; }
        .spinner {
            width: 40px;
            height: 40px;
            border: 4px solid rgba(255, 255, 255, 0.3);
            border-top: 4px solid white;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        @media (max-width: 768px) {
            .container { padding: 10px; }
            .header h1 { font-size: 2rem; }
            .quiz-content { padding: 20px; }
            .question-text { font-size: 1.1rem; }
            .navigation { flex-direction: column; gap: 16px; }
            .nav-btn { width: 100%; justify-content: center; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>⚡ Enhanced dbt Quiz</h1>
                         <p>Random questions with unique options from Markdown repository!</p>
        </div>

        <div id="config" class="quiz-container">
            <div class="quiz-header">
                <h2>Quiz Configuration</h2>
                <p>Configure your quiz settings before starting</p>
            </div>
            
            <div class="quiz-content">
                <div class="config-form">
                    <!-- Number of Questions -->
                    <section class="config-section">
                        <label class="config-label">Number of Questions</label>
                        <div class="question-pills">
                            <button type="button" class="question-pill" data-value="5">5</button>
                            <button type="button" class="question-pill active" data-value="10">10</button>
                            <button type="button" class="question-pill" data-value="15">15</button>
                            <button type="button" class="question-pill" data-value="20">20</button>
                            <button type="button" class="question-pill" data-value="30">30</button>
                            <div class="custom-input-container">
                                <input type="number" id="customQuestionCount" min="1" max="45" class="custom-input" placeholder="custom">
                                <span class="custom-label">custom</span>
                            </div>
                        </div>
                        <p class="config-hint">You can pick a preset or type your own, up to the total available.</p>
                    </section>
                    
                    <!-- Difficulty Level -->
                    <section class="config-section">
                        <label class="config-label">Difficulty Level</label>
                        <div class="difficulty-grid">
                            <button type="button" class="difficulty-btn" data-value="1">Easy</button>
                            <button type="button" class="difficulty-btn active" data-value="2">Medium</button>
                            <button type="button" class="difficulty-btn" data-value="3">Difficult</button>
                            <button type="button" class="difficulty-btn" data-value="4">Critical</button>
                            <button type="button" class="difficulty-btn" data-value="5">No Preference</button>
                        </div>
                        <p class="config-hint">Labels only. No numeric prefixes shown.</p>
                    </section>
                    
                    <!-- Available Total -->
                    <section class="config-section">
                        <div class="total-stats">
                            <div class="total-info">
                                <p class="total-label">Total Questions Available</p>
                                <p class="total-value" id="totalCount">45</p>
                            </div>
                            <div class="total-source">From current question bank</div>
                        </div>
                    </section>
                    
                    <!-- Start Button -->
                    <div class="start-container">
                        <button class="start-btn" id="startQuizBtn" onclick="startQuiz()">Start Quiz</button>
                    </div>
                </div>
            </div>
        </div>

        <div id="loading" class="loading" style="display: none;">
            <h2>Loading Quiz...</h2>
            <div class="spinner"></div>
            <p>Loading questions from Markdown repository</p>
        </div>

        <div id="quiz" class="quiz-container" style="display: none;">
            <div class="quiz-header">
                <h2>dbt Certification Quiz</h2>
                <div class="progress" id="progress"></div>
            </div>
            
            <div class="quiz-content">
                <div id="question-container"></div>
                
                <div class="navigation">
                    <button class="nav-btn prev-btn" id="prevBtn" onclick="previousQuestion()">← Previous</button>
                    <button class="nav-btn next-btn" id="nextBtn" onclick="nextQuestion()">Next →</button>
                    <button class="nav-btn submit-btn" id="submitBtn" onclick="submitQuiz()" style="display: none;">Submit Quiz</button>
                </div>
            </div>
        </div>

        <div id="results" class="quiz-container" style="display: none;">
            <div class="quiz-header">
                <h2>Quiz Results</h2>
            </div>
            
            <div class="results">
                <div class="score" id="score"></div>
                <div class="score-text" id="scoreText"></div>
                <button class="restart-btn" onclick="restartQuiz()">Take Another Quiz</button>
            </div>
        </div>
    </div>

    <script>
        let quizData = null;
        let currentQuestion = 0;
        let answers = [];

                 window.onload = function() {
             // Show configuration screen by default
             document.getElementById('config').style.display = 'block';
             document.getElementById('loading').style.display = 'none';
             document.getElementById('quiz').style.display = 'none';
             document.getElementById('results').style.display = 'none';
             
             // Initialize configuration interactions
             initializeConfig();
         };

         function initializeConfig() {
             // Question pill interactions
             const questionPills = document.querySelectorAll('.question-pill');
             const customInput = document.getElementById('customQuestionCount');
             
             questionPills.forEach(pill => {
                 pill.addEventListener('click', function() {
                     // Remove active class from all pills
                     questionPills.forEach(p => p.classList.remove('active'));
                     // Add active class to clicked pill
                     this.classList.add('active');
                     // Update custom input value
                     customInput.value = this.dataset.value;
                     updateStartButton();
                 });
             });
             
             // Custom input interactions
             customInput.addEventListener('input', function() {
                 const value = parseInt(this.value);
                 if (value > 0 && value <= 45) {
                     // Remove active class from all pills
                     questionPills.forEach(p => p.classList.remove('active'));
                     updateStartButton();
                 }
             });
             
             // Difficulty button interactions
             const difficultyBtns = document.querySelectorAll('.difficulty-btn');
             difficultyBtns.forEach(btn => {
                 btn.addEventListener('click', function() {
                     // Remove active class from all buttons
                     difficultyBtns.forEach(b => b.classList.remove('active'));
                     // Add active class to clicked button
                     this.classList.add('active');
                     updateStartButton();
                 });
             });
             
             // Initialize start button state
             updateStartButton();
         }
         
         function updateStartButton() {
             const customInput = document.getElementById('customQuestionCount');
             const startBtn = document.getElementById('startQuizBtn');
             
             // Get selected question count
             let questionCount = parseInt(customInput.value);
             if (!questionCount || questionCount <= 0) {
                 // Check if any pill is active
                 const activePill = document.querySelector('.question-pill.active');
                 if (activePill) {
                     questionCount = parseInt(activePill.dataset.value);
                 }
             }
             
             // Validate question count - allow up to total available questions
             const canStart = questionCount > 0 && questionCount <= 45;
             
             startBtn.disabled = !canStart;
             if (canStart) {
                 startBtn.classList.remove('disabled');
             } else {
                 startBtn.classList.add('disabled');
             }
         }
         
         async function startQuiz() {
             // Get selected question count
             const customInput = document.getElementById('customQuestionCount');
             let questionCount = parseInt(customInput.value);
             if (!questionCount || questionCount <= 0) {
                 const activePill = document.querySelector('.question-pill.active');
                 questionCount = parseInt(activePill.dataset.value);
             }
             
             // Get selected difficulty
             const activeDifficultyBtn = document.querySelector('.difficulty-btn.active');
             const difficulty = parseInt(activeDifficultyBtn.dataset.value);
             
             // Show loading screen
             document.getElementById('config').style.display = 'none';
             document.getElementById('loading').style.display = 'block';
             
             // Load quiz with selected configuration
             await loadQuizData(questionCount, difficulty);
         }

                  async function loadQuizData(numQuestions = 10, difficulty = 2) {
             try {
                 // Use the configure-quiz endpoint with parameters
                 const response = await fetch(`/api/configure-quiz?num_questions=${numQuestions}&difficulty=${difficulty}`);
                 const data = await response.json();
                 
                 if (data.error) {
                     alert('Error loading quiz: ' + data.error);
                     // Go back to config screen
                     document.getElementById('loading').style.display = 'none';
                     document.getElementById('config').style.display = 'block';
                     return;
                 }
                 
                 quizData = data;
                 answers = new Array(quizData.questions.length).fill(null);
                 
                 document.getElementById('loading').style.display = 'none';
                 document.getElementById('quiz').style.display = 'block';
                 
                 showQuestion();
             } catch (error) {
                 console.error('Error loading quiz:', error);
                 alert('Error loading quiz. Please try again.');
                 // Go back to config screen
                 document.getElementById('loading').style.display = 'none';
                 document.getElementById('config').style.display = 'block';
             }
         }

        function showQuestion() {
            const question = quizData.questions[currentQuestion];
            const container = document.getElementById('question-container');
            
            document.getElementById('progress').textContent = 
                `Question ${currentQuestion + 1} of ${quizData.questions.length} (${quizData.difficultyName})`;
            
            container.innerHTML = `
                <div class="question">
                    <div class="question-header">
                        <span class="question-number">Question ${currentQuestion + 1}</span>
                        <span class="question-topic">${question.topic}</span>
                    </div>
                    
                                         <div class="question-content-container">
                         ${formatQuestionContent(question.question)}
                     </div>
                    
                    <div class="options">
                        ${question.options.map((option, index) => `
                            <div class="option ${answers[currentQuestion] === index ? 'selected' : ''}" 
                                 onclick="selectAnswer(${index})">
                                <span class="option-letter">${String.fromCharCode(65 + index)}</span>
                                                                 <span class="option-text">${formatInlineCode(option)}</span>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;
            
            updateNavigation();
        }

        function formatQuestionContent(text) {
            if (!text) return '';
            
            let content = String(text);
            
            // Check if the text contains Scenario and Question sections
            if (content.includes('Scenario:') && content.includes('Question:')) {
                // Split into sections
                const parts = content.split(/(?=Question:)/);
                const scenarioPart = parts[0];
                const questionPart = parts[1];
                
                let html = '';
                
                // Format Scenario section
                if (scenarioPart) {
                    const scenarioText = scenarioPart.replace('Scenario:', '').trim();
                    // Remove "Critical Scenario:" prefix if present
                    const cleanScenarioText = scenarioText.replace(/^Critical Scenario:\s*/i, '');
                    
                    // Check if scenario contains ASCII diagram
                    if (cleanScenarioText.includes('```')) {
                        // Split by code blocks
                        const textParts = cleanScenarioText.split(/(```[\s\S]*?```)/);
                        let formattedScenario = '';
                        
                        textParts.forEach(part => {
                            if (part.startsWith('```') && part.endsWith('```')) {
                                // This is a code block - format as ASCII diagram
                                const diagram = part.replace(/```/g, '').trim();
                                formattedScenario += `<pre class="ascii-diagram">${diagram}</pre>`;
                            } else if (part.trim()) {
                                // This is regular text
                                formattedScenario += `<div>${formatInlineCode(part)}</div>`;
                            }
                        });
                        
                        html += `
                            <div class="scenario-section">
                                <div class="scenario-title">Scenario</div>
                                <div class="scenario-text">${formattedScenario}</div>
                            </div>
                        `;
                    } else {
                        // Regular scenario text
                        html += `
                            <div class="scenario-section">
                                <div class="scenario-title">Scenario</div>
                                <div class="scenario-text">${formatInlineCode(cleanScenarioText)}</div>
                            </div>
                        `;
                    }
                }
                
                // Format Question section
                if (questionPart) {
                    const questionText = questionPart.replace('Question:', '').trim();
                    html += `
                        <div class="question-section">
                            <div class="question-title">Question</div>
                            <div class="question-text">${formatInlineCode(questionText)}</div>
                        </div>
                    `;
                }
                
                return html;
            } else {
                // If no clear sections, just format the entire text without Scenario title
                return `<div class="question-text">${formatInlineCode(content)}</div>`;
            }
        }

        function formatInlineCode(text) {
            if (!text) return '';
            
            // Convert text to string and apply inline code formatting
            let formattedText = String(text);
            
            // Convert Markdown bold syntax to HTML
            formattedText = formattedText.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
            
            // Format DAG model names and components
            formattedText = formattedText.replace(/(\w+_orders)/g, '<span class="code-inline">$1</span>');
            formattedText = formattedText.replace(/(\w+_payments)/g, '<span class="code-inline">$1</span>');
            formattedText = formattedText.replace(/(\w+_customers)/g, '<span class="code-inline">$1</span>');
            formattedText = formattedText.replace(/(\w+_revenue)/g, '<span class="code-inline">$1</span>');
            formattedText = formattedText.replace(/(\w+_dim)/g, '<span class="code-inline">$1</span>');
            formattedText = formattedText.replace(/(\w+_stg)/g, '<span class="code-inline">$1</span>');
            formattedText = formattedText.replace(/(\w+_fct)/g, '<span class="code-inline">$1</span>');
            formattedText = formattedText.replace(/(raw_\w+)/g, '<span class="code-inline">$1</span>');
            formattedText = formattedText.replace(/(stg_\w+)/g, '<span class="code-inline">$1</span>');
            formattedText = formattedText.replace(/(fct_\w+)/g, '<span class="code-inline">$1</span>');
            formattedText = formattedText.replace(/(dim_\w+)/g, '<span class="code-inline">$1</span>');
            formattedText = formattedText.replace(/(mart_\w+)/g, '<span class="code-inline">$1</span>');
            
            // Format arrows and DAG symbols
            formattedText = formattedText.replace(/(→)/g, '<span class="code-inline">$1</span>');
            formattedText = formattedText.replace(/(↓↓↓)/g, '<span class="code-inline">$1</span>');
            
            // Format technical terms
            formattedText = formattedText.replace(/(--defer)/g, '<span class="code-inline">$1</span>');
            formattedText = formattedText.replace(/(--full-refresh)/g, '<span class="code-inline">$1</span>');
            formattedText = formattedText.replace(/(--select)/g, '<span class="code-inline">$1</span>');
            formattedText = formattedText.replace(/(CI\/CD)/g, '<span class="code-inline">$1</span>');
            formattedText = formattedText.replace(/(production state artifacts)/g, '<span class="code-inline">$1</span>');
            formattedText = formattedText.replace(/(state comparison)/g, '<span class="code-inline">$1</span>');
            formattedText = formattedText.replace(/(state artifacts)/g, '<span class="code-inline">$1</span>');
            formattedText = formattedText.replace(/(development state artifacts)/g, '<span class="code-inline">$1</span>');
            formattedText = formattedText.replace(/(state:modified\+)/g, '<span class="code-inline">$1</span>');
            formattedText = formattedText.replace(/(dbt build)/g, '<span class="code-inline">$1</span>');
            formattedText = formattedText.replace(/(dbt run)/g, '<span class="code-inline">$1</span>');
            formattedText = formattedText.replace(/(dbt test)/g, '<span class="code-inline">$1</span>');
                            // Don't format general terms like "data quality" and "foreign key" as code
                // Only format specific technical terms and model names
            
            return formattedText;
        }

        function selectAnswer(answerIndex) {
            answers[currentQuestion] = answerIndex;
            showQuestion();
        }

        function updateNavigation() {
            const prevBtn = document.getElementById('prevBtn');
            const nextBtn = document.getElementById('nextBtn');
            const submitBtn = document.getElementById('submitBtn');
            
            prevBtn.disabled = currentQuestion === 0;
            
            if (currentQuestion === quizData.questions.length - 1) {
                nextBtn.style.display = 'none';
                submitBtn.style.display = 'block';
                submitBtn.disabled = answers[currentQuestion] === null;
            } else {
                nextBtn.style.display = 'block';
                submitBtn.style.display = 'none';
                nextBtn.disabled = answers[currentQuestion] === null;
            }
        }

        function previousQuestion() {
            if (currentQuestion > 0) {
                currentQuestion--;
                showQuestion();
            }
        }

        function nextQuestion() {
            if (currentQuestion < quizData.questions.length - 1) {
                currentQuestion++;
                showQuestion();
            }
        }

        function submitQuiz() {
            let correct = 0;
            answers.forEach((answer, index) => {
                if (answer === quizData.questions[index].correctAnswer) {
                    correct++;
                }
            });
            
            const percentage = Math.round((correct / quizData.questions.length) * 100);
            
            document.getElementById('quiz').style.display = 'none';
            document.getElementById('results').style.display = 'block';
            
            document.getElementById('score').textContent = `${percentage}%`;
            document.getElementById('scoreText').textContent = 
                `You got ${correct} out of ${quizData.questions.length} questions correct`;
            
            // Add review section
            const resultsDiv = document.querySelector('.results');
            const reviewSection = document.createElement('div');
            reviewSection.className = 'review-section';
            reviewSection.innerHTML = '<h3>Question Review</h3>';
            
            quizData.questions.forEach((question, index) => {
                const userAnswer = answers[index];
                const isCorrect = userAnswer === question.correctAnswer;
                const userAnswerText = userAnswer !== null ? question.options[userAnswer] : 'Not answered';
                const correctAnswerText = question.options[question.correctAnswer];
                
                const reviewQuestion = document.createElement('div');
                reviewQuestion.className = `review-question ${isCorrect ? 'correct' : 'incorrect'}`;
                
                reviewQuestion.innerHTML = `
                    <div class="review-question-header">
                        <span class="review-question-number">Question ${index + 1}</span>
                        <span class="review-status ${isCorrect ? 'correct' : 'incorrect'}">
                            ${isCorrect ? 'Correct' : 'Incorrect'}
                        </span>
                    </div>
                    
                    <div class="question-content-container">
                        ${formatQuestionContent(question.question)}
                    </div>
                    
                    <div class="review-answer user-answer">
                        <strong>Your Answer:</strong> ${formatInlineCode(userAnswerText)}
                    </div>
                    
                    ${!isCorrect ? `
                        <div class="review-answer correct-answer">
                            <strong>Correct Answer:</strong> ${formatInlineCode(correctAnswerText)}
                        </div>
                    ` : ''}
                    
                    <div class="review-explanation">
                        <div class="review-explanation-title">Explanation:</div>
                        ${formatInlineCode(question.explanation || 'No explanation available.')}
                    </div>
                `;
                
                reviewSection.appendChild(reviewQuestion);
            });
            
            resultsDiv.appendChild(reviewSection);
        }

                 function restartQuiz() {
             // Go back to configuration screen instead of reloading
             document.getElementById('results').style.display = 'none';
             document.getElementById('config').style.display = 'block';
             
             // Reset quiz data
             quizData = null;
             answers = [];
             currentQuestion = 0;
         }
    </script>
</body>
</html>"""
    
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(html)

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, quiz_server=None, **kwargs):
        self.quiz_server = quiz_server
        super().__init__(*args, **kwargs)
    
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_GET(self):
        if self.path == '/api/quiz-config':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            # Get quiz configuration from server
            if self.quiz_server and self.quiz_server.quiz_config:
                config = self.quiz_server.quiz_config
            else:
                # Fallback to default config
                quiz_server = FastQuizServer()
                config = quiz_server.get_quiz_config(10, 2)
            
            self.wfile.write(json.dumps(config).encode())
            return
        
        if self.path.startswith('/api/configure-quiz'):
            # Parse query parameters for quiz configuration
            from urllib.parse import urlparse, parse_qs
            parsed_url = urlparse(self.path)
            params = parse_qs(parsed_url.query)
            
            try:
                num_questions = int(params.get('num_questions', [10])[0])
                difficulty = int(params.get('difficulty', [2])[0])
                
                # Validate parameters
                if not (1 <= num_questions <= 45):
                    num_questions = 10
                if not (1 <= difficulty <= 5):
                    difficulty = 2
                
                # Create new quiz configuration
                quiz_server = FastQuizServer()
                config = quiz_server.get_quiz_config(num_questions, difficulty)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(config).encode())
                return
                
            except (ValueError, KeyError):
                # Return error for invalid parameters
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                error_response = {"error": "Invalid quiz configuration parameters"}
                self.wfile.write(json.dumps(error_response).encode())
                return

        if self.path == '/' or self.path == '/index.html':
            self.path = '/templates/index.html'
            return super().do_GET()

        super().do_GET()

def main():
    os.chdir(Path(__file__).parent.parent.parent)
    
    # Create HTML interface
    create_html_interface()
    
    # Initialize quiz server (configuration will be handled in web interface)
    quiz_server = FastQuizServer()
    
    print("\n⚡ Enhanced dbt Certification Quiz")
    print("=" * 50)
    print(f"📚 Using Markdown-based question repository")
    print(f"🔄 Web-based configuration and quiz interface")
    print(f"⚡ Instant loading - no generation time!")
    print()
    
    # Get port from environment variable (for production) or use default
    import os
    port = int(os.environ.get('PORT', PORT))
    host = '0.0.0.0' if os.environ.get('PORT') else 'localhost'
    
    # Start server with quiz configuration
    def handler_factory(*args, **kwargs):
        return CustomHTTPRequestHandler(*args, quiz_server=quiz_server, **kwargs)
    
    try:
        with socketserver.TCPServer((host, port), handler_factory) as httpd:
            print(f"🚀 Starting Enhanced dbt Quiz server...")
            print(f"📱 Server running at: http://{host}:{port}")
            
            # Only open browser locally
            if host == 'localhost':
                print(f"🌐 Opening browser automatically...")
                print(f"⏹️  Press Ctrl+C to stop the server")
                print("-" * 50)
                webbrowser.open(f'http://localhost:{port}')
            else:
                print(f"🌐 Production server running on port {port}")
                print("-" * 50)

            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print(f"\n🛑 Server stopped.")
                httpd.shutdown()
    except OSError as e:
        print(f"❌ Error starting server: {e}")
        print(f"💡 Try closing other applications that might be using port {port}")

if __name__ == "__main__":
    main()
