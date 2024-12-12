# EECP Grade Evaluation System (GESYS)

<div align="center">

![EECP GESYS Front](images/EECP%20GESYS%20Front.jpg)

[![GitHub issues](https://img.shields.io/github/issues/GeloCreativeStudio/grade-evaluation-system)](https://github.com/GeloCreativeStudio/grade-evaluation-system/issues)
[![GitHub stars](https://img.shields.io/github/stars/GeloCreativeStudio/grade-evaluation-system)](https://github.com/GeloCreativeStudio/grade-evaluation-system/stargazers)
[![GitHub license](https://img.shields.io/github/license/GeloCreativeStudio/grade-evaluation-system)](https://github.com/GeloCreativeStudio/grade-evaluation-system/blob/main/LICENSE)

</div>

## 📋 Overview

EECP GESYS is a comprehensive grade evaluation system developed specifically for EMA EMITS College Philippines (EECP). This desktop application streamlines the process of managing and evaluating student grades with a modern, user-friendly interface.

## ✨ Features

### 🔐 User Authentication
- **Role-Based Access Control**
  - Separate portals for Students and Registrars
  - Default admin account for initial setup
  - Secure password encryption
  - Session management
- **User Registration**
  - Intuitive registration forms
  - Real-time input validation
  - Automatic data verification
  - Email domain verification (@eecp.edu.ph)

### 📊 Grade Management
- **Comprehensive Grade Tracking**
  - Semester-wise grade organization
  - Automatic GPA calculation
  - Academic standing evaluation
- **Grade History**
  - Complete academic record
  - Printable grade reports
  - Progress tracking
  - Export functionality

### 💻 User Interface
- **Modern Design**
  - EECP-branded theme
  - Responsive layout
  - Dark/light mode support
- **User Experience**
  - Intuitive navigation
  - Form validation
  - Error handling
  - Helpful tooltips
  - Input format guides

## 🔧 System Requirements

- **Operating System**
  - Windows 10/11 (64-bit)
- **Hardware**
  - 4GB RAM (minimum)
  - 100MB disk space
  - 1024x768 screen resolution
- **Software**
  - Python 3.8+
  - pip (Python package installer)

## 📥 Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/GeloCreativeStudio/grade-evaluation-system.git
   cd grade-evaluation-system
   ```

2. **Set Up Python Environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install Required Packages**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize Database**
   ```bash
   python -m src.database.init_database
   ```

## 🚀 Quick Start

1. **Launch Application**
   ```bash
   python run.py
   ```

2. **Default Credentials**

   **For Registrar (Admin):**
   ```
   Username: admin
   Password: admin123
   ```
   
   **For Student (Sample):**
   ```
   Student Number: student
   Password: student123
   ```

3. **First-Time Setup**

   **For New Registrars:**
   - Select "Registrar Login"
   - Click "Sign Up"
   - Required Information:
     - Registrar ID (e.g., REG001)
     - Full Name
     - Password (minimum 8 characters)
   
   **For New Students:**
   - Use main login screen
   - Click "Sign Up"
   - Required Information:
     - Student Number (e.g., 2024xxxxx)
     - Full Name
     - Mobile Number (e.g., 09xxxxxxxxx)
     - Email Address (@eecp.edu.ph)
     - Password (minimum 8 characters)

## 📁 Project Structure

```plaintext
grade-evaluation-system/
├── data/                  # Database storage
├── images/               # UI assets
├── logs/                 # Application logs
├── src/                  # Source code
│   ├── database/        # Database operations
│   ├── ui/              # User interface
│   ├── utils/           # Utilities
│   └── main.py          # Entry point
├── tests/               # Test suite
├── .gitignore          # Git ignore rules
├── requirements.txt     # Dependencies
└── README.md           # Documentation
```

## 🧪 Testing

```bash
python -m tests.test_system
```

**Test Coverage:**
- ✓ Database CRUD operations
- ✓ User authentication
- ✓ Grade calculations
- ✓ Form validation
- ✓ Data integrity checks

## ❗ Troubleshooting

### Database Issues
```bash
# Reinitialize database
python -m src.database.init_database

# Check database permissions
icacls data/eecp_gesys.db
```

### Display Problems
```bash
# Install/upgrade UI dependencies
pip install --upgrade ttkthemes pillow
```

### Authentication Issues
- Verify correct portal (Student/Registrar)
- Check input format (email, mobile)
- Reset application cache

## 👨‍💻 Developer

<div align="center">
<img src="https://avatars.githubusercontent.com/angelo-manalo" alt="Angelo Manalo" width="150" style="border-radius: 50%;"/>

### Angelo Manalo

[![GitHub](https://img.shields.io/badge/GitHub-angelo--manalo-181717?style=for-the-badge&logo=github)](https://github.com/angelo-manalo)
[![Email](https://img.shields.io/badge/Email-202410769%40fit.edu.ph-D14836?style=for-the-badge&logo=gmail)](mailto:202410769@fit.edu.ph)

**Location:** Manila, Philippines  
**Contact:** +63 992 552 8110  
**Studio:** [GeloCreativeStudio](https://github.com/GeloCreativeStudio)
</div>

## 🤝 Contributing

1. Fork the Project
2. Create your Feature Branch
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. Commit your Changes
   ```bash
   git commit -m 'Add: Amazing Feature'
   ```
4. Push to the Branch
   ```bash
   git push origin feature/AmazingFeature
   ```
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/GeloCreativeStudio/grade-evaluation-system/issues)
- **Email:** 202410769@fit.edu.ph
- **Website:** [GeloCreativeStudio](https://github.com/GeloCreativeStudio)

## 🙏 Acknowledgments

- **EECP** - For project support and guidance
- **GeloCreativeStudio** - For development and maintenance
- **Open Source Community** - For tools and libraries:
  - Python & Tkinter
  - ttkthemes
  - SQLite3

---
<div align="center">
Made with ❤️ by GeloCreativeStudio

© 2024 EECP GESYS. All Rights Reserved.

Developed by [Angelo Manalo](https://github.com/angelo-manalo)
</div>
