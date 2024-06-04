# Sprocket Corp. API

The Sprocket Corp. API is a RESTful API that allows consumers to interact with the Sprocket Corp. database. The API provides endpoints for managing locations, sprocket types, factories, and sprockets.
The API is built using the following tools and technologies:

- Python3.10
- FastAPI
- SQLAlchemy
- PostgreSQL
- Docker
- Docker Compose
- Pytest

## Assumptions

The following assumptions were made when designing the API:

- The corporation has multiple locations where sprockets are stored.
- Each location has a name, address, city, postal code, and country code (we're going global here).
- The corporation produces different types of sprockets.
- Each sprocket type has a name, number of teeth, pitch diameter, pitch, and outside diameter.
- The corporation has factories where sprockets are produced.
- When fetching the factory information along with the chart data, the chart data is a representation of 
when the factory was created and the sprocket production goal OR the sprocket production actual field changes for the factory.
This is to assume that we want to see the production goal or the actual production of the factory over time as either variable changes.


## API Endpoints
To view the endpoints, start the docker-compose environment locally and visit the Swagger UI at `http://localhost:8000/docs` in your browser. 
The Swagger UI provides a user-friendly interface for interacting with the API endpoints.


## Getting Started
To get started with the Sprocket Corp. API, follow the steps below:

1. Clone the repository:
2. Install Docker and Docker Compose
3. Run the following command to start the API:
   ```bash
   docker-compose up
   ```
4. SSH into the container to run the database migrations:
   ```bash
   docker exec api bash
   alembic -n devdb -c app/migrations/alembic.ini upgrade head
   
   # let's also update the "test" database
   alembic -n testdb -c app/migrations/alembic.ini upgrade head
   ```
5. Running the command in the previous step will create the database tables and seed the database with sample data. Namely,
It will create 3 locations and 3 sprocket types.
6. You can play around with the API by visiting `http://localhost:8000/docs` in your browser. This will
    open the Swagger UI where you can interact with the API endpoints.
7. I have also written some tests for the API. You can run the tests by running the following command:
    ```bash
    docker-compose exec api pytest
    ```
   This will run the tests and output the results in the terminal, along with the coverage report to stdout.

## Current Features
- The API provides endpoints for managing locations, sprocket types, factories, and sprockets.
- A consumer of the API can create, retrieve, update, and delete locations, sprocket types, factories, and sprockets.
- When a factory is created, the API automatically creates a chart for the factory. The chart data is a representation of when the factory was created and the sprocket production goal OR the sprocket production actual field changes for the factory.
- When a sprocket is created, the API will also add a chart entry for the corresponding factory. It matters that the factory exists before the sprocket is created, because we are tracking the production of each factory.
- API versioning, the API is versioned with a prefix of `/v1/` to ensure that the API is backwards compatible, should we need to make changes in the future and create various versions of the API.
- Swagger documentation, the API comes with built-in swagger documentation, which can be accessed at `http://localhost:8000/docs`.
- Tests, the API comes with tests that can be run by running the following command:
    ```bash
    docker-compose exec api pytest
    ```
    This will run the tests and output the results in the terminal, along with the coverage report to stdout. (Current coverage is at 94%)
- Ruff linter, the API comes with a linter that can be run by running the following command:
    ```bash
    docker-compose exec api ruff format
    ```
    This will run the linter and output the results in the terminal.
- Pagination for the sprocket types, sprockets, and factory endpoints. This is to ensure that the API responds in a prudent amount of time and reduces the likelihood of creating database locks.

## Future Improvements
Given more time, I would think about the following improvements:

- Initially, I tried to setup an environment where I could run the tests in a separate database container. However, I ran into some issues with it that took me longer than I had hoped, specifically with the test db connection when running tests. 
 I figured it would be best to move on and ensure that the API is functional and tested. Ideally, 
I would like to have a separate database container for testing purposes and one just for manual testing & local development. However, the tests are still running in the same database as the application. It doesn't hurt to also automatically
create some seed data by running the tests ;) (at least for this project).
- I would think about adding healthchecks. Especially in a distributed environment, it's important to know if the services are up and running.
- I would also secure the API with some form of authentication. I would probably use jwt tokens for this, and enforce that the token be passed along in the header to validate that 
the user is who they say they are AND that they are authorized to make such changes.
- If we were exposing this API to the public, I would also consider adding some form of logging. This is to ensure that we can track what is happening with the API and to help with debugging in the future.
    - I would also consider enforcing API keys for the API to ensure that only authorized consumers of the API get access.
- I would also consider adding some form of monitoring to the API. This is to ensure that we can track the performance of the API and to ensure that it is running smoothly.
- I would also add some form of rate limiting to the API. This is to prevent abuse of the API and to ensure that the API is available to all users.
- Add a CI Pipeline to the project. This is to ensure that the project is always in a deployable state and that the tests are always passing before deploying.
- I would add code quality scanners like Snyk, SonarQube, or CodeClimate to ensure that the code is of high quality and that we are following best practices.
- I would also consider adding a code coverage tool like Codecov to ensure that we are testing as many code paths in the application as possible.
- There are definitely some performance improvements to be made. I would consider another look at the database tables and analyze which queries are more read-heavy and which are more write-heavy. I would consider adding indexes to the read-heavy tables (first) to speed up the queries.
- I'm currently using a plaintext `.env` file for the environment variables. I would consider using a more secure method like AWS Secrets Manager or Hashicorp Vault to store the secrets. With kubernetes, you can deploy the secrets as environment variables to the pods.
- Unit tests, specifically for the `Factory.sprocket_production_actual` - the endpoint tests already test this indirectly, but it would be nice to always ensure that the function is working regardless of any consumers calling out to it.