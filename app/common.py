"""Hàm dùng chung cho các trang của app."""
import re
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "ket_qua"
MODEL_PATH = ROOT / "model" / "model.joblib"


@st.cache_data
def load_csv(name: str) -> pd.DataFrame:
    """Đọc CSV trong ket_qua/ (file Excel-friendly có BOM nên dùng utf-8-sig)."""
    return pd.read_csv(RESULTS / name, encoding="utf-8-sig")


@st.cache_resource
def load_model():
    if not MODEL_PATH.exists():
        return None
    return joblib.load(MODEL_PATH)


def normalize(text: str) -> str:
    """Đưa văn bản thô về dạng gần giống dữ liệu train: chữ thường, dấu câu tách bằng khoảng trắng."""
    text = text.lower()
    text = re.sub(r'([.,;:!?()\[\]"“”‘’\'])', r" \1 ", text)
    return re.sub(r"\s+", " ", text).strip()
