# wiserank

**wiserank** is a simple platform for running pairwise comparison experiments: participants can select a set of items to compare, make pairwise comparisons, and visualize an inferred ranking. Made with [flask](https://flask.palletsprojects.com/en/3.0.x/) and [Vue.js](https://vuejs.org/), wiserank can either be run locally as is to support experiments in a lab setting or modified slightly for use as a full web application.

## Tutorial

Follow this tutorial to download and setup wiserank for an initial pairwise comparison experiment.

### Download wiserank repository

Use `git clone` to download the wiserank repository either via HTTPS

```shell
git clone https://github.com/LarremoreLab/wiserank.git
```

or SSH

```shell
git clone git@github.com:LarremoreLab/wiserank.git
```

### Add Item Data

Wiserank contains four example datasets of items to compare: movies, academic journals, soccer players, and stocks from the S&P 500.

Add any files with items you want users to compare as .csv files in the data/parsed directory. Each csv file should have the following columns:

- "track": a label that indicates a collection of items that can be compared
- "link_id": an id that uniquely identifies the item in the context of the other items in its original dataset
- "name": a display name for an item
- "meta": an additional piece of metadata to be displayed along with the name but only after comparisons have been made (optional)

Delete the example files containing items that you do not want users to be able to compare. For the tutorial and testing, it can be useful to keep a couple of these (e.g. movies, academic journals).

### Create Python virtual environment

Via terminal, create a Python virtual environment in the root of the wiserank directory:

  ```shell
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  ```

### Initialize the local database and load the item data

In terminal and with the created virtual environment active, navigate to the backend directory: `cd backend`. Run the database initialization script: `python initialize_db.py`

### Start the backend, flask application

From the backend directory run: `flask --app wiserank --debug run -p 5001`

### Start the frontend, Vue.js application

If necessary, install [npm](https://nodejs.org/en/download/package-manager). Then, in a new terminal window navigate to the frontend directory. Install node dependencies: `npm install` and then serve the web app: `npm run serve`

### Interact with wiserank in the browser

In a web browser, navigate to [localhost:8080](http://localhost:8080). Create an account as prompted and try out wiserank with one of the example datasets (hint: searching for items in the selection stage can help jump-start the item recommendation algorithms for movies and academic journals).

Depending on how study participants will interact with wiserank, the code in frontend/src/App.vue can be changed to prevent participants from creating accounts or accessing any account with only the relevant email/username.
