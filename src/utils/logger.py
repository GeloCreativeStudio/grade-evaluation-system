"""
Logging configuration for the Grade Evaluation System.
"""

import logging
import os
from datetime import datetime

def setup_logger():
    """Configure and return the application logger."""
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Configure logging
    logger = logging.getLogger('GradeEvaluationSystem')
    logger.setLevel(logging.DEBUG)

    # Create handlers
    file_handler = logging.FileHandler(
        f'logs/app_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
    )
    console_handler = logging.StreamHandler()

    # Create formatters and add it to handlers
    log_format = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(module)s: %(message)s'
    )
    file_handler.setFormatter(log_format)
    console_handler.setFormatter(log_format)

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# Create and export logger instance
logger = setup_logger()
