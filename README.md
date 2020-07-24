# Workshop IFS Sample Solution

This is my sample solution for [Hacking the Home Assignment](https://github.com/yulkes/PublicSpeaking/tree/master/HackingTheHomeAssignment) 
example home assignment.

It follows the guidelines listed during the workshop and in my book.

## Introduction

This is IFS, an Insecure Filesystem operated over a REST API.

It supports the following endpoints:
* `GET /fs/<path>` : Return a JSON response structured as:
        ```
        {"success": true, 
         "fs": {"filename": "<path from request>", 
                "dirs": ["dir1", ...], 
                "files": ["a", ...]}}
        ```
* `DELETE /fs/<path>` : Delete the file or directory at `<path>`.
* `PUT /fs/<path>` with body `{name: "<new path>"}` : Move the file at `<path>` to `<new path>`. 

The service will prevent accessing files and directories outside the root scope it's defined on in `BASE_PATH` configuration variable.

## Quick Start

Run the application in Docker:

    make run_docker

You can also run it locally:
    
    make run

And open it in the browser at [http://127.0.0.1:5000/fs](http://127.0.0.1:5000/fs) (Per the assignment's specs)

### Other commands:
`make test` - Will run all unit and integration tests

`make end_to_end_test` - Start a Docker container with an example directory structure and run E2E tests tha delete and move files. 

`make zip` - Generate a Zip file with only the relevant files, ready for submission and review.

## Prerequisites

This is built to be used with Python 3.8, and uses a Virtual Environment for installing dependencies.

The E2E tests require Docker to be installed.

## Components

The web-app is Flask app, with one Blueprint for the filesystem access.

The Filesystem Blueprint is in `ifs/filesystem`, and contains the following files:
* `models.py`: Domain object for the requests and responses of the filesystem service
* `fs.py`: An interface `AbstractFileSystemService` and implementation for clean filesystem access.
* `views.py`:` Flask routes that adapt between incoming parameters and the models for the Filesystem service's API.


## Development environment and release process

 - create virtualenv with Flask and development dependencies: `make .venv`

 - run development server in debug mode: `make run`; Flask will restart if source code is modified

 - run tests: `make test`

 - create source submission: `make zip` (will run tests first, and will only include required files)

 - to remove virtualenv and built distributions: `make clean`

 - to add more python dependencies: add to `requirements.txt`

 - to modify configuration in development environment: edit file `settings.cfg`
