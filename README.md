# Autism Screening Quiz Web Application

## Overview
This is a web-based screening tool designed to help identify potential autism spectrum traits in children. The application provides a simple, interactive quiz interface for parents or guardians to complete, with results that can be discussed with healthcare professionals.

## Disclaimer
This application is for screening purposes only and is not a diagnostic tool. Results should always be discussed with qualified healthcare professionals for proper evaluation and diagnosis.

## Features
- Interactive 10-question autism screening quiz
- Smooth, animated UI with progress tracking
- Results categorization (low, moderate, or high likelihood of autism spectrum traits)
- Data storage of quiz responses in SQLite database
- Age verification to ensure users are parents/guardians (30+ years old)
- Mobile-responsive design

## Technical Stack
- **Backend**: Python with Flask framework
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript
- **Template Engine**: Jinja2 (Flask's default template engine)

## Installation

### Prerequisites
- Python 3.6 or higher
- pip (Python package installer)

### Setup Steps
1. Clone this repository or download the source code
2. Navigate to the project directory
3. Install the required dependencies:
   ```
   pip install flask
   ```
4. Run the application:
   ```
   python First.py
   ```
5. Open your web browser and navigate to `http://127.0.0.1:5000/`

## Application Structure
- `First.py` - Main application file containing Flask routes and database initialization
- Templates:
  - `index.html` - Welcome/landing page
  - `start.html` - Parent information collection page
  - `quiz.html` - The actual quiz with questions
  - `result.html` - Results display page

## Quiz Flow
1. User visits the landing page with information about the screening tool
2. User enters their name and age (must be at least 30 years old)
3. User completes the 10-question quiz, answering each question on a scale:
   - Never (0 points)
   - Sometimes (1 point)
   - Often (2 points)
   - Always (3 points)
4. Results are calculated and presented to the user
5. Results are stored in the database for potential future reference

## Scoring System
- Maximum possible score: 30 points
- Results interpretation:
  - 0-10 points: Low likelihood of autism spectrum traits
  - 11-20 points: Moderate likelihood of autism spectrum traits
  - 21-30 points: High likelihood of autism spectrum traits

## Database Schema
The application uses a SQLite database (`autism_quiz.db`) with the following schema:
```
CREATE TABLE responses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    total_score INTEGER NOT NULL,
    result TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
```

## Customization
To modify the quiz questions, edit the `questions` list in `First.py`. The scoring system can also be adjusted by modifying the condition statements in the `result()` function.

## Future Enhancements
- User accounts and authentication
- Multiple language support
- Additional assessment tools
- Detailed reporting with specific recommendations
- Export results functionality (PDF, email)


## Contact
fotedarnamith@gmail.com
