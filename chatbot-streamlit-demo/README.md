## Getting Started

### Prerequisites

Ensure you have Python installed. It is recommended to use `miniconda` or `conda` for environment management.

### Installation

1.  **Install Miniconda (if not already installed)**

    Download and install Miniconda from the official website: <mcurl name="Miniconda Installer" url="https://docs.conda.io/en/latest/miniconda.html"></mcurl>

2.  **Create a Conda Environment**

    Open your terminal or Anaconda Prompt and create a new environment:

    ```bash
    conda create -n chatbot-env python=3.9
    conda activate chatbot-env
    ```

3.  **Install Requirements**

    Navigate to the project directory and install the necessary packages:

    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Streamlit Application**

    ```bash
    streamlit run streamlit_app.py

    The application will open in your web browser.

### Running with Docker (Optional)

1.  **Build the Docker Image**

    Navigate to the project directory and build the Docker image:

    ```bash
    docker build -t chatbot-streamlit-demo .
    ```

2.  **Run the Docker Container**

    Run the Docker container, mapping port 8501:

    ```bash
    docker run -p 8501:8501 chatbot-streamlit-demo
    ```

    The application will be accessible in your web browser at `http://localhost:8501`.

## Code Structure

- streamlit_app.py: The main Streamlit application file, containing the chatbot UI and logic.
- database_tools.py: Contains functions for interacting with the sales_data.db database.
- requirements.txt: Lists all Python dependencies required for the project.
- streamlit_react_app.py: (Optional) Another Streamlit application, possibly demonstrating React integration.
- streamlit_react_tools_app.py: (Optional) Another Streamlit application, possibly demonstrating React tools integration.
