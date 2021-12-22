# ubademy.service.courses
[![codecov](https://codecov.io/gh/Ubademy/ubademy.service.courses/branch/master/graph/badge.svg?token=WOM0ZAP02J)](https://codecov.io/gh/Ubademy/ubademy.service.courses) [![Tests](https://github.com/Ubademy/ubademy.service.courses/actions/workflows/test.yml/badge.svg)](https://github.com/Ubademy/ubademy.service.courses/actions/workflows/test.yml) [![Linters](https://github.com/Ubademy/ubademy.service.courses/actions/workflows/linters.yml/badge.svg)](https://github.com/Ubademy/ubademy.service.courses/actions/workflows/linters.yml) [![Deploy](https://github.com/Ubademy/ubademy.service.courses/actions/workflows/deploy.yml/badge.svg)](https://github.com/Ubademy/ubademy.service.courses/actions/workflows/deploy.yml)

Courses microservice for [Ubademy](https://ubademy.github.io/)

This service manages:
* Course CRUD
* Course content
* Collaborators
* Reviews


For further information visit [Ubademy Courses](https://ubademy.github.io/services/courses)

Deployed at: [ubademy-service-courses](https://ubademy-service-courses.herokuapp.com/docs#) :rocket:



### Technologies

* [FastAPI](https://fastapi.tiangolo.com/)
* [SQLAlchemy](https://www.sqlalchemy.org/): PostgreSQL Database
* [Poetry](https://python-poetry.org/)
* [Docker](https://www.docker.com/)
* [Heroku](https://www.heroku.com/)

### Architecture

Directory structure (based on [Onion Architecture](https://jeffreypalermo.com/2008/07/the-onion-architecture-part-1/)):

```tree
├── main.py
├── routes
├── app
│   ├── domain
│   │   ├── collab
│   │   │   └── collab_exception.py
│   │   ├── content
│   │   │   └── content_exception.py
│   │   ├── course
│   │   │   ├── course.py
│   │   │   ├── course_exception.py
│   │   │   └── course_repository.py
│   │   └── review
│   │       ├── review.py
│   │       └── review_exception.py
│   ├── infrastructure
│   │   ├── course
│   │   │   ├── course_dto.py
│   │   │   ├── course_query_service.py
│   │   │   └── course_repository.py
│   │   └── database.py
│   ├── presentation
│   │   └── schema
│   │       ├── collab
│   │       │   └── collab_error_message.py
│   │       ├── content
│   │       │   └── content_error_message.py
│   │       ├── course
│   │       │   └── course_error_message.py
│   │       └── review
│   │           └── review_error_message.py
│   └── usecase
│       ├── collab
│       │   ├── collab_query_model.py
│       │   └── collab_query_usecase.py
│       ├── content
│       │   ├── content_command_model.py
│       │   └── course_query_model.py
│       ├── course
│       │   ├── course_command_model.py
│       │   ├── course_command_usecase.py
│       │   ├── course_query_model.py
│       │   ├── course_query_service.py
│       │   └── course_query_usecase.py
│       ├── metrics
│       │   ├── category_metrics_query_model.py
│       │   ├── new_courses_metrics_query_model.py
│       │   └── subscriptions_metrics_query_model.py
│       └── review
|           ├── review_command_model.py
│           └── review_query_model.py
└── tests
```

## Installation

### Dependencies:
* [python3.9](https://www.python.org/downloads/release/python-390/) and utils
* [Docker](https://www.docker.com/)
* [Docker-Compose](https://docs.docker.com/compose/)
* [Poetry](https://python-poetry.org/)

Once you have installed these tools, make will take care of the rest :relieved:

``` bash
make install
```

## Usage

### Run the API locally
``` bash
make run
```

### Reset Database and then run locally
``` bash
make reset
```

### Run format, tests and linters
``` bash
make checks
```

### Access API Swagger
Once the API is running you can check all available endpoints at [http://127.0.0.1:8000/docs#/](http://127.0.0.1:8000/docs#/)
