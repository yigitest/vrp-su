from .models import InputData
from .settings import settings


from typing import Dict, List, Tuple
from copy import deepcopy
import logging

logger = logging.getLogger("routing")


class OrToolsDataModel:
    """Data module class for ortools solver"""

    def __init__(
        self,
        num_nodes: int,
        num_vehicles: int,
        distance_matrix: List[List[int]],
        service_time: List[int],
        vehicle_starts: List[int],
        vehicle_ends: List[int],
        vehicle_capacities: List[int],
        node_demands: List[int],
        node_to_job_id_map: Dict[int, int],
    ):
        self.num_nodes = num_nodes
        self.num_vehicles = num_vehicles
        self.distance_matrix = distance_matrix
        self.service_time = service_time
        self.vehicle_starts = vehicle_starts
        self.vehicle_ends = vehicle_ends
        self.vehicle_capacities = vehicle_capacities
        self.node_demands = node_demands
        self.node_to_job_id_map = node_to_job_id_map


def create_ortools_data_model(input_data: InputData) -> OrToolsDataModel:
    """Converts raw input data to a more useful format for ortools vrp solver."""
    try:
        num_nodes, distance_matrix, service_time = _prep_distance_matrix(input_data)

        dummy_end_node_id = num_nodes - 1

        num_vehicles, vehicle_starts, vehicle_ends, vehicle_capacities = _prep_vehicles(
            input_data, dummy_end_node_id
        )

        node_demands = _prep_demands(num_nodes, input_data)

        node_to_job_id_map = _prep_location_to_job_map(input_data)

        return OrToolsDataModel(
            num_nodes,
            num_vehicles,
            distance_matrix,
            service_time,
            vehicle_starts,
            vehicle_ends,
            vehicle_capacities,
            node_demands,
            node_to_job_id_map,
        )
    except:
        logger.exception("Failed to create data model for ortools!")
        return None


def _prep_distance_matrix(
    input_data: InputData,
) -> Tuple[int, List[List[int]], List[int]]:
    """prepares distance matrix and service_time array

    vehicles are allowed to end at arbitrary locations. To set up the problem this way,
    simply modify the distance matrix so that distance to the dummyEndNode from any other
    location is 0.
    """
    distance_matrix = deepcopy(input_data.matrix)
    n = len(distance_matrix)

    # Add dummyEndNode's own row and distance to other nodes (all 0).
    for row in distance_matrix:
        row.append(0)  # from all other nodes to DummyEnd
    dummy_row = [0] * (n + 1)
    distance_matrix.append(dummy_row)  # from DummyEnd to all other

    # Add service time of jobs at the locations
    service_time = [0] * (n + 1)
    if settings.use_service_time:
        for job in input_data.jobs:
            service_time[job.location_index] += job.service

    print(service_time)
    return len(distance_matrix), distance_matrix, service_time


def _prep_vehicles(
    input_data: InputData, dummy_end_node_id: int
) -> Tuple[int, List[int], List[int], List[int]]:
    """prepares num_vehicle, start_positions, end_positions and capacities arrays for vehicles"""

    start_positions = [v.start_index for v in input_data.vehicles]
    end_positions = [dummy_end_node_id] * len(start_positions)
    # TODO capacity is an array!
    capacities = [sum(v.capacity) for v in input_data.vehicles]

    return len(input_data.vehicles), start_positions, end_positions, capacities


def _prep_demands(num_nodes: int, input_data: InputData) -> List[int]:
    """prepares node_demand array by iterating over all jobs

    FIXME multiple job's location_index can point to same node
    """
    node_demands = [0] * num_nodes
    for job in input_data.jobs:
        # TODO Job.delivery is an array! why?
        node_demands[job.location_index] += sum(job.delivery)
    return node_demands


def _prep_location_to_job_map(input_data: InputData):
    """prepares locationindex_to_jobid map

    FIXME multiple job's location_index can point to same node
    """
    node_location_to_job_id = {}
    for job in input_data.jobs:
        node_location_to_job_id[job.location_index] = job.id
    return node_location_to_job_id
