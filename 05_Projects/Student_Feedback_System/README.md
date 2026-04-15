# 🎓 Student Feedback System (V2)

A premium student feedback system built with **Gradio** for a seamless UI and **Firebase** for cloud data storage, now with enhanced features!

## ✨ New in V2:
- **Auto-Clearing Form**: Form fields reset after a successful submission for better user experience.
- **Enhanced Data Handling**: Records are now sorted so you see the **latest feedback at the top**.
- **Secure Configuration**: Support for `.env` files to keep your API keys separate from your code.
- **UI Refresh**: Added a 'Refresh' button to manually sync data without reloading the page.
- **Robust Error Handling**: Better validation and informative error messages.

## 🚀 How to Run

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Firebase
1. Go to your [Firebase Console](https://console.firebase.google.com/).
2. Select your project: `studentfeedbacksystem-185d5`.
3. In the sidebar, click on **Build** -> **Realtime Database**.
4. Click **Create Database** and set it up in **Test Mode** (or update rules for public write access).
5. (Optional but Recommended) Copy ` .env.example` to `.env` and update the values there.

### 3. Run the App
```bash
python app.py
```
This will launch the app and provide a public URL for everyone to use (valid for 72 hours via Gradio share).

## 🛠️ Technology Stack
- **UI**: Gradio (Soft Theme)
- **Cloud Backend**: Pyrebase4 (Firebase Python Wrapper)
- **Data Engine**: Pandas
- **Security**: Python-dotenv
