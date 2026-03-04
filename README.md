# Orbit Application

This is a Flask application that provides a dynamic form and stores submissions in a database.

## Deployment on Render

This project is configured for deployment on [Render](https://render.com/).

### Prerequisites

*   A GitHub account with this repository.
*   A Render account.

### Deployment Steps

1.  **Push to GitHub:** Ensure all files, including `render.yaml`, are pushed to your GitHub repository.

2.  **Create a Blueprint Service on Render:**
    *   Log in to your Render account.
    *   Click the **New +** button and select **Blueprint**.
    *   Connect the GitHub repository for this project.
    *   Render will automatically detect the `render.yaml` file and begin deploying your web service and a PostgreSQL database.

3.  **Initialize the Database:**
    *   After the first deployment, you must create the database tables.
    *   Go to your new service's dashboard on Render.
    *   Open the **Shell** tab.
    *   Execute the following command:
        ```bash
        python -c 'from form_backend import db, app; app.app_context().push(); db.create_all()'
        ```

Your application will then be live at the URL provided by Render.

### Local Development

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the application:**
    ```bash
    python form_backend.py
    ```
    The application will be available at `http://127.0.0.1:5001/`.
    Local development uses an SQLite database (`submissions.db`).
