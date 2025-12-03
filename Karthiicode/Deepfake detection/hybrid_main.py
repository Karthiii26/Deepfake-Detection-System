import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk
import threading
import time
import os
from hybrid_predict import predict_hybrid

ctk.set_appearance_mode("dark")

SLEEK_COLORS = {
    "bg_primary": "#1E293B",      
    "bg_secondary": "#334155",    
    "bg_card": "#475569",         
    "bg_accent": "#3B82F6",       
    "text_primary": "#F8FAFC",    
    "text_secondary": "#CBD5E1",     
    "error": "#EF4444",           
    "warning": "#F59E0B"          
}

MAX_IMAGES = 50

class DeepfakeDetectorApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Deepfake Detection System")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        # Set the background color
        self.root.configure(fg_color=SLEEK_COLORS["bg_primary"])
        
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        
        self.selected_files = []
        self.result_frames = []
        self.is_processing = False
        
        self.setup_ui()
        
    def setup_ui(self):
        header_frame = ctk.CTkFrame(
            self.root, 
            height=100, 
            corner_radius=0,
            fg_color=SLEEK_COLORS["bg_accent"]
        )
        header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        header_frame.grid_columnconfigure(1, weight=1)
        header_frame.grid_propagate(False)
        
        logo_frame = ctk.CTkFrame(
            header_frame,
            width=80,
            height=80,
            corner_radius=30,       
            fg_color=SLEEK_COLORS["bg_accent"]
        )
        logo_frame.grid(row=0, column=0, padx=20, pady=10)
        logo_frame.grid_propagate(False)

        try:
            logo_img = Image.open("logo.png").resize((96, 96), Image.Resampling.LANCZOS)
            logo_photo = ImageTk.PhotoImage(logo_img)
            logo_label = ctk.CTkLabel(
                logo_frame, 
                image=logo_photo,
                text="",  
            )
            logo_label.image = logo_photo 
            logo_label.place(relx=0.5, rely=0.5, anchor="center")
        except Exception as e:
            logo_label = ctk.CTkLabel(
                logo_frame,
                text="🛡️",
                font=("Segoe UI", 28),
                text_color=SLEEK_COLORS["text_primary"]
            )
            logo_label.place(relx=0.5, rely=0.5, anchor="center")

        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.grid(row=0, column=1, sticky="w", padx=(10, 0), pady=10)
        
        title_label = ctk.CTkLabel(
            title_frame, 
            text="Deepfake Detection System", 
            font=("Segoe UI", 24, "bold"),
            text_color=SLEEK_COLORS["text_primary"]
        )
        title_label.pack(anchor="w")
        
        subtitle_label = ctk.CTkLabel(
            title_frame,
            text="Advanced AI-powered face authenticity analysis",
            font=("Segoe UI", 14),
            text_color=SLEEK_COLORS["text_secondary"]
        )
        subtitle_label.pack(anchor="w")
        
        # Control Panel with sleek buttons
        control_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        control_frame.grid(row=0, column=2, padx=20, pady=10, sticky="e")
        
        self.select_button = ctk.CTkButton(
            control_frame,
            text="Select Images",
            command=self.select_files,
            font=("Segoe UI", 14, "bold"),
            height=40,
            width=140,
            fg_color=SLEEK_COLORS["bg_accent"],
            hover_color="#5B63D3",
            corner_radius=8
        )
        self.select_button.pack(side="left", padx=(0, 10))
        
        self.clear_button = ctk.CTkButton(
            control_frame,
            text="Clear All",
            command=self.clear_results,
            font=("Segoe UI", 14),
            height=40,
            width=100,
            fg_color=SLEEK_COLORS["bg_card"],
            hover_color="#242B3D",
            corner_radius=8
        )
        self.clear_button.pack(side="left")
        
        # Main Content Area with sleek background
        main_frame = ctk.CTkFrame(
            self.root, 
            corner_radius=0,
            fg_color=SLEEK_COLORS["bg_primary"]
        )
        main_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        
        # Status Bar with sleek styling
        status_frame = ctk.CTkFrame(
            main_frame, 
            height=50, 
            corner_radius=0,
            fg_color=SLEEK_COLORS["bg_secondary"]
        )
        status_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        status_frame.grid_columnconfigure(1, weight=1)
        status_frame.grid_propagate(False)
        
        self.status_label = ctk.CTkLabel(
            status_frame,
            text="Ready to analyze images",
            font=("Segoe UI", 12),
            text_color=SLEEK_COLORS["text_secondary"]
        )
        self.status_label.grid(row=0, column=0, padx=20, pady=15, sticky="w")
        
        self.progress_bar = ctk.CTkProgressBar(
            status_frame, 
            width=200, 
            height=8,
            progress_color=SLEEK_COLORS["bg_accent"],
            fg_color=SLEEK_COLORS["bg_card"]
        )
        self.progress_bar.grid(row=0, column=1, padx=20, pady=15, sticky="e")
        self.progress_bar.set(0)
        
        # Results Area with sleek scrollable frame
        self.results_frame = ctk.CTkScrollableFrame(
            main_frame, 
            corner_radius=0,
            fg_color=SLEEK_COLORS["bg_primary"]
        )
        self.results_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        self.results_frame.grid_columnconfigure(0, weight=1)
        
        # Welcome message
        self.show_welcome_message()
        
    def show_welcome_message(self):
        welcome_frame = ctk.CTkFrame(
            self.results_frame, 
            height=300,
            fg_color=SLEEK_COLORS["bg_card"],
            corner_radius=12
        )
        welcome_frame.grid(row=0, column=0, sticky="ew", padx=40, pady=40)
        welcome_frame.grid_columnconfigure(0, weight=1)
        welcome_frame.grid_propagate(False)
        
        icon_label = ctk.CTkLabel(
            welcome_frame, 
            text="📁", 
            font=("Segoe UI", 64),
            text_color=SLEEK_COLORS["text_secondary"]
        )
        icon_label.grid(row=0, column=0, pady=(40, 20))
        
        welcome_title = ctk.CTkLabel(
            welcome_frame,
            text="Upload Images for Analysis",
            font=("Segoe UI", 20, "bold"),
            text_color=SLEEK_COLORS["text_primary"]
        )
        welcome_title.grid(row=1, column=0, pady=(0, 10))
        
        welcome_desc = ctk.CTkLabel(
            welcome_frame,
            text="Select up to 50 images to detect deepfakes\nSupported formats: JPG, PNG, WEBP",
            font=("Segoe UI", 14),
            text_color=SLEEK_COLORS["text_muted"]
        )
        welcome_desc.grid(row=2, column=0, pady=(0, 40))
        
        self.welcome_frame = welcome_frame
        
    def select_files(self):
        if self.is_processing:
            return
            
        filetypes = [
            ("Image files", "*.jpg *.jpeg *.png *.webp"),
            ("All files", "*.*")
        ]
        
        files = filedialog.askopenfilenames(
            title="Select Images for Deepfake Detection",
            filetypes=filetypes
        )
        
        if files:
            self.selected_files = list(files)[:MAX_IMAGES]
            self.display_results()
            self.start_analysis()
    
    def display_results(self):
    # Destroy the upload placeholder card if present
        if hasattr(self, 'welcome_frame') and self.welcome_frame:
            self.welcome_frame.destroy()
            self.welcome_frame = None

        # Clear existing result frames
        for card_data in self.result_frames:
            card_data['frame'].destroy()
        self.result_frames.clear()

        # Now add new result cards
        for i, file_path in enumerate(self.selected_files):
            self.create_result_card(file_path, i)

    
    def create_result_card(self, file_path, index):
        # Main card frame with sleek styling
        card_frame = ctk.CTkFrame(
            self.results_frame, 
            height=140,
            fg_color=SLEEK_COLORS["bg_card"],
            corner_radius=12
        )
        card_frame.grid(row=index, column=0, sticky="ew", padx=20, pady=10)
        card_frame.grid_columnconfigure(1, weight=1)
        card_frame.grid_propagate(False)
        
        # Image thumbnail with sleek frame
        image_frame = ctk.CTkFrame(
            card_frame, 
            width=120, 
            height=120,
            fg_color=SLEEK_COLORS["bg_secondary"],
            corner_radius=8
        )
        image_frame.grid(row=0, column=0, padx=15, pady=10)
        image_frame.grid_propagate(False)
        
        try:
            image = Image.open(file_path)
            image = image.resize((100, 100), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            
            image_label = ctk.CTkLabel(image_frame, image=photo, text="")
            image_label.image = photo  # Keep reference
            image_label.place(relx=0.5, rely=0.5, anchor="center")
        except Exception:
            image_label = ctk.CTkLabel(
                image_frame, 
                text="❌", 
                font=("Segoe UI", 32),
                text_color=SLEEK_COLORS["error"]
            )
            image_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Information panel
        info_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
        info_frame.grid(row=0, column=1, sticky="nsew", padx=15, pady=10)
        info_frame.grid_columnconfigure(0, weight=1)
        
        # File name
        filename = os.path.basename(file_path)
        if len(filename) > 60:
            filename = filename[:57] + "..."
        
        name_label = ctk.CTkLabel(
            info_frame,
            text=filename,
            font=("Segoe UI", 16, "bold"),
            anchor="w",
            text_color=SLEEK_COLORS["text_primary"]
        )
        name_label.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        # Status
        status_label = ctk.CTkLabel(
            info_frame,
            text="🔄 Analyzing...",
            font=("Segoe UI", 18, "bold"),
            anchor="w",
            text_color=SLEEK_COLORS["text_secondary"]
        )
        status_label.grid(row=1, column=0, sticky="ew", pady=(0, 5))
        
        # Confidence
        confidence_label = ctk.CTkLabel(
            info_frame,
            text="Confidence: Analyzing...",
            font=("Segoe UI", 14),
            anchor="w",
            text_color=SLEEK_COLORS["text_muted"]
        )
        confidence_label.grid(row=2, column=0, sticky="ew", pady=(0, 5))
        
        # Processing time
        time_label = ctk.CTkLabel(
            info_frame,
            text="Processing time: --",
            font=("Segoe UI", 12),
            anchor="w",
            text_color=SLEEK_COLORS["text_muted"]
        )
        time_label.grid(row=3, column=0, sticky="ew")
        
        # Store references
        card_data = {
            'frame': card_frame,
            'status': status_label,
            'confidence': confidence_label,
            'time': time_label,
            'path': file_path
        }
        
        self.result_frames.append(card_data)
    
    def start_analysis(self):
        self.is_processing = True
        self.select_button.configure(state="disabled", text="Processing...")
        self.status_label.configure(text=f"Analyzing {len(self.selected_files)} images...")
        self.progress_bar.set(0)
        
        # Start processing in separate thread
        thread = threading.Thread(target=self.process_images, daemon=True)
        thread.start()
    
    def process_images(self):
        total_files = len(self.selected_files)
        real_count = 0
        fake_count = 0
        error_count = 0
        
        for i, card_data in enumerate(self.result_frames):
            start_time = time.time()
            
            try:
                # Call your prediction function
                pred, conf = predict_hybrid(card_data['path'])
                processing_time = time.time() - start_time
                
                # Update UI on main thread
                self.root.after(0, self.update_card_result, i, pred, conf, processing_time)
                
                if pred.lower() == "real":
                    real_count += 1
                elif pred.lower() == "fake":
                    fake_count += 1
                else:
                    error_count += 1
                    
            except Exception as e:
                processing_time = time.time() - start_time
                self.root.after(0, self.update_card_error, i, str(e), processing_time)
                error_count += 1
            
            # Update progress
            progress = (i + 1) / total_files
            self.root.after(0, self.progress_bar.set, progress)
        
        # Analysis complete
        self.root.after(0, self.analysis_complete, real_count, fake_count, error_count)
    
    def update_card_result(self, index, prediction, confidence, processing_time):
        card_data = self.result_frames[index]
        
        if prediction.lower() == "real":
            status_text = "✅ AUTHENTIC"
            text_color = SLEEK_COLORS["success"]
        else:
            status_text = "⚠️ DEEPFAKE DETECTED"
            text_color = SLEEK_COLORS["error"]
        
        card_data['status'].configure(text=status_text, text_color=text_color)
        card_data['confidence'].configure(text=f"Confidence: {int(confidence)}%", text_color=text_color)
        card_data['time'].configure(text=f"Processing time: {processing_time:.2f}s")
    
    def update_card_error(self, index, error, processing_time):
        card_data = self.result_frames[index]
        card_data['status'].configure(text="❌ ANALYSIS FAILED", text_color=SLEEK_COLORS["error"])
        card_data['confidence'].configure(text="Confidence: N/A", text_color=SLEEK_COLORS["error"])
        card_data['time'].configure(text=f"Processing time: {processing_time:.2f}s")
    
    def analysis_complete(self, real_count, fake_count, error_count):
        self.is_processing = False
        self.select_button.configure(state="normal", text="Select Images")
        
        status_text = f"Analysis complete: {real_count} Authentic, {fake_count} Deepfake, {error_count} Errors"
        self.status_label.configure(text=status_text)
        
        self.progress_bar.set(1)
    
    def clear_results(self):
        if self.is_processing:
            return
            
        # Clear all result frames
        for card_data in self.result_frames:
            card_data['frame'].destroy()
        self.result_frames.clear()
        self.selected_files.clear()
        
        # Reset UI
        self.status_label.configure(text="Ready to analyze images")
        self.progress_bar.set(0)
        
        # Show welcome message again
        self.show_welcome_message()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = DeepfakeDetectorApp()
    app.run()
