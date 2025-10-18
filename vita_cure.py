import speech_recognition as sr
import pyttsx3
import tkinter as tk
from tkinter import scrolledtext, messagebox
from datetime import datetime

class VitaCureGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("VitaCure Health Assistant")
        self.root.geometry("600x750")
        self.root.configure(bg="#f0f0f0")

        self.engine = pyttsx3.init()
        self.conversation = []

        self.remedies = {
            "cold": "Stay hydrated, rest well, and try warm ginger tea. A steam inhalation may help too.",
            "fever": "Drink plenty of fluids, rest, and take paracetamol if necessary. Seek medical help if fever persists.",
            "headache": "Ensure proper hydration, take a break from screens, and rest in a quiet, dark room.",
            "cough": "Drink warm water with honey and lemon. Avoid cold drinks and get sufficient rest.",
            "stomach ache": "Try a bland diet like bananas, rice, and toast. Drink warm water and avoid heavy meals.",
            "sore throat": "Gargle with warm salt water and drink herbal tea with honey. Avoid cold foods."
        }

        self.create_widgets()

    def create_widgets(self):
        self.chat_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=60, height=18, font=("Arial", 12))
        self.chat_area.pack(padx=10, pady=10)

        self.voice_button = tk.Button(self.root, text="🎤 Start Voice Input",
                                      command=self.handle_voice_input,
                                      height=2, width=25, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
        self.voice_button.pack(pady=10)

        self.text_label = tk.Label(self.root, text="Or type your sickness below:", bg="#f0f0f0", font=("Arial", 12, "italic"))
        self.text_label.pack(pady=5)

        self.text_entry = tk.Entry(self.root, width=50, font=("Arial", 12))
        self.text_entry.pack(pady=5)

        self.submit_button = tk.Button(self.root, text="💊 Submit",
                                       command=self.handle_text_input,
                                       height=2, width=25, bg="#9C27B0", fg="white", font=("Arial", 12, "bold"))
        self.submit_button.pack(pady=10)

        self.prescription_button = tk.Button(self.root, text="📜 Generate Prescription",
                                             command=self.generate_prescription,
                                             height=2, width=25, bg="#2196F3", fg="white", font=("Arial", 12, "bold"))
        self.prescription_button.pack(pady=10)

        self.exit_button = tk.Button(self.root, text="❌ Exit", command=self.confirm_exit,
                                     height=2, width=25, bg="#f44336", fg="white", font=("Arial", 12, "bold"))
        self.exit_button.pack(pady=10)

    def speak(self, text):
        self.update_chat("VitaCure:", text)
        self.engine.say(text)
        self.engine.runAndWait()

    def update_chat(self, speaker, message):
        self.chat_area.insert(tk.END, f"{speaker} {message}\n\n")
        self.chat_area.see(tk.END)
        self.conversation.append((speaker, message))

    def listen(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.update_chat("System:", "🎤 Listening...")
            self.speak("How can I assist you?")
            try:
                audio = recognizer.listen(source, timeout=5)
                query = recognizer.recognize_google(audio)
                self.update_chat("You:", query)
                return query.lower()
            except sr.UnknownValueError:
                self.speak("Sorry, I couldn't understand. Please try again.")
            except sr.RequestError:
                self.speak("Error connecting to speech recognition service.")
            except sr.WaitTimeoutError:
                self.speak("I didn't hear anything. Please speak again.")
        return None

    def get_remedy(self, query):
        for disease, remedy in self.remedies.items():
            if disease in query:
                return f"For {disease}, {remedy}"
        return "I'm sorry, I couldn't find a remedy for that. Please consult a doctor."

    def handle_voice_input(self):
        query = self.listen()
        if query:
            if any(exit_word in query for exit_word in ["exit", "quit", "stop"]):
                self.confirm_exit()
            else:
                remedy = self.get_remedy(query)
                self.speak(remedy)

    def handle_text_input(self):
        query = self.text_entry.get().strip().lower()
        if not query:
            self.speak("Please enter a sickness or symptom.")
            return
        self.update_chat("You:", query)
        if any(exit_word in query for exit_word in ["exit", "quit", "stop"]):
            self.confirm_exit()
        else:
            remedy = self.get_remedy(query)
            self.speak(remedy)
        self.text_entry.delete(0, tk.END)

    def generate_prescription(self):
        if not self.conversation:
            self.update_chat("System:", "No consultation data available.")
            return

        prescription_text = f"""
=== VitaCure Health Assistant ===
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Consultation Summary:
"""
        for speaker, message in self.conversation:
            prescription_text += f"{speaker} {message}\n"

        try:
            with open("prescription.txt", "w") as file:
                file.write(prescription_text)
            self.update_chat("System:", "✅ Prescription saved as 'prescription.txt'")
        except Exception as e:
            self.update_chat("System:", f"❌ Error saving prescription: {e}")

    def confirm_exit(self):
        if messagebox.askyesno("Exit Confirmation", "Are you sure you want to exit VitaCure?"):
            self.speak("Thank you for using VitaCure. Stay healthy!")
            self.root.quit()

def main():
    root = tk.Tk()
    app = VitaCureGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
