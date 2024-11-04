#!/bin/bash

cd front

npm install
npm run dev &

cd ..

cd back
python3 app.py