"""
Logger configuration for Local-TTS-Runner.
Provides colored logging output for better readability.
"""

import os
import logging
import colorlog
from dotenv import load_dotenv

# Load environment variables if not already loaded
load_dotenv()

# Get log level from environment or default to INFO
LOG_LEVEL_NAME = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_LEVEL = getattr(logging, LOG_LEVEL_NAME, logging.INFO)

# Set up a custom logger with colored output
logger = logging.getLogger("local-tts")
logger.setLevel(LOG_LEVEL)

# Remove existing handlers to prevent duplicate logs
for handler in logger.handlers[:]:
    logger.removeHandler(handler)

# Create console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(LOG_LEVEL)

# Create a colorlog formatter
formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(asctime)s [%(levelname)8s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }
)

# Add formatter to console handler
console_handler.setFormatter(formatter)

# Add console handler to logger
logger.addHandler(console_handler)

# Create file handler if LOG_FILE is specified in environment
LOG_FILE = os.getenv("LOG_FILE", "")
if LOG_FILE:
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setLevel(LOG_LEVEL)
    file_formatter = logging.Formatter(
        "%(asctime)s [%(levelname)8s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    logger.info(f"Logging to file: {LOG_FILE}")

# Functions to log with context information
def debug(message, context=None):
    """Log debug message with optional context"""
    if context:
        logger.debug(f"{message} | {format_context(context)}")
    else:
        logger.debug(message)

def info(message, context=None):
    """Log info message with optional context"""
    if context:
        logger.info(f"{message} | {format_context(context)}")
    else:
        logger.info(message)

def warning(message, context=None):
    """Log warning message with optional context"""
    if context:
        logger.warning(f"{message} | {format_context(context)}")
    else:
        logger.warning(message)

def error(message, context=None):
    """Log error message with optional context"""
    if context:
        logger.error(f"{message} | {format_context(context)}")
    else:
        logger.error(message)

def critical(message, context=None):
    """Log critical message with optional context"""
    if context:
        logger.critical(f"{message} | {format_context(context)}")
    else:
        logger.critical(message)

def format_context(context):
    """Format context dictionary as string"""
    if not context:
        return ""
    try:
        return ", ".join([f"{k}={v}" for k, v in context.items()])
    except:
        return str(context)
