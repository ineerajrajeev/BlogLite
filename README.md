## BlogLite

BlogLite is a simple and lightweight blog sharing platform built using Vue.JS for the frontend and Flask for the backend jobs and API. It utilizes Redis for caching and Celery along with Redis to schedule tasks.

## Features

-   User registration and login
-   Create and edit blog posts
-   View and search for other users' posts
-   Like posts
### Technologies Used

-   Vue.js: A progressive JavaScript framework for building user interfaces
-   Flask: A micro web framework for Python
-   Redis: An in-memory data structure store used for caching
-   Celery: A distributed task queue for scheduling tasks
-   Mailhog: A simple mail server for testing mailing services

### Requirements

-   Node.js and npm (for building and running the Vue.js frontend)
-   Python 3 and pip (for running the Flask backend)
-   Redis (for caching)
-   Celery (for scheduling tasks)
-   MailHog (For testing mail services)

### Installation

1.  Clone the repository: `git clone https://github.com/shetkarneeraj/BlogLite.git`
2.  Navigate to the Vue App directory: `cd BlogLite/app`
3.  Install the frontend dependencies: `npm install`
4.  Navigate to the API directory: `cd BlogLite/api`
5.  Install the backend dependencies: `./run_api.sh`
6.  Start the Celery beats: `celery_beats.sh`
7.  Start the Celery worker: `celery_worker.sh`
8.  Activate Virtual Environment: `source ./venv/bin/activate`
9.  Navigate to the Vue App directory: `cd BlogLite/app`
10.  Start the Vue development server: `npm run serve`
11. Run MailHog Server: `~/go/bin/MailHog`

## Deployment

To deploy BlogLite to a production environment, you can use a web server like Nginx or Apache and set up a reverse proxy to the Flask application.

### Usage

Once the installation and setup is complete, open your browser and navigate to `http://localhost:8080`. You will be prompted to register or login. Once logged in, you can create, edit and view posts, search for other users' posts, and comment and like on posts. You can also schedule post publishing by setting a specific date and time for the post to be published.
