#!/bin/bash
python3 backend/app/app.py &
echo "backend $!"
cd my-shopping-list-app
npm start &
