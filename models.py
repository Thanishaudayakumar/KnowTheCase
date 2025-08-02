from datetime import datetime
from app import db

class CaseQuery(db.Model):
    """Model to log case lookup queries"""
    id = db.Column(db.Integer, primary_key=True)
    case_type = db.Column(db.String(100), nullable=False)
    case_number = db.Column(db.String(100), nullable=False)
    filing_year = db.Column(db.Integer, nullable=False)
    query_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    source_court = db.Column(db.String(200), nullable=True)
    status = db.Column(db.String(50), default='pending')  # pending, success, failed
    error_message = db.Column(db.Text, nullable=True)
    raw_response = db.Column(db.Text, nullable=True)
    
    def __repr__(self):
        return f'<CaseQuery {self.case_type}/{self.case_number}/{self.filing_year}>'

class CaseResult(db.Model):
    """Model to store parsed case results"""
    id = db.Column(db.Integer, primary_key=True)
    query_id = db.Column(db.Integer, db.ForeignKey('case_query.id'), nullable=False)
    petitioner_name = db.Column(db.String(500), nullable=True)
    respondent_name = db.Column(db.String(500), nullable=True)
    filing_date = db.Column(db.Date, nullable=True)
    next_hearing_date = db.Column(db.Date, nullable=True)
    case_status = db.Column(db.String(200), nullable=True)
    judge_name = db.Column(db.String(200), nullable=True)
    pdf_links = db.Column(db.Text, nullable=True)  # JSON string of PDF URLs
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    query = db.relationship('CaseQuery', backref=db.backref('results', lazy=True))
    
    def __repr__(self):
        return f'<CaseResult {self.petitioner_name} vs {self.respondent_name}>'
