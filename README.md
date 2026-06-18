# Python Web Database APP

A lightweight, high-performance full-stack Python web application featuring complete CRUD operations, built with FastAPI, Streamlit, Pydantic validation, and an SQLite3 database. Includes user authentication and a multi-page interface.

---

## 🛠️ Tech Stack & Tools

* **Frontend UI:** [Streamlit](https://streamlit.io/) — Used to build an interactive, responsive multi-page user interface entirely in Python.
* **Backend API:** [FastAPI](https://fastapi.tiangolo.com/) — A modern, high-performance web framework used to build robust RESTful APIs.
* **Data Validation:** [Pydantic](https://docs.pydantic.dev/) — Ensures strict data parsing, type-safety, and deep validation across application layers.
* **Database:** [SQLite3](https://www.sqlite.org/index.html) — A lightweight, serverless relational database management system for persistent data storage.

---

## 🚀 Key Features & Pages

The application is structured as a multi-page web app supporting secure user workflows:

* **🏠 Home Page:** the dashboard welcoming users and providing an overview of application status and page links.
* **🔐 Login Page:** secure entry point verifying user credentials before granting access to protected routes.
* **🆕 Create Account Page:** Form-driven registration interface utilizing Pydantic to validate user inputs against constraints on fields like User ID, password, DOB ,etc.
* **🔄 Update Page:** allows authenticated users to safely modify their data.
* **❌ Delete Page:** allows safe data deletion.
* **ℹ️ About Page:** brief detail about the application

---

## 📁 Project Structure

```text
├── backend/
│   ├── main.py          # FastAPI application entrypoint & API routes
│   ├── database         # SQLite3 connection setup
│   └── schemas          # Pydantic data validation models
|
├── frontend/
│   ├── 1_🏠︎_Home.py     # Main Streamlit application
│   └── pages/           # Multi-page UI scripts (Login, Create, Update, Delete, About)
├── requirements.txt     # Project dependencies
└── README.md            # Project documentation
