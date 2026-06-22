#!/bin/sh
# FastAPI runs on a fixed internal port (not the Render-assigned $PORT)
uvicorn backend.main:app --host 0.0.0.0 --port 8000 &

# Streamlit gets $PORT from Render (the port Render routes public traffic to)
streamlit run App.py \
  --server.port ${PORT:-8501} \
  --server.address 0.0.0.0 \
  --server.headless true
