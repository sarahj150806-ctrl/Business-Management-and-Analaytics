# Business Management & Analytics Platform

An enterprise full-stack business analytics application designed to upload financial data (CSV/Excel), map custom transaction schemas dynamically, analyze revenue variances, identify root causes of profit losses, and perform predictive profit forecasting using machine learning.

---

## 🚀 Key Features

* **Dynamic Column Mapping**: Flexibly maps user-defined CSV/Excel headers (Items, Revenue, Cost) without requiring rigid template formats.
* **Profit Loss & Root Cause Diagnostics**: Automatically scans financial comparisons to isolate loss-making items and provides automated operational recommendations.
* **Predictive ML Analytics**: Integrates linear regression modeling to forecast upcoming profit trends based on historical baseline comparisons.
* **Dual Backend Architecture**:
  * **Node.js/Express**: Handles secure user authentication and session flows.
  * **Python/FastAPI**: Drives high-performance asynchronous data parsing, pandas data manipulations, and machine learning models.
* **Modern Dashboard UI**: Responsive blue-and-white enterprise dashboard equipped with live metrics, loss diagnostic cards, and regression forecasts.

---

## 🛠️ Tech Stack

* **Frontend**: HTML5, CSS3, JavaScript (Fetch API / Async UI)
* **Auth Backend**: Node.js, Express.js, CORS
* **Analytics Backend**: Python 3.10+, FastAPI, Pandas, NumPy, Scikit-Learn, Uvicorn
* **Deployment Ready**: Configured for Render/Railway backends and Vercel/Netlify static hosting.

---

## 📂 Project Structure

```text
├── frontend/
│   ├── index.html          # Authentication / Login portal
│   └── dashboard.html      # Main enterprise analytics interface
├── node-backend/
│   ├── server.js           # Authentication & User API service
│   └── package.json        # Node dependencies & scripts
├── python-backend/
│   ├── main.py             # FastAPI data processor & ML engine
│   └── requirements.txt    # Python data science packages
├── .gitignore              # Ignored system & build directories
└── README.md               # Project documentation
