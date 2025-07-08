#!/bin/bash

# Operating Agreement Builder - Startup Script

echo "Starting Operating Agreement Builder..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "Node.js is not installed. Please install Node.js 14 or higher."
    exit 1
fi

# Install backend dependencies if needed
if [ ! -d "backend/venv" ]; then
    echo "Creating Python virtual environment..."
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    cd ..
else
    echo "Activating Python virtual environment..."
    source backend/venv/bin/activate
fi

# Install frontend dependencies if needed
if [ ! -d "frontend/node_modules" ]; then
    echo "Installing frontend dependencies..."
    cd frontend
    npm install
    cd ..
fi

# Start backend in background
echo "Starting backend server..."
cd backend
source venv/bin/activate
python app.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start
sleep 3

# Start frontend
echo "Starting frontend application..."
cd frontend
npm start &
FRONTEND_PID=$!

echo ""
echo "============================================"
echo "Operating Agreement Builder is running!"
echo "Frontend: http://localhost:3000"
echo "Backend API: http://localhost:5001"
echo "Press Ctrl+C to stop both servers"
echo "============================================"

# Function to cleanup on exit
cleanup() {
    echo "Stopping servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit
}

# Set up cleanup on script exit
trap cleanup EXIT

# Wait for both processes
wait