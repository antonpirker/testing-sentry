# Redis Cache Module

This project includes a simple Django application that uses 
Djangos caching framework and sends data about cache utilization
to Sentry.io.

## Load Testing Procedure

### Setup Test Environment

This is how you setup the test environment (Dont worry, a virtual env will be created 
and all dependencies installed): 

```bash
# Clone Repo
git clone https://github.com/antonpirker/testing-sentry.git

# Enter directory
cd testing-sentry/test-django-cache-module

# In one terminal: Start Django
./run-django.sh

# In another terminal: Start Locust server
./run-locust.sh
```

### Conduct the Load Test

- Point your browser to the Locust server: **http://0.0.0.0:8089**
- Enter the following:
    - Number of users peak: **100**
    - Ramp up: **3**
    - Host: **http://127.0.0.1:8000**
    - Run time (under advanced options): **5m**
- Click **START**
- Look at the Locust charts! ^^
- After the test has finished hit **CTRL+C in the Django terminal**
- Run **`mprof plot`** in the Django terminal (this will show you the memory profile of the run)
- **Generate the Locust report**: Within the Locust web UI, navigate to the "Download Data" tab, 
  then select "Download Report." The HTML report opens in a new tab. Click the 
  "Download the Report" link at the top right of the page to download the report HTML file.
- Put the test results in the `/results/` folder (und a nicely named subfolder)
- Thanks! Have a nice day!