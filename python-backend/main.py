import pandas as pd
import numpy as np
from io import BytesIO
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sklearn.linear_model import LinearRegression
from typing import Optional

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def parse_file(file: UploadFile):
    contents = await file.read()
    filename = (file.filename or "").lower()
    
    if filename.endswith('.csv'):
        return pd.read_csv(BytesIO(contents))
    elif filename.endswith(('.xlsx', '.xls')):
        return pd.read_excel(BytesIO(contents))
    else:
        raise HTTPException(status_code=400, detail="Invalid file format")

@app.post("/api/compare")
async def compare_files(
    file1: UploadFile = File(...),
    file2: UploadFile = File(...),
    item_col: Optional[str] = Form("Item"),
    revenue_col: Optional[str] = Form("Revenue"),
    cost_col: Optional[str] = Form("Cost")
):
    df1 = await parse_file(file1)
    df2 = await parse_file(file2)

    for col, name in [(item_col, 'Item'), (revenue_col, 'Revenue'), (cost_col, 'Cost')]:
        if col not in df1.columns or col not in df2.columns:
            raise HTTPException(
                status_code=400, 
                detail=f"Column '{col}' specified for {name} not found in uploaded files."
            )

    df1 = df1.rename(columns={item_col: 'Item', revenue_col: 'Revenue', cost_col: 'Cost'})
    df2 = df2.rename(columns={item_col: 'Item', revenue_col: 'Revenue', cost_col: 'Cost'})

    df1['Profit'] = df1['Revenue'] - df1['Cost']
    df2['Profit'] = df2['Revenue'] - df2['Cost']

    rev1, rev2 = df1['Revenue'].sum(), df2['Revenue'].sum()
    cost1, cost2 = df1['Cost'].sum(), df2['Cost'].sum()
    prof1, prof2 = df1['Profit'].sum(), df2['Profit'].sum()

    merged = pd.merge(df1, df2, on='Item', suffixes=('_base', '_comp'))
    merged['profit_change'] = merged['Profit_comp'] - merged['Profit_base']
    merged['cost_change'] = merged['Cost_comp'] - merged['Cost_base']

    loss_causes = []
    for _, row in merged[merged['profit_change'] < 0].iterrows():
        reason = "Cost increase" if row['cost_change'] > 0 else "Revenue drop"
        action = "Renegotiate vendor prices" if reason == "Cost increase" else "Adjust marketing strategy"
        loss_causes.append({
            "item": str(row['Item']),
            "profit_change": float(row['profit_change']),
            "reason": reason,
            "action": action
        })

    X = np.array([1, 2]).reshape(-1, 1)
    y = np.array([prof1, prof2])
    model = LinearRegression().fit(X, y)
    next_profit_pred = float(model.predict(np.array([[3]]))[0])

    return {
        "summary": {
            "revenue_variance": float(rev2 - rev1),
            "cost_variance": float(cost2 - cost1),
            "profit_variance": float(prof2 - prof1),
            "predicted_next_profit": round(next_profit_pred, 2)
        },
        "loss_causes": loss_causes
    }