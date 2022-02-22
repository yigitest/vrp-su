from lib2to3.pytree import Base
from typing import List, Dict
from pydantic import BaseModel


class Vehicle(BaseModel):
    id: int
    start_index: int
    capacity: List[int]


class Job(BaseModel):
    id: int
    location_index: int
    delivery: List[int]
    service: int


class InputData(BaseModel):
    vehicles: List[Vehicle]
    jobs: List[Job]
    matrix: List[List[int]]


class Route(BaseModel):
    delivery_duration: int = 0
    jobs: List[int] = []

    def append_job(self, job_id: int, duration: int):
        self.jobs.append(job_id)
        self.delivery_duration += duration


class OutputData(BaseModel):
    total_delivery_duration: int = 0
    routes: Dict[int, Route] = {}

    def add_route(self, vehicle_id: int, route: Route):
        self.routes[vehicle_id] = route
        self.total_delivery_duration += route.delivery_duration


class HTTPError(BaseModel):
    detail: str

    class Config:
        schema_extra = {
            "example": {"detail": "HTTPException raised."},
        }
