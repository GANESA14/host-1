import os
import logging
from tkinter import Tk, Label, Entry, Button, filedialog, StringVar, messagebox, ttk, Frame
from yt_dlp import YoutubeDL
import threading

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('VideoDownloader')

class VideoDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-Platform Video Downloader")
        self.root.geometry("600x400")
        self.root.resizable(True, True)

        # Variables
        self.video_url = StringVar()
        self.download_path = StringVar()
        self.format_var = StringVar(value="best")
        self.status_var = StringVar(value="Ready")
        self.progress_var = StringVar(value="0%")
        
        # Set default download path to user's Downloads folder
        default_path = os.path.join(os.path.expanduser('~'), 'Downloads')
        self.download_path.set(default_path)

        self.setup_ui()

    def setup_ui(self):
        # Main container
        main_frame = Frame(self.root, padx=20, pady=10)
        main_frame.pack(fill='both', expand=True)

        # Title
        Label(main_frame, text="Multi-Platform Video Downloader", 
              font=("Arial", 16, "bold")).pack(pady=10)
        
        # Supported platforms info
        platforms = "Supports: YouTube, Instagram, Facebook, Twitter, TikTok, etc."
        Label(main_frame, text=platforms, font=("Arial", 10)).pack()

        # URL input
        url_frame = Frame(main_frame)
        url_frame.pack(fill='x', pady=10)
        Label(url_frame, text="Video URL:", font=("Arial", 11)).pack(anchor='w')
        Entry(url_frame, textvariable=self.video_url, width=60).pack(fill='x')

        # Download path selection
        path_frame = Frame(main_frame)
        path_frame.pack(fill='x', pady=10)
        Label(path_frame, text="Download Path:", font=("Arial", 11)).pack(anchor='w')
        path_entry = Entry(path_frame, textvariable=self.download_path, width=50)
        path_entry.pack(side='left', fill='x', expand=True)
        Button(path_frame, text="Browse", command=self.select_download_path).pack(side='right', padx=5)

        # Format selection
        format_frame = Frame(main_frame)
        format_frame.pack(fill='x', pady=10)
        Label(format_frame, text="Format:", font=("Arial", 11)).pack(side='left')
        formats = [
            "best (Recommended)",
            "bestvideo+bestaudio",
            "worstvideo+worstaudio",
            "audio_only"
        ]
        format_combo = ttk.Combobox(format_frame, textvariable=self.format_var, values=formats, state='readonly')
        format_combo.pack(side='left', padx=5)

        # Download button
        Button(main_frame, text="Download", command=self.start_download,
               bg="#4CAF50", fg="white", font=("Arial", 12),
               width=20).pack(pady=20)

        # Progress frame
        progress_frame = Frame(main_frame)
        progress_frame.pack(fill='x', pady=10)
        
        self.progress_bar = ttk.Progressbar(progress_frame, length=300, mode='determinate')
        self.progress_bar.pack(fill='x')
        
        status_frame = Frame(main_frame)
        status_frame.pack(fill='x')
        self.status_label = Label(status_frame, textvariable=self.status_var, font=("Arial", 10))
        self.status_label.pack(side='left')
        self.progress_label = Label(status_frame, textvariable=self.progress_var, font=("Arial", 10))
        self.progress_label.pack(side='right')

    def select_download_path(self):
        folder = filedialog.askdirectory()
        if folder:
            self.download_path.set(folder)
            logger.info(f"Download path set to: {folder}")

    def progress_hook(self, d):
        try:
            if d['status'] == 'downloading':
                total_bytes = d.get('total_bytes', 0) or d.get('total_bytes_estimate', 0)
                downloaded_bytes = d.get('downloaded_bytes', 0)
                
                if total_bytes:
                    percentage = (downloaded_bytes / total_bytes) * 100
                    self.progress_var.set(f"{percentage:.1f}%")
                    self.progress_bar['value'] = percentage
                
                speed = d.get('speed', 0)
                if speed:
                    speed_str = f"{speed/1024/1024:.1f} MB/s"
                    eta = d.get('eta', 0)
                    eta_str = f"{eta//60}:{eta%60:02d}" if eta else 'N/A'
                    self.status_var.set(f"Downloading... Speed: {speed_str}, ETA: {eta_str}")
                
                logger.debug(f"Download progress: {percentage:.1f}%, Speed: {speed_str}")

            elif d['status'] == 'finished':
                self.progress_var.set("100%")
                self.progress_bar['value'] = 100
                self.status_var.set("Download complete! Processing...")
                logger.info("Download finished successfully")

        except Exception as e:
            logger.error(f"Error in progress_hook: {str(e)}")
            self.status_var.set(f"Error: {str(e)}")

    def get_format(self):
        format_selection = self.format_var.get()
        format_dict = {
            "best (Recommended)": "best",
            "bestvideo+bestaudio": "bestvideo+bestaudio/best",
            "worstvideo+worstaudio": "worstvideo+worstaudio",
            "audio_only": "bestaudio/best"
        }
        selected_format = format_dict.get(format_selection, "best")
        logger.info(f"Selected format: {selected_format}")
        return selected_format

    def download_video(self):
        url = self.video_url.get().strip()
        path = self.download_path.get().strip()

        logger.info(f"Starting download - URL: {url}, Path: {path}")

        if not url:
            raise ValueError("Please enter a valid URL")
        if not path:
            raise ValueError("Please select a download path")
        if not os.path.exists(path):
            os.makedirs(path)
            logger.info(f"Created download directory: {path}")

        # Configure yt-dlp options
        ydl_opts = {
            'outtmpl': os.path.join(path, '%(title)s.%(ext)s'),
            'format': self.get_format(),
            'progress_hooks': [self.progress_hook],
            'ignoreerrors': False,  # Changed to False to see errors
            'no_warnings': False,   # Changed to False to see warnings
            'quiet': False,         # Changed to False to see output
            'verbose': True,        # Added verbose output
        }

        logger.debug(f"yt-dlp options: {ydl_opts}")

        # Add format-specific options
        if self.format_var.get() == "audio_only":
            ydl_opts.update({
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            })

        try:
            # Download the video
            with YoutubeDL(ydl_opts) as ydl:
                logger.info("Starting yt-dlp download")
                info = ydl.extract_info(url, download=False)
                logger.info(f"Video information extracted: {info.get('title', 'Unknown title')}")
                ydl.download([url])
                logger.info("Download completed successfully")
        except Exception as e:
            logger.error(f"Download failed: {str(e)}")
            raise

    def start_download(self):
        # Reset progress
        self.progress_bar['value'] = 0
        self.progress_var.set("0%")
        self.status_var.set("Starting download...")
        logger.info("Starting new download")

        # Start download in a separate thread
        thread = threading.Thread(target=self.download_thread, daemon=True)
        thread.start()

    def download_thread(self):
        try:
            self.download_video()
            self.root.after(0, self.download_complete)
        except Exception as e:
            logger.error(f"Error in download thread: {str(e)}")
            self.root.after(0, lambda: self.download_error(str(e)))

    def download_complete(self):
        self.status_var.set("Download complete!")
        logger.info("Download completed successfully")
        messagebox.showinfo("Success", "Download completed successfully!")

    def download_error(self, error_message):
        self.status_var.set("Download failed")
        self.progress_var.set("0%")
        self.progress_bar['value'] = 0
        logger.error(f"Download failed: {error_message}")
        messagebox.showerror("Error", f"Download failed: {error_message}")

if __name__ == "__main__":
    root = Tk()
    app = VideoDownloader(root)
    root.mainloop()