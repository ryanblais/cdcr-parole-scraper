
# cdcr-parole-scraper

This is a Python project that uses a virtual environment (venv) for dependency management.

## Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

## Setup

1. Clone the repository:
    ```
    git clone git@github.com:ryanblais/cdcr-parole-scraper.git
    cd cdcr-parole-scraper
    ```

2. Create a virtual environment:
    ```
    python3 -m venv venv
    ```

3. Activate the virtual environment:
    - On Linux or MacOS:
        ```
        source venv/bin/activate
        ```
    - On Windows:
        ```
        .\venv\Scripts\activate
        ```

4. Install the required packages:
    ```
    pip install -r requirements.txt
    ```

5. Install playwright:
    ```
    playwright install
    ```


## Running the Application

After setting up the project and activating the virtual environment, you can run the application with the following command:

```
python3 -m app.main
```
