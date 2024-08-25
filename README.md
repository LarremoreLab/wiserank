# wiserank

A general platform for ranking from pairwise comparisons

## Setup

- Add any files with items you want users to compare as csv files in the data/parsed directory.
  - Each csv file should have the following columns: "track", "link_id", "name", "meta".
  - Delete the example files containing items that you do not want users to be able to compare.

- Create a python virtual environment in the root of the directory
  - python3 -m venv .venv
  - source .venv/bin/activate
  - pip install -r requirements.txt

- navigate to the backend directory
  - cd backend
- in terminal, run the database initialization script
  - "python initialize.py"

- start the backend
  - from the backend directory, "flask --app wiserank --debug run -p 5001"
- start the frontend
  - in a new terminal, from the frontend directory, "npm run serve"

- navigate to http://localhost:8080