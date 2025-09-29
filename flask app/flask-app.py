import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import requests
from flask import Flask, request, jsonify
from urllib.parse import urlparse
import psutil
import time

# Flask App
app = Flask(__name__)

class CPUMonitor:
    """Monitor CPU usage while processing links"""
    
    @staticmethod
    def get_cpu_info():
        return {
            'cpu_percent': psutil.cpu_percent(interval=0.1),
            'cpu_count': psutil.cpu_count(),
            'memory_percent': psutil.virtual_memory().percent,
            'active_threads': threading.active_count()
        }

@app.route('/process-link', methods=['POST'])
def process_link():
    """Process link with CPU monitoring"""
    start_time = time.time()
    cpu_start = psutil.cpu_percent()
    
    try:
        data = request.get_json()
        link = data.get('link', '')
        
        if not link:
            return jsonify({'success': False, 'error': 'No link provided'}), 400
        
        # Add scheme if missing
        if not link.startswith(('http://', 'https://')):
            link = 'https://' + link
        
        # Parse URL
        parsed_url = urlparse(link)
        
        if not parsed_url.netloc:
            return jsonify({'success': False, 'error': 'Invalid URL'}), 400
        
        # Simulate CPU-intensive processing
        result = []
        for i in range(1000):
            result.append(i ** 2)
        
        # Try to fetch the link
        try:
            response = requests.head(link, timeout=5, allow_redirects=True)
            status = f"Accessible (Status: {response.status_code})"
            headers = dict(response.headers)
        except requests.RequestException as e:
            status = f"Unable to reach"
            headers = {}
        
        cpu_end = psutil.cpu_percent()
        processing_time = time.time() - start_time
        
        return jsonify({
            'success': True,
            'data': {
                'url': link,
                'domain': parsed_url.netloc,
                'scheme': parsed_url.scheme,
                'path': parsed_url.path,
                'status': status,
                'headers_count': len(headers)
            },
            'performance': {
                'processing_time': f"{processing_time:.3f}s",
                'cpu_usage_start': f"{cpu_start}%",
                'cpu_usage_end': f"{cpu_end}%",
                'cpu_count': psutil.cpu_count()
            }
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

class FlaskDesktopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flask Emulator App")
        self.root.geometry("800x600")
        self.flask_thread = None
        self.monitoring = False
        
        self.setup_ui()
        self.start_flask()
        self.start_cpu_monitoring()
    
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title = ttk.Label(main_frame, text="🔗 Flask Emulator", font=('Arial', 16, 'bold'))
        title.grid(row=0, column=0, columnspan=2, pady=10)
        
        # CPU Info Frame
        cpu_frame = ttk.LabelFrame(main_frame, text="CPU Monitor", padding="10")
        cpu_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.cpu_label = ttk.Label(cpu_frame, text="CPU: 0%")
        self.cpu_label.grid(row=0, column=0, padx=5)
        
        self.memory_label = ttk.Label(cpu_frame, text="Memory: 0%")
        self.memory_label.grid(row=0, column=1, padx=5)
        
        self.threads_label = ttk.Label(cpu_frame, text="Threads: 0")
        self.threads_label.grid(row=0, column=2, padx=5)
        
        # Link Input Frame
        input_frame = ttk.LabelFrame(main_frame, text="Process Link", padding="10")
        input_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(input_frame, text="Enter URL:").grid(row=0, column=0, sticky=tk.W)
        
        self.link_entry = ttk.Entry(input_frame, width=60)
        self.link_entry.grid(row=1, column=0, padx=5, pady=5)
        self.link_entry.insert(0, "https://example.com")
        
        self.process_btn = ttk.Button(input_frame, text="Process Link", command=self.process_link)
        self.process_btn.grid(row=1, column=1, padx=5)
        
        # Results Frame
        results_frame = ttk.LabelFrame(main_frame, text="Results", padding="10")
        results_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        self.results_text = scrolledtext.ScrolledText(results_frame, width=90, height=20)
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Status bar
        self.status_label = ttk.Label(main_frame, text="Flask server running", 
                                      relief=tk.SUNKEN)
        self.status_label.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
    
    def start_flask(self):
        """Start Flask server in background thread"""
        def run_flask():
            app.run(debug=False, host='127.0.0.1', port=5000, use_reloader=False)
        
        self.flask_thread = threading.Thread(target=run_flask, daemon=True)
        self.flask_thread.start()
        time.sleep(1)  # Give server time to start
        self.log_result("✓ Flask server started successfully\n")
    
    def start_cpu_monitoring(self):
        """Start CPU monitoring in background"""
        self.monitoring = True
        
        def monitor():
            while self.monitoring:
                try:
                    info = CPUMonitor.get_cpu_info()
                    self.cpu_label.config(text=f"CPU: {info['cpu_percent']}%")
                    self.memory_label.config(text=f"Memory: {info['memory_percent']}%")
                    self.threads_label.config(text=f"Threads: {info['active_threads']}")
                    time.sleep(1)
                except:
                    break
        
        monitor_thread = threading.Thread(target=monitor, daemon=True)
        monitor_thread.start()
    
    def process_link(self):
        """Process the link through Flask endpoint"""
        link = self.link_entry.get().strip()
        
        if not link:
            messagebox.showwarning("Warning", "Please enter a URL")
            return
        
        self.process_btn.config(state='disabled')
        self.log_result(f"\n{'='*80}\n")
        self.log_result(f"Processing: {link}\n")
        self.status_label.config(text="Processing...")
        
        def make_request():
            try:
                response = requests.post(
                    'http://localhost:5000/process-link',
                    json={'link': link},
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    self.display_results(data)
                else:
                    self.log_result(f"Error: {response.json().get('error', 'Unknown error')}\n")
                
            except requests.exceptions.ConnectionError:
                self.log_result("Error: Cannot connect to Flask server\n")
            except Exception as e:
                self.log_result(f"Error: {str(e)}\n")
            finally:
                self.process_btn.config(state='normal')
                self.status_label.config(text="Flask server running ")
        
        threading.Thread(target=make_request, daemon=True).start()
    
    def display_results(self, data):
        """Display processing results"""
        if data.get('success'):
            result_data = data['data']
            perf_data = data['performance']
            
            self.log_result("✓ Success!\n\n")
            self.log_result("Link Information:\n")
            self.log_result(f"  URL: {result_data['url']}\n")
            self.log_result(f"  Domain: {result_data['domain']}\n")
            self.log_result(f"  Scheme: {result_data['scheme']}\n")
            self.log_result(f"  Path: {result_data['path']}\n")
            self.log_result(f"  Status: {result_data['status']}\n")
            self.log_result(f"  Headers: {result_data['headers_count']} found\n\n")
            
            self.log_result("Performance Metrics:\n")
            self.log_result(f"  Processing Time: {perf_data['processing_time']}\n")
            self.log_result(f"  CPU Usage (Start): {perf_data['cpu_usage_start']}\n")
            self.log_result(f"  CPU Usage (End): {perf_data['cpu_usage_end']}\n")
            self.log_result(f"  CPU Cores: {perf_data['cpu_count']}\n")
        else:
            self.log_result(f"✗ Failed: {data.get('error', 'Unknown error')}\n")
    
    def log_result(self, message):
        """Add message to results text box"""
        self.results_text.insert(tk.END, message)
        self.results_text.see(tk.END)
        self.root.update()

def main():
    root = tk.Tk()
    app = FlaskDesktopApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()