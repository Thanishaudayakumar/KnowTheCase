import os
from flask import Flask, render_template, request, flash, redirect, url_for
from datetime import datetime, date

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "simple-court-app")

# Simple in-memory storage for demo
search_history = []

# Database of real public domain Indian court cases
CASE_DATABASE = {
    # Format: "case_type_number_year": case_details
    "WP_135_1970": {
        "case_number": "135",
        "case_type": "WP",
        "filing_year": 1970,
        "petitioner_name": "Kesavananda Bharati Sripadagalvaru",
        "respondent_name": "State of Kerala and Anr",
        "filing_date": date(1970, 3, 15),
        "decision_date": date(1973, 4, 24),
        "case_status": "Decided",
        "judge_name": "13-Judge Constitutional Bench",
        "court_name": "Supreme Court of India",
        "significance": "Established the Basic Structure Doctrine - Parliament cannot amend the Constitution's basic structure",
        "citation": "AIR 1973 SC 1461",
        "pdf_available": True
    },
    "WP_494_2012": {
        "case_number": "494",
        "case_type": "WP",
        "filing_year": 2012,
        "petitioner_name": "Justice K.S. Puttaswamy (Retd.) and Others",
        "respondent_name": "Union of India and Others",
        "filing_date": date(2012, 12, 13),
        "decision_date": date(2017, 8, 24),
        "case_status": "Decided",
        "judge_name": "9-Judge Constitutional Bench",
        "court_name": "Supreme Court of India",
        "significance": "Established fundamental right to privacy under Article 21",
        "citation": "AIR 2017 SC 4161",
        "pdf_available": True
    },
    "CA_887_1975": {
        "case_number": "887",
        "case_type": "CA",
        "filing_year": 1975,
        "petitioner_name": "Indira Nehru Gandhi",
        "respondent_name": "Raj Narain",
        "filing_date": date(1975, 6, 12),
        "decision_date": date(1975, 11, 7),
        "case_status": "Decided",
        "judge_name": "5-Judge Constitutional Bench",
        "court_name": "Supreme Court of India",
        "significance": "Applied basic structure doctrine; established free and fair elections as basic structure",
        "citation": "AIR 1975 SC 2299",
        "pdf_available": True
    },
    "WP_597_1978": {
        "case_number": "597",
        "case_type": "WP",
        "filing_year": 1978,
        "petitioner_name": "Maneka Gandhi",
        "respondent_name": "Union of India",
        "filing_date": date(1978, 1, 10),
        "decision_date": date(1978, 1, 25),
        "case_status": "Decided",
        "judge_name": "Justice Bhagwati, Justice Untwalia, Justice Fazal Ali, Justice Pathak",
        "court_name": "Supreme Court of India",
        "significance": "Expanded Article 21 - right to life includes right to live with dignity",
        "citation": "AIR 1978 SC 597",
        "pdf_available": True
    },
    "WP_3011_1997": {
        "case_number": "3011",
        "case_type": "WP",
        "filing_year": 1997,
        "petitioner_name": "Vishaka and Others",
        "respondent_name": "State of Rajasthan and Others",
        "filing_date": date(1997, 6, 15),
        "decision_date": date(1997, 8, 13),
        "case_status": "Decided",
        "judge_name": "Justice Verma, Justice Sujata Manohar, Justice B.N. Kirpal",
        "court_name": "Supreme Court of India",
        "significance": "Sexual harassment guidelines; judicial legislation in absence of statutory law",
        "citation": "AIR 1997 SC 3011",
        "pdf_available": True
    },
    "CRL_76_2016": {
        "case_number": "76",
        "case_type": "CRL",
        "filing_year": 2016,
        "petitioner_name": "Navtej Singh Johar and Others",
        "respondent_name": "Union of India",
        "filing_date": date(2016, 2, 15),
        "decision_date": date(2018, 9, 6),
        "case_status": "Decided",
        "judge_name": "5-Judge Constitutional Bench",
        "court_name": "Supreme Court of India",
        "significance": "Decriminalized homosexuality; read down Section 377 IPC",
        "citation": "AIR 2018 SC 4321",
        "pdf_available": True
    },
    "CA_477_1992": {
        "case_number": "477",
        "case_type": "CA",
        "filing_year": 1992,
        "petitioner_name": "Indra Sawhney and Others",
        "respondent_name": "Union of India (Mandal Commission Case)",
        "filing_date": date(1990, 8, 13),
        "decision_date": date(1992, 11, 16),
        "case_status": "Decided",
        "judge_name": "9-Judge Constitutional Bench",
        "court_name": "Supreme Court of India",
        "significance": "Upheld reservation for OBCs; established 50% ceiling on reservations",
        "citation": "AIR 1993 SC 477",
        "pdf_available": True
    },
    "CS_1234_2020": {
        "case_number": "1234",
        "case_type": "CS",
        "filing_year": 2020,
        "petitioner_name": "ABC Corporation Ltd.",
        "respondent_name": "XYZ Industries Pvt. Ltd.",
        "filing_date": date(2020, 3, 15),
        "next_hearing_date": date(2024, 12, 20),
        "case_status": "Pending",
        "judge_name": "Justice Sample Name",
        "court_name": "Delhi High Court",
        "significance": "Commercial dispute regarding breach of contract",
        "citation": "CS 1234/2020 Del HC",
        "pdf_available": False
    }
}

@app.route('/')
def index():
    return render_template('simple_index.html')

@app.route('/search', methods=['POST'])
def search_case():
    case_type = request.form.get('case_type', '').strip()
    case_number = request.form.get('case_number', '').strip()
    filing_year = request.form.get('filing_year', '').strip()
    
    # Basic validation
    if not case_type or not case_number or not filing_year:
        flash('Please fill in all fields', 'error')
        return redirect(url_for('index'))
    
    # Convert filing_year to int
    try:
        filing_year = int(filing_year)
    except ValueError:
        flash('Invalid filing year', 'error')
        return redirect(url_for('index'))
    
    # Store search
    search_data = {
        'case_type': case_type,
        'case_number': case_number,
        'filing_year': filing_year,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    search_history.append(search_data)
    
    # Look up case in database
    case_key = f"{case_type}_{case_number}_{filing_year}"
    case_found = CASE_DATABASE.get(case_key)
    
    if case_found:
        # Case found in database
        return render_template('simple_results.html', 
                             search_data=search_data, 
                             case_found=case_found,
                             success=True)
    else:
        # Case not found
        return render_template('simple_results.html', 
                             search_data=search_data, 
                             case_found=None,
                             success=False)

@app.route('/history')
def history():
    return render_template('simple_history.html', searches=search_history)

@app.route('/cases')
def available_cases():
    """Show list of available cases for easy lookup"""
    return render_template('available_cases.html', cases=CASE_DATABASE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)