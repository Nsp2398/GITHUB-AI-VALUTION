# 🚀 ValuAI Setup Guide - Complete Installation Instructions

## 📋 Prerequisites

Before starting, ensure you have the following installed:

### Required Software:
- **Node.js** (v16 or higher) - [Download from nodejs.org](https://nodejs.org/)
- **Python** (v3.8 or higher) - [Download from python.org](https://python.org/)
- **Git** - [Download from git-scm.com](https://git-scm.com/)
- **VS Code** (recommended) - [Download from code.visualstudio.com](https://code.visualstudio.com/)

### Verify Installation:
```bash
node --version    # Should show v16.x.x or higher
npm --version     # Should show 8.x.x or higher  
python --version  # Should show 3.8.x or higher
git --version     # Should show git version
```

---

## 🔧 Step-by-Step Setup

### Step 1: Clone the Repository
```bash
git clone https://github.com/Nsp2398/GITHUB-AI-VALUTION.git
cd GITHUB-AI-VALUTION
```

### Step 2: Backend Setup (Python/Flask)

#### 2.1 Create Python Virtual Environment
```bash
# Windows (PowerShell/CMD)
python -m venv venv
venv\Scripts\activate

# Windows (Git Bash)
python -m venv venv
source venv/Scripts/activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 2.2 Install Python Dependencies
```bash
# Make sure virtual environment is activated
pip install --upgrade pip
pip install flask flask-cors python-docx reportlab requests
```

#### 2.3 Test Backend
```bash
# From project root directory
python main_server.py
```
You should see:
```
🚀 Starting ValuAI Business Valuation Tool...
📊 Initializing database...
✅ Server ready!
🔧 API Base URL: http://127.0.0.1:5002
```

### Step 3: Frontend Setup (React/Node.js)

#### 3.1 Navigate to Client Directory
```bash
cd client
```

#### 3.2 Install Node.js Dependencies
```bash
npm install
```

If you encounter issues, try:
```bash
npm install --legacy-peer-deps
```

#### 3.3 Start Frontend Development Server
```bash
npm run dev
```

You should see:
```
VITE v4.5.14  ready in 661 ms
➜  Local:   http://127.0.0.1:5173/
```

---

## 🌐 Accessing the Application

### URLs:
- **Frontend**: http://127.0.0.1:5173/
- **Backend API**: http://127.0.0.1:5002/api/health

### Verification Steps:
1. Open http://127.0.0.1:5173/ in your browser
2. You should see the ValuAI interface
3. Test backend by visiting http://127.0.0.1:5002/api/health (should show "ok")

---

## 🔧 Common Issues & Solutions

### Issue 1: "Site can't be reached" or "Connection refused"

**Solution A - Check if servers are running:**
```bash
# Check if ports are in use
netstat -an | findstr ":5173"  # Frontend
netstat -an | findstr ":5002"  # Backend
```

**Solution B - Kill existing processes:**
```bash
# Windows
taskkill /f /im node.exe
taskkill /f /im python.exe

# macOS/Linux  
killall node
killall python
```

**Solution C - Restart servers:**
```bash
# Terminal 1: Start Backend
cd GITHUB-AI-VALUTION
venv\Scripts\activate    # Windows
python main_server.py

# Terminal 2: Start Frontend  
cd GITHUB-AI-VALUTION/client
npm run dev
```

### Issue 2: "Module not found" errors

**Backend Modules:**
```bash
# Activate virtual environment first
venv\Scripts\activate    # Windows
source venv/bin/activate # macOS/Linux

# Install missing modules
pip install flask flask-cors python-docx reportlab requests sqlite3
```

**Frontend Modules:**
```bash
cd client
rm -rf node_modules package-lock.json
npm install
```

### Issue 3: Port conflicts

**Change Frontend Port:**
Edit `client/vite.config.ts`:
```typescript
server: {
  port: 5174,  // Change to different port
  // ... rest of config
}
```

**Change Backend Port:**
Edit `main_server.py` (line ~1212):
```python
app.run(host='127.0.0.1', port=5003, debug=True)  # Change port
```

### Issue 4: Permission errors

**Windows:**
```bash
# Run as Administrator or use:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**macOS/Linux:**
```bash
# Use sudo for global installs
sudo npm install -g npm@latest
```

### Issue 5: Python path issues

**Windows:**
```bash
# Use full path to Python
C:\Python39\python.exe -m venv venv
```

**Add to PATH or use:**
```bash
py -m venv venv  # Windows Python Launcher
```

---

## 📁 Project Structure

```
GITHUB-AI-VALUTION/
├── client/                 # React frontend
│   ├── src/
│   ├── package.json
│   └── vite.config.ts
├── server/                 # Flask backend (alternative)
├── main_server.py         # Main backend server
├── requirements.txt       # Python dependencies
├── venv/                  # Python virtual environment
└── README.md
```

---

## 🔍 Troubleshooting Checklist

Before asking for help, please check:

- [ ] Node.js and Python are installed and in PATH
- [ ] Virtual environment is activated (you should see `(venv)` in terminal)
- [ ] All dependencies are installed (`pip install` and `npm install` completed)
- [ ] No other applications are using ports 5173 and 5002
- [ ] Firewall/antivirus isn't blocking the connections
- [ ] You're accessing the correct URLs (127.0.0.1, not localhost)

### Quick Test Commands:
```bash
# Test Python
python --version
python -c "import flask; print('Flask OK')"

# Test Node.js
node --version
npm --version

# Test network connectivity
curl http://127.0.0.1:5002/api/health
```

---

## 🆘 Getting Help

If you're still having issues:

1. **Check the terminal outputs** for specific error messages
2. **Verify prerequisites** are correctly installed
3. **Try the manual setup** commands step by step
4. **Check Windows/macOS specific instructions** above
5. **Look for firewall/antivirus blocking** the ports

### Common Error Messages:

| Error | Solution |
|-------|----------|
| `'python' is not recognized` | Install Python and add to PATH |
| `'npm' is not recognized` | Install Node.js and add to PATH |
| `Port 5173 is already in use` | Kill existing process or change port |
| `Module not found` | Install dependencies in virtual environment |
| `Connection refused` | Check if backend server is running |

---

## 🎯 Quick Start (TL;DR)

For experienced developers:

```bash
# 1. Clone and setup
git clone https://github.com/Nsp2398/GITHUB-AI-VALUTION.git
cd GITHUB-AI-VALUTION

# 2. Backend
python -m venv venv
venv\Scripts\activate    # Windows
pip install flask flask-cors python-docx reportlab requests
python main_server.py    # Keep running

# 3. Frontend (new terminal)
cd client
npm install
npm run dev             # Keep running

# 4. Open http://127.0.0.1:5173/
```

---

## 🔄 Development Workflow

### Daily development:
1. **Start Backend**: `python main_server.py`
2. **Start Frontend**: `npm run dev` (in client folder)
3. **Access**: http://127.0.0.1:5173/

### Making changes:
- Frontend changes auto-reload
- Backend changes require restart (Ctrl+C, then `python main_server.py`)

### Before committing:
- Test both frontend and backend
- Check no console errors
- Verify all features work

---

**🎉 You're all set! The ValuAI Business Valuation Tool should now be running successfully.**
