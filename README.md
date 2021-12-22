# ubademy.service.courses
[![codecov](https://codecov.io/gh/Ubademy/ubademy.service.courses/branch/master/graph/badge.svg?token=WOM0ZAP02J)](https://codecov.io/gh/Ubademy/ubademy.service.courses) [![Tests](https://github.com/Ubademy/ubademy.service.courses/actions/workflows/test.yml/badge.svg)](https://github.com/Ubademy/ubademy.service.courses/actions/workflows/test.yml) [![Linters](https://github.com/Ubademy/ubademy.service.courses/actions/workflows/linters.yml/badge.svg)](https://github.com/Ubademy/ubademy.service.courses/actions/workflows/linters.yml) [![Deploy](https://github.com/Ubademy/ubademy.service.courses/actions/workflows/deploy.yml/badge.svg)](https://github.com/Ubademy/ubademy.service.courses/actions/workflows/deploy.yml)

This is courses microservice.

## Technologies

* [FastAPI](https://fastapi.tiangolo.com/)
* [SQLAlchemy](https://www.sqlalchemy.org/)
* [Poetry](https://python-poetry.org/)
* [Docker](https://www.docker.com/)
* [Heroku](https://www.heroku.com/)

## Architecture

Directory structure (based on [Onion Architecture](https://jeffreypalermo.com/2008/07/the-onion-architecture-part-1/)):

```tree
├── main.py
├── app
│   ├── domain
│   │   ├── content
│   │   │   └── content_exception.py
│   │   ├── course
│   │   │   ├── course.py
│   │   │   ├── course_exception.py
│   │   │   └── course_repository.py
│   │   └── user
│   │       └── user_exception.py
│   ├── infrastructure
│   │   ├── course
│   │   │   ├── course_dto.py               # DTO using SQLAlchemy
│   │   │   ├── course_query_service.py     # Query service implementation
│   │   │   └── course_repository.py        # Repository implementation
│   │   └── database.py
│   ├── presentation
│   │   └── schema
│   │       ├── content
│   │       │   └── content_error_message.py
│   │       ├── course
│   │       │   └── course_error_message.py
│   │       └── user
│   │           └── user_error_message.py
│   └── usecase
│       ├── content
│       │   ├── content_command_model.py    # Write and Update models
│       │   └── course_query_model.py       # Read model
│       ├── course
│       │   ├── course_command_model.py     # Write and Update models
│       │   ├── course_command_usecase.py
│       │   ├── course_query_model.py       # Read model
│       │   ├── course_query_service.py     # Query service interface
│       │   └── course_query_usecase.py
│       └── user
│           ├── user_command_model.py       # Write and Update models
|           ├── user_query_model.py         # Read model
│           └── user_query_usecase.py
└── tests
```

## Build
``` bash
docker-compose build    # Build app

make build              # Destroys DB and then builds
```

## Run
``` bash
make run
```

Access api swagger at: http://127.0.0.1:8000/docs#/

## Tests
``` bash
make test
```

## Reformat
``` bash
make fmt
```

## Lint
``` bash
make lint
```
