"""
PDF Service for generating quiz attempt summaries
"""
import os
import tempfile
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor


class PDFService:
    """Service for generating PDF reports"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        # Title style
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=HexColor('#8b5cf6')  # Purple color
        )
        
        # Subtitle style
        self.subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=20,
            alignment=TA_CENTER,
            textColor=HexColor('#6b7280')  # Gray color
        )
        
        # Header style
        self.header_style = ParagraphStyle(
            'CustomHeader',
            parent=self.styles['Heading3'],
            fontSize=14,
            spaceAfter=12,
            textColor=HexColor('#374151')  # Dark gray
        )
        
        # Normal text style
        self.normal_style = ParagraphStyle(
            'CustomNormal',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=6,
            textColor=HexColor('#1f2937')  # Very dark gray
        )
        
        # Question style
        self.question_style = ParagraphStyle(
            'CustomQuestion',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=8,
            leftIndent=20,
            textColor=HexColor('#1f2937')
        )
        
        # Answer style
        self.answer_style = ParagraphStyle(
            'CustomAnswer',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            leftIndent=30,
            textColor=HexColor('#6b7280')
        )
    
    def generate_quiz_attempt_pdf(self, attempt_data, questions_data=None):
        """
        Generate a PDF summary of a quiz attempt
        
        Args:
            attempt_data (dict): Quiz attempt data from database
            questions_data (list): Optional list of questions with answers
            
        Returns:
            bytes: PDF file content
        """
        # Create temporary file
        tmp_file = None
        try:
            tmp_file = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
            tmp_file.close()  # Close immediately to avoid file handle issues
            
            doc = SimpleDocTemplate(
                tmp_file.name,
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72
            )
            
            # Build PDF content
            story = []
            
            # Add header with logo and title
            story.extend(self._create_header(attempt_data))
            
            # Add attempt summary
            story.extend(self._create_summary_section(attempt_data))
            
            # Add performance breakdown
            story.extend(self._create_performance_section(attempt_data))
            
            # Add questions and answers if provided
            if questions_data:
                story.extend(self._create_questions_section(questions_data))
            
            # Add footer
            story.extend(self._create_footer(attempt_data))
            
            # Build PDF
            doc.build(story)
            
            # Read the generated PDF
            with open(tmp_file.name, 'rb') as f:
                pdf_content = f.read()
            
            return pdf_content
            
        finally:
            # Clean up temporary file with error handling
            if tmp_file and os.path.exists(tmp_file.name):
                try:
                    os.unlink(tmp_file.name)
                except (OSError, PermissionError):
                    # On Windows, sometimes the file can't be deleted immediately
                    # This is not critical for the functionality
                    pass
    
    def _create_header(self, attempt_data):
        """Create PDF header with logo and title"""
        elements = []
        
        # Title
        title = Paragraph("dbt Certification Quiz", self.title_style)
        elements.append(title)
        
        # Subtitle
        subtitle = Paragraph("Attempt Summary Report", self.subtitle_style)
        elements.append(subtitle)
        
        # Attempt info
        attempt_date = datetime.fromisoformat(attempt_data['created_at'].replace('Z', '+00:00')).strftime('%B %d, %Y at %I:%M %p')
        attempt_info = f"Attempt #{attempt_data['id']} • {attempt_date}"
        info_para = Paragraph(attempt_info, self.normal_style)
        elements.append(info_para)
        
        elements.append(Spacer(1, 20))
        return elements
    
    def _create_summary_section(self, attempt_data):
        """Create summary section with key metrics"""
        elements = []
        
        # Section header
        header = Paragraph("Quiz Summary", self.header_style)
        elements.append(header)
        
        # Summary table
        summary_data = [
            ['Metric', 'Value'],
            ['Total Questions', str(attempt_data['total_questions'])],
            ['Correct Answers', str(attempt_data['correct_answers'])],
            ['Incorrect Answers', str(attempt_data['total_questions'] - attempt_data['correct_answers'])],
            ['Score Percentage', f"{attempt_data['percentage']}%"],
            ['Quiz Type', 'PRO Quiz' if attempt_data.get('is_pro_quiz') else 'Free Quiz'],
            ['Difficulty Level', str(attempt_data.get('difficulty', 'Standard'))]
        ]
        
        summary_table = Table(summary_data, colWidths=[2*inch, 3*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#8b5cf6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f9fafb')),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ALIGN', (1, 1), (1, -1), 'CENTER'),
        ]))
        
        elements.append(summary_table)
        elements.append(Spacer(1, 20))
        return elements
    
    def _create_performance_section(self, attempt_data):
        """Create performance analysis section"""
        elements = []
        
        # Section header
        header = Paragraph("Performance Analysis", self.header_style)
        elements.append(header)
        
        # Performance assessment
        percentage = attempt_data['percentage']
        if percentage >= 90:
            performance = "Excellent"
            color = HexColor('#10b981')  # Green
        elif percentage >= 80:
            performance = "Good"
            color = HexColor('#3b82f6')  # Blue
        elif percentage >= 70:
            performance = "Average"
            color = HexColor('#f59e0b')  # Yellow
        else:
            performance = "Needs Improvement"
            color = HexColor('#ef4444')  # Red
        
        performance_text = f"Your performance is rated as: <b>{performance}</b>"
        performance_para = Paragraph(performance_text, self.normal_style)
        elements.append(performance_para)
        
        # Recommendations
        if percentage < 70:
            recommendation = "Consider reviewing the topics where you struggled and take more practice quizzes to improve your understanding."
        elif percentage < 80:
            recommendation = "Good progress! Focus on the areas where you made mistakes to reach the next level."
        elif percentage < 90:
            recommendation = "Great work! You're very close to excellent performance. Review any incorrect answers."
        else:
            recommendation = "Outstanding performance! You have a strong understanding of the material."
        
        rec_para = Paragraph(f"<b>Recommendation:</b> {recommendation}", self.normal_style)
        elements.append(rec_para)
        
        elements.append(Spacer(1, 20))
        return elements
    
    def _create_questions_section(self, questions_data):
        """Create detailed questions and answers section"""
        elements = []
        
        # Section header
        header = Paragraph("Questions & Answers", self.header_style)
        elements.append(header)
        
        for question_data in questions_data:
            question_number = question_data.get('question_number', 1)
            
            # Question number and text
            question_text = f"<b>Question {question_number}:</b> {question_data.get('question_text', 'Question text not available')}"
            question_para = Paragraph(question_text, self.question_style)
            elements.append(question_para)
            
            # Show options
            options = question_data.get('options', [])
            if options:
                options_text = "<b>Options:</b><br/>"
                for i, option in enumerate(options):
                    option_letter = chr(65 + i)  # A, B, C, D
                    options_text += f"{option_letter}. {option}<br/>"
                options_para = Paragraph(options_text, self.answer_style)
                elements.append(options_para)
            
            # User's answer
            user_answer_idx = question_data.get('user_answer')
            if user_answer_idx is not None:
                user_answer_letter = chr(65 + user_answer_idx) if 0 <= user_answer_idx < len(options) else 'Invalid'
                user_answer_text = f"<b>Your Answer:</b> {user_answer_letter}"
                if question_data.get('is_correct', False):
                    user_answer_text += " ✓"
                else:
                    user_answer_text += " ✗"
                user_para = Paragraph(user_answer_text, self.answer_style)
                elements.append(user_para)
            else:
                user_para = Paragraph("<b>Your Answer:</b> Not answered", self.answer_style)
                elements.append(user_para)
            
            # Correct answer
            correct_answer_idx = question_data.get('correct_answer', 0)
            correct_answer_letter = chr(65 + correct_answer_idx) if 0 <= correct_answer_idx < len(options) else 'A'
            correct_answer_text = f"<b>Correct Answer:</b> {correct_answer_letter}"
            correct_para = Paragraph(correct_answer_text, self.answer_style)
            elements.append(correct_para)
            
            # Explanation if available
            explanation = question_data.get('explanation')
            if explanation:
                explanation_text = f"<b>Explanation:</b> {explanation}"
                explanation_para = Paragraph(explanation_text, self.answer_style)
                elements.append(explanation_para)
            
            elements.append(Spacer(1, 15))
        
        return elements
    
    def _create_footer(self, attempt_data):
        """Create PDF footer"""
        elements = []
        
        elements.append(Spacer(1, 30))
        
        # Footer text
        footer_text = f"""
        <b>Generated on:</b> {datetime.now().strftime('%B %d, %Y at %I:%M %p')}<br/>
        <b>Report ID:</b> {attempt_data['id']}<br/>
        <b>Quiz Platform:</b> dbt Certification Quiz PRO
        """
        
        footer_para = Paragraph(footer_text, self.normal_style)
        elements.append(footer_para)
        
        return elements
    
    def cleanup_old_pdfs(self, user_id, max_pdfs=10):
        """
        Clean up old PDF files for a user, keeping only the most recent ones
        
        Args:
            user_id (str): User ID
            max_pdfs (int): Maximum number of PDFs to keep
        """
        # Note: Since we're generating PDFs on-demand, we don't need to store files
        # The cleanup is handled by limiting the history display to last 10 attempts
        # This ensures users can only download PDFs for their most recent attempts
        # while the dashboard shows analytics for their complete history
        
        # In a production environment with file storage, this would:
        # 1. List all PDF files for the user
        # 2. Sort by creation date
        # 3. Delete files beyond the max_pdfs limit
        # 4. Update database records accordingly
        
        pass
