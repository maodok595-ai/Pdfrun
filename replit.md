# PDF Generator Application

## Overview

A Flask-based web application that converts user-inputted text into professionally formatted PDF documents. The application features a clean web interface where users can paste or type text, and it generates a downloadable PDF with proper formatting, paragraph preservation, and list handling. Built with Python Flask for the backend and uses ReportLab for PDF generation.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Template Engine**: Jinja2 templates with Flask
- **UI Design**: Single-page application with gradient background and modern CSS styling
- **Form Handling**: Simple HTML form with textarea for text input
- **Responsive Design**: Mobile-friendly layout with viewport meta tag

### Backend Architecture
- **Web Framework**: Flask with minimal configuration
- **PDF Generation**: ReportLab library for creating formatted PDF documents
- **Text Processing**: Custom text parser that handles paragraphs, lists, and HTML escaping
- **File Handling**: In-memory PDF generation and download response

### Core Components
1. **Main Application** (`app.py`):
   - Flask route handlers for home page and PDF generation
   - Text preprocessing logic for better PDF formatting
   - PDF document creation with paragraph and list detection

2. **Template System** (`templates/index.html`):
   - Clean, modern web interface
   - Gradient background with card-style container
   - Form for text input with styling

### Text Processing Logic
- **HTML Escaping**: Prevents parsing errors from special characters
- **Paragraph Detection**: Splits text on double line breaks
- **List Recognition**: Detects bullet points and numbered lists
- **Smart Line Joining**: Preserves list formatting while joining regular paragraphs

### Security Considerations
- **Secret Key**: Uses environment variable with fallback for development
- **Input Sanitization**: HTML escaping for user input
- **File Security**: In-memory PDF generation without file system storage

## External Dependencies

### Python Libraries
- **Flask**: Web framework for routing and template rendering
- **ReportLab**: PDF generation and formatting library
- **Standard Library**: `io`, `os`, `html`, `re` for core functionality

### Frontend Dependencies
- **CSS**: Custom styling with modern design patterns
- **HTML5**: Semantic markup with proper viewport configuration

### Environment Variables
- **SECRET_KEY**: Flask session security (optional, has development fallback)

### Runtime Requirements
- **Python 3.x**: Required for Flask and ReportLab compatibility
- **Web Browser**: For accessing the application interface