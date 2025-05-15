#!/bin/bash

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Setting up pre-commit hooks for Pack Me Up backend code...${NC}"
echo -e "${BLUE}(These hooks will only check files in the backend directory)${NC}"

# Check if pre-commit is installed
if ! command -v pre-commit &> /dev/null; then
    echo -e "${BLUE}Installing pre-commit...${NC}"
    uv add --dev pre-commit
fi

# Install pre-commit hooks
echo -e "${BLUE}Installing pre-commit hooks...${NC}"
pre-commit install

# Run pre-commit on all files
echo -e "${BLUE}Running pre-commit on all backend files...${NC}"
pre-commit run --all-files

echo -e "${GREEN}Pre-commit setup complete!${NC}"
echo -e "${BLUE}Hooks will now run automatically on git commit for backend files only.${NC}" 