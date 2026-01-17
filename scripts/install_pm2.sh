#!/bin/bash
################################################################################
# PM2 Installation Script for Twitter Bot
# This script will install PM2 and all required dependencies
#
# Usage:
#   bash scripts/install_pm2.sh
################################################################################

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_header() {
    echo -e "${BLUE}╔════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║     PM2 Installation for Twitter Bot      ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════╝${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
    print_warning "Please do not run as root"
    exit 1
fi

print_header

# 1. Check Node.js and npm
print_info "Step 1/5: Checking Node.js and npm..."
if ! command -v node &> /dev/null; then
    print_error "Node.js not found!"
    print_info "Installing Node.js..."
    
    # Detect OS
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Ubuntu/Debian
        if command -v apt-get &> /dev/null; then
            curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
            sudo apt-get install -y nodejs
        # CentOS/RHEL
        elif command -v yum &> /dev/null; then
            curl -fsSL https://rpm.nodesource.com/setup_18.x | sudo bash -
            sudo yum install -y nodejs
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            brew install node
        else
            print_error "Homebrew not found. Please install Node.js manually from https://nodejs.org"
            exit 1
        fi
    fi
else
    print_success "Node.js found: $(node --version)"
fi

if ! command -v npm &> /dev/null; then
    print_error "npm not found! Please install Node.js from https://nodejs.org"
    exit 1
else
    print_success "npm found: $(npm --version)"
fi

# 2. Install PM2
print_info "Step 2/5: Installing PM2..."
if command -v pm2 &> /dev/null; then
    print_warning "PM2 already installed: $(pm2 --version)"
    read -p "Reinstall/update PM2? (y/n): " reinstall
    if [ "$reinstall" = "y" ]; then
        npm install -g pm2@latest
        print_success "PM2 updated!"
    fi
else
    npm install -g pm2
    if [ $? -eq 0 ]; then
        print_success "PM2 installed: $(pm2 --version)"
    else
        print_error "Failed to install PM2"
        exit 1
    fi
fi

# 3. Install Python dependencies
print_info "Step 3/5: Checking Python and dependencies..."
if ! command -v python3 &> /dev/null; then
    print_error "Python3 not found! Please install Python 3.x"
    exit 1
else
    print_success "Python found: $(python3 --version)"
fi

if [ -f "requirements.txt" ]; then
    print_info "Installing Python dependencies..."
    pip3 install -r requirements.txt
    if [ $? -eq 0 ]; then
        print_success "Python dependencies installed!"
    else
        print_warning "Some dependencies failed to install. Check manually."
    fi
else
    print_warning "requirements.txt not found"
fi

# 4. Create necessary directories
print_info "Step 4/5: Creating directories..."
mkdir -p data/logs
mkdir -p accounts/account1_GrnStore4347/data/logs
mkdir -p accounts/account2_KorteksL43042/data/logs
mkdir -p scripts
print_success "Directories created!"

# 5. Make helper scripts executable
print_info "Step 5/5: Setting up helper scripts..."
if [ -f "scripts/pm2_helper.sh" ]; then
    chmod +x scripts/pm2_helper.sh
    print_success "Helper script ready!"
fi

# Install PM2 log rotation
print_info "Installing PM2 log rotation..."
pm2 install pm2-logrotate
pm2 set pm2-logrotate:max_size 10M
pm2 set pm2-logrotate:retain 7
pm2 set pm2-logrotate:compress true
print_success "Log rotation configured!"

echo ""
print_success "Installation completed successfully!"
echo ""
print_info "Next steps:"
echo "  1. Configure your bot: config/settings.yaml"
echo "  2. Add Twitter cookies: accounts/*/cookies.json"
echo "  3. Start services: ./scripts/pm2_helper.sh start"
echo "  4. View status: ./scripts/pm2_helper.sh status"
echo "  5. View logs: ./scripts/pm2_helper.sh logs"
echo ""
print_info "For auto-start on boot:"
echo "  ./scripts/pm2_helper.sh startup"
echo "  # Then run the displayed command"
echo "  ./scripts/pm2_helper.sh save"
echo ""
print_success "Happy tweeting! 🚀"
echo ""
