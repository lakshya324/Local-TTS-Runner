# Color codes for terminal output
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Print header
echo -e "${GREEN}${BOLD}🎙️ Local TTS Runner${NC}"
echo -e "${BLUE}Running the application...${NC}"

# Check if virtual environment exists and activate it
if [ -d ".venv" ]; then
    echo -e "${BLUE}Activating virtual environment...${NC}"
    source .venv/bin/activate
fi

# Run setup script to check dependencies
echo -e "${BLUE}Checking dependencies...${NC}"
python setup.py

# Run the application
echo -e "${GREEN}Starting application...${NC}"
python app.py
