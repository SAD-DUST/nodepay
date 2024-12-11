name: Run Script 12pm12

on:
  workflow_dispatch:

  schedule:
    - cron: '0 6 * * *' 
    
permissions:
  contents: read

jobs:
  build:

    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4
    - name: Set up Python 3.10
      uses: actions/setup-python@v3
      with:
        python-version: "3.10"
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Run now
      run: |
        python manual-proxy.py
