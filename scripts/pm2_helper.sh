#!/bin/bash
################################################################################
# PM2 Helper Script for Twitter Bot
# 
# Usage:
#   ./scripts/pm2_helper.sh start        # Start all services
#   ./scripts/pm2_helper.sh stop         # Stop all services
#   ./scripts/pm2_helper.sh restart      # Restart all services
#   ./scripts/pm2_helper.sh status       # Show status
#   ./scripts/pm2_helper.sh logs         # View logs
#   ./scripts/pm2_helper.sh setup        # First-time setup
################################################################################

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo -e "${BLUE}╔════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║   Twitter Bot - PM2 Management Helper     ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════╝${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if PM2 is installed
check_pm2() {
    if ! command -v pm2 &> /dev/null; then
        print_error "PM2 not found! Installing..."
        npm install -g pm2
        if [ $? -eq 0 ]; then
            print_success "PM2 installed successfully!"
        else
            print_error "Failed to install PM2. Please install manually: npm install -g pm2"
            exit 1
        fi
    fi
}

# Check Python dependencies
check_dependencies() {
    print_info "Checking Python dependencies..."
    
    if ! command -v python3 &> /dev/null; then
        print_error "Python3 not found! Please install Python 3.x"
        exit 1
    fi
    
    # Check if requirements are installed
    python3 -c "import twikit" 2>/dev/null
    if [ $? -ne 0 ]; then
        print_warning "Dependencies not installed. Installing..."
        pip3 install -r requirements.txt
    fi
    
    print_success "Dependencies OK"
}

# Create directories
setup_directories() {
    print_info "Creating log directories..."
    
    mkdir -p data/logs
    mkdir -p accounts/account1_GrnStore4347/data/logs
    mkdir -p accounts/account2_KorteksL43042/data/logs
    
    print_success "Directories created"
}

# Setup (first-time)
setup() {
    print_header
    print_info "Starting first-time setup..."
    echo ""
    
    check_pm2
    check_dependencies
    setup_directories
    
    echo ""
    print_success "Setup completed!"
    echo ""
    print_info "Next steps:"
    echo "  1. Configure your settings: config/settings.yaml"
    echo "  2. Add your cookies: accounts/*/cookies.json"
    echo "  3. Start services: ./scripts/pm2_helper.sh start"
    echo ""
}

# Start services
start() {
    print_header
    print_info "Starting all services..."
    echo ""
    
    check_pm2
    
    pm2 start ecosystem.config.js
    
    if [ $? -eq 0 ]; then
        echo ""
        print_success "All services started!"
        echo ""
        print_info "Access dashboards:"
        echo "  - Dashboard V1: http://localhost:5000"
        echo "  - Dashboard V2: http://localhost:5001"
        echo ""
        pm2 status
    else
        print_error "Failed to start services. Check logs: pm2 logs"
        exit 1
    fi
}

# Stop services
stop() {
    print_header
    print_info "Stopping all services..."
    echo ""
    
    pm2 stop all
    
    if [ $? -eq 0 ]; then
        print_success "All services stopped!"
        pm2 status
    else
        print_error "Failed to stop services"
        exit 1
    fi
}

# Restart services
restart() {
    print_header
    print_info "Restarting all services..."
    echo ""
    
    pm2 restart all
    
    if [ $? -eq 0 ]; then
        print_success "All services restarted!"
        pm2 status
    else
        print_error "Failed to restart services"
        exit 1
    fi
}

# Show status
status() {
    print_header
    pm2 status
    echo ""
    pm2 monit
}

# View logs
logs() {
    print_header
    print_info "Viewing logs (Ctrl+C to exit)..."
    echo ""
    pm2 logs
}

# Monitor
monitor() {
    print_header
    print_info "Monitoring resources (Ctrl+C to exit)..."
    echo ""
    pm2 monit
}

# Delete all processes
delete() {
    print_header
    print_warning "This will delete all PM2 processes!"
    read -p "Are you sure? (yes/no): " confirm
    
    if [ "$confirm" = "yes" ]; then
        pm2 delete all
        print_success "All processes deleted"
    else
        print_info "Cancelled"
    fi
}

# Save current PM2 setup
save() {
    print_header
    print_info "Saving PM2 process list..."
    
    pm2 save
    
    if [ $? -eq 0 ]; then
        print_success "PM2 process list saved!"
        print_info "Run 'pm2 startup' to auto-start on boot"
    fi
}

# Setup auto-start on boot
startup() {
    print_header
    print_info "Setting up auto-start on boot..."
    echo ""
    
    pm2 startup
    
    echo ""
    print_warning "Run the command shown above (the 'sudo env PATH=...' line)"
    print_info "After running it, execute: ./scripts/pm2_helper.sh save"
}

# Update bot code
update() {
    print_header
    print_info "Updating bot code..."
    echo ""
    
    # Pull latest code
    if [ -d .git ]; then
        print_info "Pulling latest code from git..."
        git pull origin main
    else
        print_warning "Not a git repository. Skipping code update."
    fi
    
    # Update dependencies
    print_info "Updating dependencies..."
    pip3 install -r requirements.txt --upgrade
    
    # Restart services
    print_info "Restarting services..."
    pm2 restart all
    
    echo ""
    print_success "Update completed!"
}

# Show help
show_help() {
    print_header
    echo "Usage: ./scripts/pm2_helper.sh [command]"
    echo ""
    echo "Commands:"
    echo "  setup       - First-time setup (install PM2, create directories)"
    echo "  start       - Start all services"
    echo "  stop        - Stop all services"
    echo "  restart     - Restart all services"
    echo "  status      - Show service status"
    echo "  logs        - View logs (real-time)"
    echo "  monitor     - Monitor resources"
    echo "  save        - Save current PM2 setup"
    echo "  startup     - Setup auto-start on boot"
    echo "  delete      - Delete all PM2 processes"
    echo "  update      - Update code and restart"
    echo "  help        - Show this help message"
    echo ""
    echo "Examples:"
    echo "  ./scripts/pm2_helper.sh start"
    echo "  ./scripts/pm2_helper.sh logs"
    echo "  ./scripts/pm2_helper.sh status"
    echo ""
}

# Main
case "$1" in
    setup)
        setup
        ;;
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    status)
        status
        ;;
    logs)
        logs
        ;;
    monitor)
        monitor
        ;;
    save)
        save
        ;;
    startup)
        startup
        ;;
    delete)
        delete
        ;;
    update)
        update
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        print_error "Unknown command: $1"
        echo ""
        show_help
        exit 1
        ;;
esac
