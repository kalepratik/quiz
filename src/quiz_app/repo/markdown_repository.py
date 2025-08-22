#!/usr/bin/env python3
"""
Markdown-based Question Repository for dbt Certification Quiz
Provides beautiful formatting for human reading while maintaining CSV compatibility.
"""

import re
import csv
import json
import random
from pathlib import Path
from datetime import datetime

class MarkdownQuestionRepository:
    def __init__(self, md_file=None, csv_file=None):
        # Use default paths if not provided
        if md_file is None:
            md_file = Path(__file__).parent.parent.parent.parent / 'data' / 'questions.md'
        if csv_file is None:
            csv_file = Path(__file__).parent.parent.parent.parent / 'data' / 'questions.csv'
        self.md_file = md_file
        self.csv_file = csv_file
        self.questions = self.load_questions_from_markdown()
        self.next_id = self.get_next_id()
    
    def load_questions_from_markdown(self):
        """Load questions from Markdown file"""
        questions = {
            'easy': [],
            'medium': [],
            'difficult': [],
            'critical': []
        }
        
        if not Path(self.md_file).exists():
            print(f"⚠️  Markdown file {self.md_file} not found. Creating empty repository.")
            return questions
        
        try:
            with open(self.md_file, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Split into individual questions
            question_blocks = self.parse_markdown_questions(content)
            
            for question_data in question_blocks:
                if question_data:
                    question = {
                        'id': question_data['id'],
                        'question': question_data['question'],
                        'options': question_data['options'],
                        'correctAnswer': question_data['correct_answer'] - 1,  # Convert to 0-based index
                        'explanation': question_data['explanation'],
                        'topic': question_data['topic'],
                        'difficulty': question_data['difficulty']
                    }
                    
                    # Add to appropriate difficulty level
                    difficulty_level = self.get_difficulty_level(question_data['difficulty'])
                    questions[difficulty_level].append(question)
            
            print(f"✅ Loaded {sum(len(q) for q in questions.values())} questions from {self.md_file}")
            
        except Exception as e:
            print(f"❌ Error loading Markdown file: {e}")
            return questions
        
        return questions
    
    def parse_markdown_questions(self, content):
        """Parse markdown content into question objects"""
        questions = []
        
        # Split by question headers
        question_sections = re.split(r'^# Question \d+', content, flags=re.MULTILINE)
        
        for i, section in enumerate(question_sections[1:], 1):  # Skip first empty section
            try:
                question_data = self.parse_single_question(section, i)
                if question_data:
                    questions.append(question_data)
            except Exception as e:
                print(f"⚠️  Error parsing question {i}: {e}")
                continue
        
        return questions
    
    def parse_single_question(self, section, question_id):
        """Parse a single question section"""
        lines = section.strip().split('\n')
        
        # Extract metadata
        topic = self.extract_metadata(lines, '**Topic:**')
        difficulty_text = self.extract_metadata(lines, '**Difficulty:**')
        
        # Parse difficulty (extract number from "2 (Medium)")
        difficulty_match = re.search(r'(\d+)', difficulty_text)
        difficulty = int(difficulty_match.group(1)) if difficulty_match else 2
        
        # Extract scenario and question text
        scenario_text = self.extract_section(lines, '**Scenario:**', '**Question:**')
        question_text = self.extract_section(lines, '**Question:**', '**Options:**')
        
        # Combine scenario and question for the full question text
        full_question = f"Scenario:\n{scenario_text.strip()}\n\nQuestion:\n{question_text.strip()}"
        
        # Extract options
        options_text = self.extract_section(lines, '**Options:**', '**Correct Answer:**')
        options = self.parse_options(options_text)
        
        # Extract correct answer
        correct_answer_text = self.extract_metadata(lines, '**Correct Answer:**')
        correct_answer = self.parse_correct_answer(correct_answer_text)
        
        # Extract explanation
        explanation = self.extract_section(lines, '**Explanation:**', None)
        
        return {
            'id': question_id,
            'question': full_question,
            'options': options,
            'correct_answer': correct_answer,
            'explanation': explanation.strip(),
            'topic': topic.strip(),
            'difficulty': difficulty
        }
    
    def extract_metadata(self, lines, prefix):
        """Extract metadata from lines"""
        for line in lines:
            if line.strip().startswith(prefix):
                return line.replace(prefix, '').strip()
        return ""
    
    def extract_section(self, lines, start_marker, end_marker):
        """Extract section between markers"""
        content = []
        in_section = False
        
        for line in lines:
            if start_marker in line:
                in_section = True
                continue
            elif end_marker and end_marker in line:
                break
            elif in_section:
                content.append(line)
        
        return '\n'.join(content)
    
    def parse_options(self, options_text):
        """Parse options from text"""
        options = []
        lines = options_text.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if re.match(r'^[A-E]\.', line):
                option = line[2:].strip()  # Remove "A. " prefix
                options.append(option)
        
        return options[:5]  # Ensure exactly 5 options
    
    def parse_correct_answer(self, answer_text):
        """Parse correct answer (A=1, B=2, etc.)"""
        if not answer_text:
            return 1
        
        answer = answer_text.strip().upper()
        if answer in ['A', '1']:
            return 1
        elif answer in ['B', '2']:
            return 2
        elif answer in ['C', '3']:
            return 3
        elif answer in ['D', '4']:
            return 4
        elif answer in ['E', '5']:
            return 5
        else:
            return 1
    
    def get_next_id(self):
        """Get the next available question ID"""
        max_id = 0
        for difficulty_questions in self.questions.values():
            for question in difficulty_questions:
                if question['id'] > max_id:
                    max_id = question['id']
        return max_id + 1
    
    def get_questions(self, num_questions, difficulty):
        """Get random questions from the repository with flexible selection"""
        if difficulty == 0:
            # No preference - get questions from all difficulty levels
            all_questions = []
            for difficulty_questions in self.questions.values():
                all_questions.extend(difficulty_questions)
            available_questions = all_questions
            selected_questions = random.sample(available_questions, min(num_questions, len(available_questions)))
        else:
            difficulty_level = self.get_difficulty_level(difficulty)
            primary_questions = self.questions[difficulty_level]
            
            # Get all questions from other difficulty levels for fallback
            other_questions = []
            for diff, questions in self.questions.items():
                if diff != difficulty_level:
                    other_questions.extend(questions)
            
            # Calculate how many questions we can get from the selected difficulty
            questions_from_selected = min(num_questions, len(primary_questions))
            remaining_needed = num_questions - questions_from_selected
            
            # Select questions from the chosen difficulty
            selected_questions = random.sample(primary_questions, questions_from_selected)
            
            # If we need more questions, get them from other difficulties
            if remaining_needed > 0 and other_questions:
                additional_questions = random.sample(other_questions, min(remaining_needed, len(other_questions)))
                selected_questions.extend(additional_questions)
        
        # Create deep copies and shuffle options for each question
        for i, question in enumerate(selected_questions):
            question_copy = question.copy()
            question_copy['options'] = question['options'].copy()
            question_copy['options'], question_copy['correctAnswer'] = self.shuffle_options(
                question_copy['options'], question_copy['correctAnswer']
            )
            # Update the question in the list
            selected_questions[i] = question_copy
        
        return selected_questions
    
    def shuffle_options(self, options, correct_answer_index):
        """Shuffle options while keeping correct answer in place"""
        options_copy = options.copy()
        correct_answer = options_copy[correct_answer_index]
        
        # Remove correct answer and shuffle others
        other_options = [opt for i, opt in enumerate(options_copy) if i != correct_answer_index]
        random.shuffle(other_options)
        
        # Reinsert correct answer at random position
        new_correct_index = random.randint(0, len(options_copy) - 1)
        other_options.insert(new_correct_index, correct_answer)
        
        return other_options, new_correct_index
    
    def get_difficulty_level(self, difficulty):
        """Convert numeric difficulty to string"""
        if difficulty == 0:
            return "all"  # Special case for no preference
        difficulty_map = {
            1: 'easy',
            2: 'medium', 
            3: 'difficult',
            4: 'critical'
        }
        return difficulty_map.get(difficulty, 'medium')
    
    def add_question_to_markdown(self, question_text, options, correct_answer_index, explanation, topic, difficulty):
        """Add a new question to the Markdown file"""
        # Create markdown format
        markdown_content = f"""
# Question {self.next_id}
**Topic:** {topic}  
**Difficulty:** {difficulty} ({self.get_difficulty_level(difficulty).title()})

**Scenario:**
{question_text}

**Question:**
What will happen?

**Options:**
A. {options[0]}
B. {options[1]}
C. {options[2]}
D. {options[3]}
E. {options[4]}

**Correct Answer:** {chr(65 + correct_answer_index)}

**Explanation:**  
{explanation}

---
"""
        
        # Append to markdown file
        with open(self.md_file, 'a', encoding='utf-8') as file:
            file.write(markdown_content)
        
        # Also add to memory
        difficulty_level = self.get_difficulty_level(difficulty)
        question_obj = {
            'id': self.next_id,
            'question': question_text,
            'options': options,
            'correctAnswer': correct_answer_index,
            'explanation': explanation,
            'topic': topic,
            'difficulty': difficulty
        }
        
        self.questions[difficulty_level].append(question_obj)
        self.next_id += 1
        
        print(f"✅ Question added successfully to Markdown!")
        print(f"📝 ID: {self.next_id - 1}")
        print(f"📚 Topic: {topic}")
        print(f"🎯 Difficulty: {difficulty} ({difficulty_level})")
        
        return question_obj
    
    def export_to_csv(self):
        """Export questions to CSV format for compatibility"""
        fieldnames = ['id', 'question', 'option_a', 'option_b', 'option_c', 'option_d', 'option_e', 'correct_answer', 'explanation', 'topic', 'difficulty']
        
        with open(self.csv_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            
            for difficulty_questions in self.questions.values():
                for question in difficulty_questions:
                    row = {
                        'id': question['id'],
                        'question': question['question'],
                        'option_a': question['options'][0],
                        'option_b': question['options'][1],
                        'option_c': question['options'][2],
                        'option_d': question['options'][3],
                        'option_e': question['options'][4],
                        'correct_answer': question['correctAnswer'] + 1,  # Convert to 1-based index
                        'explanation': question['explanation'],
                        'topic': question['topic'],
                        'difficulty': question['difficulty']
                    }
                    writer.writerow(row)
        
        print(f"✅ Questions exported to {self.csv_file}")
    
    def get_question_stats(self):
        """Get statistics about questions in the repository"""
        stats = {}
        total = 0
        for difficulty, questions in self.questions.items():
            count = len(questions)
            stats[difficulty] = count
            total += count
        stats['total'] = total
        return stats
    
    def search_questions(self, search_term, topic=None, difficulty=None):
        """Search questions by text, topic, or difficulty"""
        results = []
        search_term = search_term.lower()
        
        for diff_level, questions in self.questions.items():
            if difficulty and self.get_difficulty_level(difficulty) != diff_level:
                continue
                
            for question in questions:
                if topic and question['topic'].lower() != topic.lower():
                    continue
                    
                if (search_term in question['question'].lower() or 
                    search_term in question['explanation'].lower() or
                    any(search_term in opt.lower() for opt in question['options'])):
                    results.append(question)
        
        return results

def create_sample_markdown():
    """Create a sample markdown file with formatted questions"""
    sample_content = """# dbt Certification Questions

# Question 1
**Topic:** DAG Execution  
**Difficulty:** 2 (Medium)

**Scenario:**
You have a DAG defined as:
`seed_customers → A_stg_customers → S_customers → B_customer_dim`

You run the following command:
`dbt build --select B_customer_dim`

**Question:**
What is the execution order?

**Options:**
A. `seed_customers → A_stg_customers → S_customers → B_customer_dim → tests`
B. `seed_customers → B_customer_dim → tests`
C. `A_stg_customers → S_customers → B_customer_dim → tests`
D. `seed_customers → A_stg_customers → B_customer_dim → tests`
E. Only `B_customer_dim` runs

**Correct Answer:** A

**Explanation:**  
When selecting a specific model, dbt builds the entire upstream dependency chain including seeds, models, and snapshots, then runs tests on the selected model.

---

# Question 2
**Topic:** State Management  
**Difficulty:** 3 (Difficult)

**Scenario:**
You have a DAG defined as:
`seed_customers → A_stg_customers → S_customers → B_customer_dim`

You run the following command:
`dbt build --select state:modified+ --state prod_artifacts/ --defer`

**Question:**
If only `A_stg_customers` is modified, which models will run?

**Options:**
A. Only `A_stg_customers` runs
B. `A_stg_customers → S_customers → B_customer_dim` run
C. `A_stg_customers` and `B_customer_dim` run
D. Only `B_customer_dim` runs
E. Nothing runs

**Correct Answer:** B

**Explanation:**  
With `state:modified+` and `--defer`, the modified model and all its downstream dependencies run while upstream models use production versions.

---

# Question 3
**Topic:** Commands  
**Difficulty:** 2 (Medium)

**Scenario:**
You have a DAG defined as:
`seed_customers → A_stg_customers → S_customers → B_customer_dim`

You run the following command:
`dbt build --full-refresh`

**Question:**
What happens when you run this command?

**Options:**
A. All models are rebuilt from scratch
B. Only incremental models are forced to rebuild from scratch
C. Only snapshots are rebuilt
D. Only seeds are reloaded
E. Only tests are rerun

**Correct Answer:** B

**Explanation:**  
The `--full-refresh` flag only forces incremental models to rebuild from scratch; seeds, snapshots, and regular models run normally.

---
"""
    
    with open('data/questions.md', 'w', encoding='utf-8') as file:
        file.write(sample_content)
    
    print("✅ Sample markdown file created at data/questions.md")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "create-sample":
        create_sample_markdown()
    elif len(sys.argv) > 1 and sys.argv[1] == "export-csv":
        repo = MarkdownQuestionRepository()
        repo.export_to_csv()
    else:
        # Create sample if file doesn't exist
        if not Path('data/questions.md').exists():
            create_sample_markdown()
        
        repo = MarkdownQuestionRepository()
        print("🎯 Markdown Question Repository Created Successfully!")
        print("=" * 50)
        stats = repo.get_question_stats()
        print(f"📊 Total questions: {stats['total']}")
        print(f"📚 Easy (1): {stats['easy']}")
        print(f"📚 Medium (2): {stats['medium']}")
        print(f"📚 Difficult (3): {stats['difficult']}")
        print(f"📚 Critical (4): {stats['critical']}")
        print("\n💡 To create sample questions, run: python markdown_question_repository.py create-sample")
        print("💡 To export to CSV, run: python markdown_question_repository.py export-csv")
