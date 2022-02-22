from typing import List
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