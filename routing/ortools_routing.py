from typing import Dict
import logging

from .models import InputData, OutputData, Route
from .ortools_data_model import OrToolsDataModel, create_ortools_data_model
from .settings import settings

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

logger = logging.getLogger("routing")


def solveOrtoolsRouting(input_data: InputData) -> OutputData:
    data = create_ortools_data_model(input_data=input_data)

    if not data:
        logger.error("Failed to create data model!")
        return None

    manager = pywrapcp.RoutingIndexManager(
        data.num_nodes, data.num_vehicles, data.vehicle_starts, data.vehicle_ends
    )

    routing = pywrapcp.RoutingModel(manager)

    # Add the distance callback

    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data.distance_matrix[from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add the demand callback and capacity constraints

    def demand_callback(from_index):
        """Returns the demand of the node."""
        # Convert from routing variable Index to demands NodeIndex.
        from_node = manager.IndexToNode(from_index)
        return data.node_demands[from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        data.vehicle_capacities,
        True,  # start cumul to zero
        "Capacity",
    )

    # Setting search parameters.

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )

    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.AUTOMATIC
    )

    search_parameters.log_search = settings.ortools_log_search
    search_parameters.time_limit.FromSeconds(settings.ortools_time_limit)

    ortools_solution = routing.SolveWithParameters(search_parameters)

    solution = _prepare_solution_output(
        input_data=input_data,
        data=data,
        manager=manager,
        routing=routing,
        ortools_solution=ortools_solution,
    )

    return solution


def _prepare_solution_output(
    input_data: InputData, data: OrToolsDataModel, manager, routing, ortools_solution
) -> OutputData:
    if ortools_solution:
        output_data = OutputData()

        # objective_value = ortools_solution.ObjectiveValue()
        for vehicle_index in range(data.num_vehicles):
            vehicle = input_data.vehicles[vehicle_index]
            route = Route()
            node_index = routing.Start(vehicle_index)

            while not routing.IsEnd(node_index):
                previous_node_index = node_index
                node_index = ortools_solution.Value(routing.NextVar(node_index))

                distance = routing.GetArcCostForVehicle(
                    previous_node_index, node_index, vehicle_index
                )

                # add node and distance value to Route
                # do not include dummy_end_node.
                node_id = manager.IndexToNode(node_index)
                job_id = data.node_to_job_id_map.get(node_id)
                if job_id:
                    route.append_job(job_id=job_id, duration=distance)

            output_data.add_route(vehicle_id=vehicle.id, route=route)

        return output_data

    else:
        # ortools failed to find any solution
        return None
