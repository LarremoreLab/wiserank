# wiserank

A general platform for ranking from pairwise comparisons

## Setup

- Add any files with items you want users to compare as csv files in the data/parsed directory.
  - Each csv file should have the following columns:
    - "track": a label that indicates a collection of items that can be compared
    - "link_id": an id that uniquely identifies the item in the context of the other items in its original dataset
    - "name": a display name for an item
    - "meta": an additional piece of metadata to be displayed along with the name but only after comparisons have been made (optional)
  - Delete the example files containing items that you do not want users to be able to compare.

- Via terminal, create a python virtual environment in the root of the wiserank directory:

  ```shell
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  ```

- navigate to the backend directory: `cd backend`
- in terminal, run the database initialization script: `python initialize_db.py`

- start the backend
  - from the backend directory, `flask --app wiserank --debug run -p 5001`
- start the frontend (install [npm](https://nodejs.org/en/download/package-manager) if you do not already have it)
  - in a new terminal, from the frontend directory:
    - install node dependencies: `npm install`
    - serve the web app: `npm run serve`

- navigate to [localhost:8080](http://localhost:8080)
