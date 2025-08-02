from flask import render_template, request, flash, redirect, url_for, jsonify
from app import app, db
from models import CaseQuery, CaseResult
from scraper import scrape_case_data
import logging

logger = logging.getLogger(__name__)

@app.route('/')
def index():
    """Main page with case lookup form"""
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search_case():
    """Handle case search form submission"""
    try:
        # Get form data
        case_type = request.form.get('case_type')
        case_number = request.form.get('case_number', '').strip()
        filing_year = request.form.get('filing_year')
        
        # Validate form data
        if not case_type or not case_number or not filing_year:
            flash('All fields are required. Please fill in Case Type, Case Number, and Filing Year.', 'error')
            return redirect(url_for('index'))
        
        try:
            filing_year = int(filing_year)
            if filing_year < 1950 or filing_year > 2024:
                flash('Filing year must be between 1950 and 2024.', 'error')
                return redirect(url_for('index'))
        except ValueError:
            flash('Filing year must be a valid number.', 'error')
            return redirect(url_for('index'))
        
        # Log the query
        query = CaseQuery(
            case_type=case_type,
            case_number=case_number,
            filing_year=filing_year,
            source_court='Delhi High Court'  # Default court for demo
        )
        db.session.add(query)
        db.session.commit()
        
        logger.info(f"New case query: {case_type}/{case_number}/{filing_year}")
        
        # Attempt to scrape case data
        scrape_result = scrape_case_data(case_type, case_number, filing_year)
        
        if scrape_result['success']:
            # Update query status
            query.status = 'success'
            query.raw_response = str(scrape_result.get('raw_data', ''))
            
            # Store case result
            case_result = CaseResult(
                query_id=query.id,
                petitioner_name=scrape_result.get('petitioner_name'),
                respondent_name=scrape_result.get('respondent_name'),
                filing_date=scrape_result.get('filing_date'),
                next_hearing_date=scrape_result.get('next_hearing_date'),
                case_status=scrape_result.get('case_status'),
                judge_name=scrape_result.get('judge_name'),
                pdf_links=str(scrape_result.get('pdf_links', []))
            )
            db.session.add(case_result)
            db.session.commit()
            
            return render_template('results.html', 
                                 query=query, 
                                 result=case_result,
                                 success=True)
        else:
            # Update query with error
            query.status = 'failed'
            query.error_message = scrape_result.get('error', 'Unknown error occurred')
            db.session.commit()
            
            flash(f"Case lookup failed: {scrape_result.get('error', 'Unknown error')}", 'error')
            return render_template('results.html', 
                                 query=query, 
                                 result=None,
                                 success=False,
                                 error=scrape_result.get('error'))
    
    except Exception as e:
        logger.error(f"Error in search_case: {str(e)}")
        flash('An unexpected error occurred. Please try again.', 'error')
        return redirect(url_for('index'))

@app.route('/history')
def query_history():
    """Show query history"""
    queries = CaseQuery.query.order_by(CaseQuery.query_timestamp.desc()).limit(50).all()
    return render_template('history.html', queries=queries)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
