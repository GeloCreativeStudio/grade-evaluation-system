# Grade Evaluation System

A modern and user-friendly grade evaluation system built with Python and Tkinter, designed for educational institutions to manage student grades efficiently.

## Features

- **User Authentication**
  - Separate login systems for students and registrars
  - Secure password handling
  - User registration for both students and registrars

- **Grade Management**
  - Input and update student grades
  - Calculate GPA and academic standing
  - Track academic progress across semesters
  - View grade history and transcripts

- **User Interface**
  - Modern and intuitive GUI using ttk themed widgets
  - Responsive design with proper form validation
  - Clear navigation between different sections
  - Professional color scheme and styling

## System Requirements

- Python 3.8 or higher
- Windows/Linux/MacOS operating system
- Minimum 4GB RAM
- 100MB free disk space

## Installation Guide

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd GradeEvaluationSystem
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Linux/MacOS:
     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Initialize the Database**
   ```bash
   python -m src.database.init_database
   ```

## Running the Application

1. **Start the Application**
   ```bash
   python run.py
   ```

2. **First-time Setup**
   - For registrars: Create a new account using the registration form
   - For students: Register with your student details
   - All passwords must meet the minimum security requirements

## Project Structure

```
GradeEvaluationSystem/
├── data/                  # Database and data files
├── logs/                  # Application logs
├── src/                   # Source code
│   ├── database/         # Database operations
│   ├── ui/               # User interface components
│   ├── utils/            # Utility functions
│   └── main.py           # Application entry point
├── tests/                # Test files
├── requirements.txt      # Project dependencies
└── README.md            # Project documentation
```

## Testing

Run the test suite to verify system functionality:
```bash
python -m tests.test_system
```

## Troubleshooting

1. **Database Connection Issues**
   - Ensure the database file exists in the data directory
   - Check file permissions
   - Verify SQLite3 is properly installed

2. **GUI Display Problems**
   - Update tkinter and ttkthemes packages
   - Check system theme compatibility
   - Verify Python version compatibility

3. **Login Issues**
   - Clear browser cache and cookies
   - Reset password if necessary
   - Contact system administrator for account verification

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and queries:
- Create an issue in the repository
- Contact the system administrator
- Check the documentation for common issues

## Acknowledgments

- Built with Python and Tkinter
- Uses ttkthemes for modern styling
- SQLite3 for database management
