"""
Application configuration and settings
"""

# Development settings
DEV_MODE = True  # TODO: Move to environment variable

# CORS settings
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:4321",  # Astro's default port
    "http://127.0.0.1:4321",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:4322",
    "http://127.0.0.1:4310",
] 