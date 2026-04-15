import gradio as gr
import pyrebase
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv

# Load credentials from .env if present
load_dotenv()

# Firebase Configuration
# Using provided values as defaults
config = {
    "apiKey": os.getenv("FIREBASE_API_KEY", "AIzaSyBihFNrFDNGKcLZ2h01wTWnGAsfVOvpERY"),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN", "studentfeedbacksystem-185d5.firebaseapp.com"),
    "projectId": os.getenv("FIREBASE_PROJECT_ID", "studentfeedbacksystem-185d5"),
    "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET", "studentfeedbacksystem-185d5.firebasestorage.app"),
    "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID", "461412386533"),
    "appId": os.getenv("FIREBASE_APP_ID", "1:461412386533:web:9dc4e9d746a1179edc360c"),
    "databaseURL": os.getenv("FIREBASE_DATABASE_URL", f"https://{os.getenv('FIREBASE_PROJECT_ID', 'studentfeedbacksystem-185d5')}-default-rtdb.firebaseio.com/")
}

# Initialize Firebase
try:
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
except Exception as e:
    print(f"Error initializing Firebase: {str(e)}")
    db = None

def get_latest_feedbacks():
    """Helper to fetch and format data for the table."""
    if db is None:
        return None
    try:
        all_feedbacks = db.child("feedbacks").get().val()
        if all_feedbacks:
            # We want to show latest records first
            items = list(all_feedbacks.values())
            df = pd.DataFrame(items)
            # Ensure columns exist even if some records are partial
            cols = ["timestamp", "student_name", "student_id", "course_name", "instructor_name", "rating", "comments"]
            for c in cols:
                if c not in df.columns:
                    df[c] = ""
            df = df[cols].sort_values(by="timestamp", ascending=False)
            return df
        return pd.DataFrame(columns=["timestamp", "student_name", "student_id", "course_name", "instructor_name", "rating", "comments"])
    except Exception as e:
        print(f"Fetch Error: {str(e)}")
        return None

def submit_feedback(student_name, student_id, course_name, instructor_name, rating, comments):
    """
    Handles feedback submission, updates DB, and clears form.
    """
    if not all([student_name, student_id, course_name, instructor_name]):
        return (
            gr.update(value="⚠️ Error: All fields except comments are required!", visible=True),
            get_latest_feedbacks(),
            student_name, student_id, course_name, instructor_name, rating, comments # keep values
        )

    data = {
        "student_name": student_name,
        "student_id": student_id,
        "course_name": course_name,
        "instructor_name": instructor_name,
        "rating": int(rating),
        "comments": comments,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    try:
        if db is None:
            raise Exception("Firebase connection not initialized.")
            
        db.child("feedbacks").push(data)
        
        # Success state: feedback table updated, form cleared
        success_msg = f"🎉 Success! Thank you, {student_name}. Your feedback for {course_name} has been recorded."
        
        return (
            gr.update(value=success_msg, visible=True),
            get_latest_feedbacks(),
            "", "", None, "", 5, "" # Reset input fields: name, id, course, instructor, rating, comments
        )
            
    except Exception as e:
        error_msg = f"❌ Database Error: {str(e)}"
        return (
            gr.update(value=error_msg, visible=True),
            get_latest_feedbacks(),
            student_name, student_id, course_name, instructor_name, rating, comments
        )

# --- Gradio UI Design ---
with gr.Blocks() as demo:
    gr.Markdown(
        """
        # 🎓 Institutional Student Feedback System
        ### Empowering excellence through your voice.
        """
    )
    
    with gr.Row():
        with gr.Column(scale=2):
            gr.Markdown("### 📝 Submit Your Feedback")
            with gr.Group():
                name_input = gr.Textbox(label="Full Name*", placeholder="e.g. John Doe")
                id_input = gr.Textbox(label="Student ID*", placeholder="e.g. S12345")
                with gr.Row():
                    course_input = gr.Dropdown(
                        label="Course*", 
                        choices=["CS101", "DS202", "AI303", "WEB404"], 
                        allow_custom_value=True
                    )
                    instructor_input = gr.Textbox(label="Instructor*", placeholder="e.g. Dr. Smith")
                
                rating_input = gr.Slider(label="Rating (1-5)*", minimum=1, maximum=5, step=1, value=5)
                comments_input = gr.TextArea(label="Detailed Comments", placeholder="Tell us more about your experience...", lines=4)
            
            submit_btn = gr.Button("🚀 Submit Feedback", variant="primary")
            output_status = gr.Markdown(visible=False)
            
        with gr.Column(scale=3):
            gr.Markdown("### 📊 Live Feedback Summary")
            feedback_table = gr.Dataframe(
                label="Recent Submissions (Last 50)",
                headers=["Timestamp", "Student", "ID", "Course", "Instructor", "Rating", "Comments"],
                datatype=["str", "str", "str", "str", "str", "number", "str"],
                interactive=False,
                wrap=True
            )
            refresh_btn = gr.Button("🔄 Refresh Data", variant="secondary")

    # Event Handlers
    submit_btn.click(
        fn=submit_feedback, 
        inputs=[name_input, id_input, course_input, instructor_input, rating_input, comments_input], 
        outputs=[output_status, feedback_table, name_input, id_input, course_input, instructor_input, rating_input, comments_input]
    )
    
    refresh_btn.click(fn=get_latest_feedbacks, outputs=feedback_table)

    # Initial Load
    demo.load(fn=get_latest_feedbacks, outputs=feedback_table)

if __name__ == "__main__":
    # Launching with Gradio 6.0+ compatible parameters
    demo.launch(
        share=True, 
        server_name="0.0.0.0",
        theme=gr.themes.Soft(primary_hue="indigo", secondary_hue="slate"),
        css=".feedback-box { border: 1px solid #ddd; padding: 10px; }"
    )
