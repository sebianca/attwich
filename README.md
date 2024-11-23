# Twitch Streamer Screenshot Test

This project automates the process of navigating to a Twitch streamer's page and taking a screenshot using Selenium and pytest.

## Prerequisites

- **Python 3.\***
- **Google Chrome** browser installed on your machine

## Setup Instructions

### 1. Clone the Repository

```bash
git clone [repository_url]
cd test_twitch
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment (Linux/MacOS)

```bash
source venv/bin/activate
```

### 3. Activate the Virtual Environment (Windows)

```bash
venv\Scripts\activate
```


### 4. Install the Required Packages

```bash
pip install -r requirements.txt
```

### 5. Run the Test

```bash
pytest test_twitch.py
```

### 5.1 Run the Test (DEBUG Mode)

```bash
pytest --capture=no test_twitch.py
```


