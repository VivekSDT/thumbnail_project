# 🖼️ Thumbnail Generator Pipeline

A Python-based multiprocessing system that automatically watches a directory for new images, generates thumbnails, and stores them efficiently — complete with configurable settings, batch processing, and logging.

---

## 🚀 Features

- **Directory Watcher** – Continuously monitors an input folder for new images.  
- **Config-driven Setup** – All settings come from `.env` for flexibility.  
- **Batch Processing** – Groups images before sending to consumers for better efficiency.  
- **Parallel Consumers** – Multiple consumers process batches in parallel for speed.  
- **Centralized Logging** – Unified structured logs for easy debugging and monitoring.  
- **Progress Tracking** – Visual progress with optional tqdm integration.  
- **Extensible Design** – Easy to extend for image transformations or cloud integration (S3, SNS, etc.).

---

## 🧰 Project Structure

```bash
thumbnail_project/
│
├── producer/           # Input folder for raw images
├── consumer/           # Output folder for thumbnails
├── logs/               # Stores log files
│
├── main.py             # Entry point for the application
├── producer_module.py  # Handles image discovery & batching
├── consumer_module.py  # Processes and saves thumbnails
├── config_loader.py    # Loads configuration from environment
├── logger_config.py    # Configures logging system
│
├── .env                # Environment-specific variables (excluded from git)
├── sample_env          # Template for .env
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```



---

## ⚙️ Setup Instructions

### 1 Clone the repository
```bash
git clone https://github.com/viveksdt/thumbnail_project.git
cd thumbnail_project
```

### 2 Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3 Install dependencies
```bash
pip install -r requirements.txt
```

### 4 Configure environment
```bash
cp sample_env .env
```

---

## Usage
1. Place your images inside the producer/ folder.
2. Run the main script:
```bash
python main.py
```
3. Thumbnails will be saved in the consumer/ folder.
4. Logs are written to logs/process.log.

