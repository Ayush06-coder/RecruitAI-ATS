#!/bin/sh
# Start FastAPI backend in background
uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-8000} &

# Start Streamlit frontend in foreground
streamlit run App.py \
  --server.port ${STREAMLIT_PORT:-8501} \
  --server.address 0.0.0.0 \
  --server.headless true
