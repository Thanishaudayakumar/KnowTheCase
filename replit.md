# Overview

The Indian Court Case Lookup Portal is a professional web application designed for searching case information from Indian judicial databases. The application provides a formal, court-appropriate interface that reflects the authority and seriousness of legal proceedings. It features comprehensive case lookup functionality with database logging for audit trails and query tracking.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture

The frontend uses a traditional server-side rendered architecture with Flask templates and Bootstrap 5 for responsive design. The UI follows a professional court theme with:

- **Template System**: Jinja2 templates with a base template providing consistent navigation and layout
- **Styling Framework**: Bootstrap 5 for responsive grid and components, supplemented with custom CSS
- **Design Language**: Court-appropriate color scheme (muted blue/gray/white) with serif fonts for formal elements and sans-serif for inputs
- **Client-side Enhancement**: Progressive enhancement with JavaScript for form validation, loading states, and user experience improvements

## Backend Architecture

The backend follows a simple Flask application pattern with clear separation of concerns:

- **Application Factory**: Flask app initialization with SQLAlchemy integration and proper configuration management
- **Routing Layer**: Centralized route handlers in `routes.py` for case search and result display
- **Data Processing**: Dedicated scraper module for interfacing with court websites (currently demonstration mode)
- **Error Handling**: Comprehensive form validation and user feedback mechanisms

## Data Storage Solutions

The application uses SQLite as the primary database with SQLAlchemy ORM:

- **Query Logging**: `CaseQuery` model tracks all search attempts with metadata including timestamps, status, and error messages
- **Result Storage**: `CaseResult` model stores parsed case information linked to queries via foreign key relationships
- **Audit Trail**: Complete logging of user interactions and system responses for debugging and compliance

## Authentication and Authorization

Currently, the application does not implement user authentication, operating as a public search interface. The architecture is prepared for future authentication implementation through Flask's session management.

## Web Scraping Architecture

The scraping functionality is designed with a modular approach:

- **Abstracted Interface**: The scraper module provides a consistent interface regardless of the target court website
- **Error Handling**: Comprehensive error catching and logging for failed scraping attempts
- **Demonstration Mode**: Currently returns structured error responses to showcase the interface without actual scraping due to CAPTCHA and authentication complexities

# External Dependencies

## Core Framework Dependencies

- **Flask**: Python web framework for application structure and routing
- **SQLAlchemy**: ORM for database operations and model definitions
- **Bootstrap 5**: Frontend CSS framework for responsive design and components
- **FontAwesome**: Icon library for professional legal iconography

## Data Processing Dependencies

- **Beautiful Soup**: HTML parsing library prepared for web scraping implementation
- **Requests**: HTTP client library for making requests to court websites

## Development and Deployment

- **SQLite**: Embedded database for development and small-scale deployment
- **Werkzeug ProxyFix**: Middleware for proper request handling behind proxies

## Target Court Websites

The application is designed to interface with Indian court websites including:

- Delhi High Court (delhihighcourt.nic.in)
- District eCourts (districts.ecourts.gov.in)

Note: Actual scraping implementation requires handling complex authentication, CAPTCHA systems, and legal compliance considerations.