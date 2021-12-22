import logging

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.usecase.course import CourseQueryUseCase
from app.usecase.metrics.category_metrics_query_model import (
    PaginatedCategoryMetricsReadModel,
)
from app.usecase.metrics.new_courses_metrics_query_model import (
    NewCoursesMetricsReadModel,
)
from app.usecase.metrics.subscriptions_metrics_query_model import (
    SubscriptionMetricsReadModel,
)

from .dependencies import course_query_usecase

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get(
    "/courses/metrics/categories",
    response_model=PaginatedCategoryMetricsReadModel,
    status_code=status.HTTP_200_OK,
    tags=["metrics"],
)
async def get_category_metrics(
    limit: int = 10,
    query_usecase: CourseQueryUseCase = Depends(course_query_usecase),
):
    try:
        metrics, count = query_usecase.get_category_metrics(limit=limit)

    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return PaginatedCategoryMetricsReadModel(categories=metrics, count=count)


@router.get(
    "/courses/metrics/courses",
    response_model=NewCoursesMetricsReadModel,
    status_code=status.HTTP_200_OK,
    tags=["metrics"],
)
async def get_new_courses_metrics(
    year: int = None,
    query_usecase: CourseQueryUseCase = Depends(course_query_usecase),
):
    try:
        metrics = query_usecase.get_course_metrics(year=year)

    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return metrics


@router.get(
    "/courses/metrics/subscriptions",
    response_model=SubscriptionMetricsReadModel,
    status_code=status.HTTP_200_OK,
    tags=["metrics"],
)
async def get_subscriptions_metrics(
    query_usecase: CourseQueryUseCase = Depends(course_query_usecase),
):
    try:
        metrics = query_usecase.get_subscription_metrics()

    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return metrics
