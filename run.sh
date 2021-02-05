#!/bin/bash
echo starting chatbot...
exec rasa run -m models --enable-api --cors "*" --debug --port 5500 &
exec docker run -p 8000:8000 rasa/duckling &
exec docker run -p 5055:5055 mauricetk/rasa-custom-actions-booking-assistant:custom5 &
exec python3 webclient/app.py
echo chatbot is running  