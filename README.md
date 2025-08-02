# Indian Court Case Lookup Portal

A professional web application for searching case information from Indian judicial databases. Built with Flask and featuring a court-appropriate UI design that reflects the seriousness and authority of legal tools.

## 🏛️ Features

### Professional Court-Themed Interface
- **Clean, authoritative design** with muted blue/gray/white color scheme
- **Typography**: Serif fonts (Georgia, Times New Roman) for formal text, sans-serif for inputs
- **Responsive layout** using Bootstrap 5
- **Legal iconography** with FontAwesome icons (gavel, file-pdf, etc.)
- **Court seal placeholder** and official branding

### Case Lookup Functionality
- **Comprehensive search form** with:
  - Case Type dropdown (CS, CRL, WP, LPA, etc.)
  - Case Number input with format validation
  - Filing Year selection (1950-2024)
- **Form validation** and user feedback
- **Professional loading states** and error handling

### Database Logging
- **SQLite database** for query logging and audit trails
- **Query history** tracking with timestamps
- **Raw response storage** for debugging and analysis
- **Status tracking** (pending, success, failed)

### Results Display
- **Card-based layout** for case information
- **Structured data presentation**:
  - Parties' names (Petitioner/Respondent)
  - Filing dates and hearing schedules
  - Case status and presiding judge
  - Court document links (PDF downloads)
- **Error handling** with actionable feedback

## 🛠️ Technology Stack

### Backend
- **Flask** - Python web framework
- **SQLAlchemy** - Database ORM
- **SQLite** - Database for query logging
- **Beautiful Soup** - Web scraping (prepared for future implementation)
- **Requests** - HTTP client for court website interaction

### Frontend
- **HTML5** with Jinja2 templates
- **Bootstrap 5** - Responsive UI framework
- **FontAwesome** - Professional iconography
- **Custom CSS** - Court-themed styling
- **Vanilla JavaScript** - Form validation and UX enhancements

## 📁 Project Structure

