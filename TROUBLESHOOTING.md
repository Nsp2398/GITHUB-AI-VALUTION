# 🚨 "This site can't be reached" - Quick Fix Guide

If you're seeing **"This site can't be reached"** when trying to access http://127.0.0.1:5173/, follow these steps:

## 🔧 Quick Fix (5 minutes)

### Step 1: Run the Setup Script
```bash
# Windows: Double-click this file in the project folder
setup_for_friends.bat
```

### Step 2: Wait for Setup
- The script will install everything automatically
- Wait for both server windows to open
- **Don't close the server windows!**

### Step 3: Access the App
- The browser should open automatically
- If not, manually go to: http://127.0.0.1:5173/
- **If it still doesn't work, wait 30 seconds and refresh**

---

## 🐛 Still Not Working?

### Check These Common Issues:

#### ✅ Are the servers running?
Look for these two windows:
- **"ValuAI Backend"** - Should show Python server messages
- **"ValuAI Frontend"** - Should show Vite/React messages

#### ✅ Check the URLs:
- ❌ Don't use: `localhost:5173`
- ✅ Use: `127.0.0.1:5173`

#### ✅ Wait longer:
- First startup can take 1-2 minutes
- Try refreshing the page after waiting

#### ✅ Check your firewall:
- Windows might be blocking the connections
- Allow Node.js and Python through Windows Firewall

---

## 🔧 Manual Setup (if script fails)

### Prerequisites:
1. **Install Node.js**: https://nodejs.org (v16 or higher)
2. **Install Python**: https://python.org (v3.8 or higher)

### Commands:
```bash
# 1. Clone the project (if not done already)
git clone https://github.com/Nsp2398/GITHUB-AI-VALUTION.git
cd GITHUB-AI-VALUTION

# 2. Setup Python backend
python -m venv venv
venv\Scripts\activate    # Windows
pip install flask flask-cors python-docx reportlab requests

# 3. Setup React frontend
cd client
npm install

# 4. Start backend (Terminal 1)
cd ../
python main_server.py

# 5. Start frontend (Terminal 2)
cd client
npm run dev
```

### Expected Output:
**Backend should show:**
```
🚀 Starting ValuAI Business Valuation Tool...
✅ Server ready!
🔧 API Base URL: http://127.0.0.1:5002
* Running on http://127.0.0.1:5002
```

**Frontend should show:**
```
VITE v4.5.14  ready in 661 ms
➜  Local:   http://127.0.0.1:5173/
```

---

## 🆘 Still Having Issues?

### Common Error Messages:

| Error | Solution |
|-------|----------|
| `'python' is not recognized` | Install Python and restart VS Code |
| `'npm' is not recognized` | Install Node.js and restart VS Code |
| `Port 5173 is already in use` | Close other applications using the port |
| `ECONNREFUSED` | Backend server isn't running |
| `Module not found` | Run `pip install` in activated virtual environment |

### Debug Steps:
1. **Check if Python works**: Open terminal, type `python --version`
2. **Check if Node works**: Open terminal, type `node --version`
3. **Check if ports are free**: Open terminal, type `netstat -an | findstr "5173"`
4. **Restart VS Code**: Close VS Code completely and reopen
5. **Check antivirus**: Temporarily disable antivirus and try again

### Get Help:
- Read the full guide: `SETUP_GUIDE.md`
- Check project issues on GitHub
- Make sure you followed all steps in order

---

## ✅ Success Checklist

When everything is working, you should see:
- [ ] Two command windows running (Backend + Frontend)
- [ ] Browser opens to http://127.0.0.1:5173/
- [ ] ValuAI interface loads (not an error page)
- [ ] You can navigate the application

**🎉 Once you see the ValuAI interface, you're all set!**
