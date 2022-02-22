from pydantic import BaseSettings


class Settings(BaseSettings):
    """Settings for the vrp solver.

    Each option has a sensible default value,
    and they can be changed using `.env` file or environment variables.

    USE_SERVICE_TIME, enables addition of service time for all destinations (default: True)
    ORTOOLS_LOG_SEARCH, enables verbose logging (default: False)
    ORTOOLS_TIME_LIMIT, time limit in seconds (default: 30)


    """

    use_service_time: bool = True

    ortools_log_search: bool = False
    ortools_time_limit: int = 30

    class Config:
        env_file = ".env"


settings = Settings()
