#!/usr/bin/env python3
"""
Script to import questions from markdown files into the database.
Supports both regular questions and PRO-only exam questions.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from flask import Flask
from backend import create_app
from backend.utils.markdown_repository import MarkdownQuestionRepository
from backend.services.database_service import DatabaseService
from backend.models import db, Question
import re

def parse_markdown_questions(content, is_pro_only=False):
    """Parse markdown content into question objects"""
    questions = []
    
    # Split by question headers
    question_sections = re.split(r'^# Question \d+', content, flags=re.MULTILINE)
    
    for i, section in enumerate(question_sections[1:], 1):  # Skip first empty section
        try:
            question_data = parse_single_question(section, i, is_pro_only)
            if question_data:
                questions.append(question_data)
        except Exception as e:
            print(f"⚠️  Error parsing question {i}: {e}")
            continue
    
    return questions

def parse_single_question(section, question_id, is_pro_only):
    """Parse a single question section"""
    lines = section.strip().split('\n')
    
    # Extract metadata
    topic = extract_metadata(lines, '**Topic:**')
    difficulty_text = extract_metadata(lines, '**Difficulty:**')
    pro_only_text = extract_metadata(lines, '**Is PRO Only:**')
    
    # Check if this is a PRO-only question
    if pro_only_text.lower().strip() in ['true', 'yes', '1']:
        is_pro_only = True
    
    # Parse difficulty (extract number from "2 (Medium)")
    difficulty_match = re.search(r'(\d+)', difficulty_text)
    difficulty = int(difficulty_match.group(1)) if difficulty_match else 2
    
    # Extract scenario and question text
    scenario_text = extract_section(lines, '**Scenario:**', '**Question:**')
    question_text = extract_section(lines, '**Question:**', '**Options:**')
    
    # If there's no separate Question section, use the scenario text as the question
    if not question_text.strip():
        scenario_lines = scenario_text.strip().split('\n')
        question_lines = []
        for line in scenario_lines:
            line_stripped = line.strip()
            if line_stripped.startswith('**Options:**'):
                break
            if line_stripped.startswith('**Correct Answer:**'):
                break
            if line_stripped.startswith('**Explanation:**'):
                break
            question_lines.append(line)
        
        full_question = '\n'.join(question_lines).strip()
    else:
        # Combine scenario and question for the full question text
        full_question = f"{scenario_text.strip()}\n\n{question_text.strip()}"
    
    # Extract options
    options_text = extract_section(lines, '**Options:**', '**Correct Answer:**')
    options = parse_options(options_text)
    
    # Extract correct answer
    correct_answer_text = extract_metadata(lines, '**Correct Answer:**')
    correct_answer = parse_correct_answer(correct_answer_text)
    
    # Extract explanation
    explanation = extract_section(lines, '**Explanation:**', None)
    
    return {
        'question_id': question_id,
        'question': full_question,
        'options': options,
        'correct_answer': correct_answer,
        'explanation': explanation.strip(),
        'topic': topic.strip(),
        'difficulty': difficulty,
        'is_pro_only': is_pro_only
    }

def extract_metadata(lines, prefix):
    """Extract metadata from lines"""
    for line in lines:
        if line.strip().startswith(prefix):
            return line.replace(prefix, '').strip()
    return ""

def extract_section(lines, start_marker, end_marker):
    """Extract section between markers"""
    content = []
    in_section = False
    
    for i, line in enumerate(lines):
        line_stripped = line.strip()
        
        if start_marker in line_stripped:
            in_section = True
            continue
        elif end_marker and end_marker in line_stripped:
            break
        elif in_section:
            content.append(line)
    
    result = '\n'.join(content).strip()
    result = re.sub(r'^\n+', '', result)
    result = re.sub(r'\n+$', '', result)
    result = re.sub(r'```\s*\n', '```\n', result)
    result = re.sub(r'\n\s*```', '\n```', result)
    
    return result

def parse_options(options_text):
    """Parse options from text"""
    options = []
    lines = options_text.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if re.match(r'^[A-E]\.', line):
            option = line[2:].strip()  # Remove "A. " prefix
            options.append(option)
    
    return options[:5]  # Ensure max 5 options

def parse_correct_answer(answer_text):
    """Parse correct answer (A=0, B=1, etc.)"""
    if not answer_text:
        return 0
    
    answer = answer_text.strip().upper()
    if answer in ['A', '1']:
        return 0
    elif answer in ['B', '2']:
        return 1
    elif answer in ['C', '3']:
        return 2
    elif answer in ['D', '4']:
        return 3
    elif answer in ['E', '5']:
        return 4
    else:
        return 0

def import_questions_from_file(file_path, is_pro_only=False):
    """Import questions from a markdown file"""
    file_path = Path(file_path)
    
    if not file_path.exists():
        print(f"❌ File not found: {file_path}")
        return 0
    
    print(f"📖 Reading questions from: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    questions = parse_markdown_questions(content, is_pro_only)
    print(f"✅ Parsed {len(questions)} questions from markdown")
    
    app = create_app()
    with app.app_context():
        db_service = DatabaseService()
        imported_count = 0
        skipped_count = 0
        
        for question_data in questions:
            # Check if question already exists (by question_id)
            existing = Question.query.filter_by(question_id=question_data['question_id']).first()
            
            if existing:
                print(f"⏭️  Skipping question {question_data['question_id']} (already exists)")
                skipped_count += 1
                continue
            
            # Add question to database
            question = db_service.add_question_to_bank(
                question_text=question_data['question'],
                options=question_data['options'],
                correct_answer=question_data['correct_answer'],
                explanation=question_data['explanation'],
                difficulty_level=question_data['difficulty'],
                topic_category=question_data['topic'],
                is_pro_only=question_data['is_pro_only'],
                question_id=question_data['question_id']
            )
            
            if question:
                imported_count += 1
                pro_status = "PRO-only" if question_data['is_pro_only'] else "Regular"
                print(f"✅ Imported question {question_data['question_id']} ({pro_status})")
            else:
                print(f"❌ Failed to import question {question_data['question_id']}")
        
        print(f"\n📊 Import Summary:")
        print(f"   ✅ Imported: {imported_count}")
        print(f"   ⏭️  Skipped: {skipped_count}")
        print(f"   📝 Total: {len(questions)}")
        
        return imported_count

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Import questions from markdown files')
    parser.add_argument('file', help='Path to markdown file')
    parser.add_argument('--pro-only', action='store_true', 
                       help='Mark all questions as PRO-only')
    parser.add_argument('--regular', action='store_true',
                       help='Mark all questions as regular (not PRO-only)')
    
    args = parser.parse_args()
    
    # Determine if questions are PRO-only
    is_pro_only = args.pro_only
    if args.regular:
        is_pro_only = False
    
    # If file is pro-exam-questions.md, default to PRO-only
    if 'pro-exam' in args.file.lower() or 'pro_exam' in args.file.lower():
        is_pro_only = True
        print("🔒 Detected PRO exam questions file - marking as PRO-only")
    
    imported = import_questions_from_file(args.file, is_pro_only)
    
    if imported > 0:
        print(f"\n🎉 Successfully imported {imported} questions!")
    else:
        print("\n⚠️  No questions were imported. Check if questions already exist or if there were errors.")

if __name__ == '__main__':
    main()

