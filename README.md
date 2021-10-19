# ubademy.service.pytemplate
[![codecov](https://codecov.io/gh/Ubademy/ubademy.service.courses/branch/master/graph/badge.svg?token=T726IGKKWO)](https://codecov.io/gh/Ubademy/ubademy.service.courses) [![Tests](https://github.com/Ubademy/ubademy.service.courses/actions/workflows/test.yml/badge.svg)](https://github.com/Ubademy/ubademy.service.courses/actions/workflows/test.yml) [![Linters](https://github.com/Ubademy/ubademy.service.courses/actions/workflows/linters.yml/badge.svg)](https://github.com/Ubademy/ubademy.service.courses/actions/workflows/linters.yml) [![Deploy](https://github.com/Ubademy/ubademy.service.courses/actions/workflows/deploy.yml/badge.svg)](https://github.com/Ubademy/ubademy.service.courses/actions/workflows/deploy.yml)

This is a template repository for a REST api on python.

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
│   │   └── course
│   │       ├── course.py  # Entity
│   │       ├── course_exception.py  # Exception definitions
│   │       └── course_repository.py  # Repository interface
│   ├── infrastructure
│   │   └── sqlite
│   │       ├── course
│   │       │   ├── course_dto.py  # DTO using SQLAlchemy
│   │       │   ├── course_query_service.py  # Query service implementation
│   │       │   └── course_repository.py  # Repository implementation
│   │       └── database.py
│   ├── presentation
│   │   └── schema
│   │       └── course
│   │           └── course_error_message.py
│   └── usecase
│       └── course
│           ├── course_command_model.py  # Write models including schemas of the RESTFul API
│           ├── course_command_usecase.py
│           ├── course_query_model.py  # Read models including schemas
│           ├── course_query_service.py  # Query service interface
│           └── course_query_usecase.py
└── tests
```

## Run
``` bash
docker-compose build

docker-compose up
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
