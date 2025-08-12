@echo off
REM Install Real-time and Custom Reporting Dependencies

echo Installing Backend Dependencies...
cd server
pip install flask-socketio==5.3.6 python-socketio==5.8.0 matplotlib==3.7.2 seaborn==0.12.2 python-pptx==0.6.21

echo Installing Frontend Dependencies...
cd ../client
npm install lucide-react@0.263.1 socket.io-client@4.7.2

echo Installation complete!
echo.
echo New Features Added:
echo ✅ Custom Report Generation with PDF, DOCX, XLSX, PPTX export
echo ✅ Real-time Dashboard with live updates and WebSocket support
echo ✅ Market data streaming and performance analytics
echo ✅ Interactive dashboard with alerts and recommendations
echo.
echo To start the application:
echo Backend: python server/app.py
echo Frontend: cd client ^&^& npm run dev

pause
