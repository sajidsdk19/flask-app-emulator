# flask-app-emulator
app to process links 
# Flask CPU Emulator Desktop App

A desktop application that processes URLs with real-time CPU monitoring. The app runs Flask in the background and provides a GUI interface for link processing with performance metrics.

## Features

- 🖥️ Desktop GUI application (no browser required)
- 📊 Real-time CPU and memory monitoring
- 🔗 URL processing with performance metrics
- ⚡ Multi-threaded Flask server
- 📈 Detailed processing statistics

## Prerequisites

Before running this application, ensure you have:

- **Python 3.7 or higher** installed on your system
- **pip** (Python package installer)



## Installation

### Step 1: Download the Application

Save the application code as `flask-app.py` in a folder of your choice.

### Step 2: Create a Virtual Environment (Recommended)

Open your terminal/command prompt and navigate to the folder containing `flask-app.py`:

```bash
# On Windows
cd path\to\your\folder
python -m venv venv
venv\Scripts\activate


### Step 3: Install Required Dependencies

Install all required packages using pip:

```bash
pip install flask requests psutil
```

Or create a `requirements.txt` file with the following content:

```
flask==3.0.0
requests==2.31.0
psutil==5.9.6
```

Then install using:

```bash
pip install -r requirements.txt
```

## Running the Application

### Method 1: Simple Run

```bash
python flask-app.py
```

### Method 2: With Virtual Environment

```bash
# Activate virtual environment first
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# Then run the app
python app.py
```

## Using the Application

### Main Interface

Once the application starts, you'll see a window with three main sections:

#### 1. CPU Monitor (Top)
- **CPU**: Shows current CPU usage percentage
- **Memory**: Shows current memory usage percentage
- **Threads**: Shows number of active threads

#### 2. Process Link (Middle)
- **Enter URL**: Type or paste the URL you want to process
- **Process Link Button**: Click to start processing

#### 3. Results (Bottom)
- Displays detailed information about the processed link
- Shows performance metrics including:
  - Processing time
  - CPU usage before and after
  - Link status and headers

### Example Usage

1. The app starts with `https://example.com` pre-filled
2. Click **"Process Link"** to test
3. View results in the results panel
4. Try different URLs like:
   - `https://google.com`
   - `https://github.com`
   - `example.com` (automatically adds https://)

### Sample Output

```
================================================================================
Processing: https://example.com

✓ Success!

Link Information:
  URL: https://example.com
  Domain: example.com
  Scheme: https
  Path: /
  Status: Accessible (Status: 200)
  Headers: 12 found

Performance Metrics:
  Processing Time: 0.234s
  CPU Usage (Start): 15.2%
  CPU Usage (End): 18.7%
  CPU Cores: 8
```

## API Endpoint (Advanced)

The Flask server also runs on `http://localhost:5000` and accepts POST requests:

```bash
curl -X POST http://localhost:5000/process-link \
  -H "Content-Type: application/json" \
  -d '{"link": "https://example.com"}'
```

## Troubleshooting

### Common Issues

#### 1. "Module not found" error
```bash
# Make sure all dependencies are installed
pip install flask requests psutil
