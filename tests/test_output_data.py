from routing.models import OutputData, Route
import json


def test_output_data_from_json():
    test_data_dict = json.loads(test_data_json)
    output_data = OutputData(**test_data_dict)

    assert output_data.total_delivery_duration == 4891
    assert len(output_data.routes) == 3


def test_route():
    route1 = Route()
    route1.append_job(1, 1000)
    route1.append_job(4, 1000)
    route1.append_job(2, 1000)

    assert len(route1.jobs) == 3
    assert route1.delivery_duration == 3000

    empty_route = Route()
    assert len(empty_route.jobs) == 0
    assert empty_route.delivery_duration == 0


def test_output_data():
    output_data = OutputData()

    route1 = Route()
    route1.append_job(1, 1000)
    route1.append_job(4, 1000)
    route1.append_job(2, 1000)
    output_data.add_route(1, route1)

    route2 = Route()
    route2.append_job(3, 100)
    route2.append_job(5, 100)
    route2.append_job(6, 100)
    output_data.add_route(2, route2)

    route3 = Route()
    output_data.add_route(3, route3)

    assert output_data.total_delivery_duration == 3300
    assert len(output_data.routes) == 3


test_data_json = """
{
    "total_delivery_duration": 4891,
    "routes": {
        "1": {
            "jobs": [
                "1",
                "4",
                "2"
            ],
            "delivery_duration": 3047
        },
        "2": {
            "jobs": [
                "3",
                "5",
                "6"
            ],
            "delivery_duration": 844
        },
        "3": {
            "jobs": [],
            "delivery_duration": 0
        }
    }
}
"""
