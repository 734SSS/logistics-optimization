from ortools.constraint_solver import (
    pywrapcp,
    routing_enums_pb2
)


DEPOT = 0
NUM_VEHICLES = 7


def create_model(
    customers,
    distance_matrix,
    time_matrix,
    delivery,
    pickup
):

    num_nodes = len(customers)

    manager = pywrapcp.RoutingIndexManager(
        num_nodes,
        NUM_VEHICLES,
        DEPOT
    )

    routing = pywrapcp.RoutingModel(manager)


    # -------------------
    #       Mesafe
    # -------------------

    def distance_callback(from_index, to_index):

        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)

        distance = distance_matrix[from_node, to_node]

        return int(round(distance))


    distance_callback_index = (
        routing.RegisterTransitCallback(distance_callback)
    )

    routing.SetArcCostEvaluatorOfAllVehicles(
        distance_callback_index
    )


    # -------------------
    #        Yük
    # -------------------

    def delivery_demand_callback(from_index):

        from_node = manager.IndexToNode(from_index)

        if customers[from_node]["type"] == "Delivery":
            return int(customers[from_node]["weight"])

        return 0


    delivery_demand_index = (
        routing.RegisterUnaryTransitCallback(
            delivery_demand_callback
        )
    )


    routing.AddDimensionWithVehicleCapacity(
        delivery_demand_index,
        0,
        [37000] * NUM_VEHICLES,
        True,
        "DeliveryCapacity"
    )


    # -------------------
    #       Pick Up
    # -------------------

    def pickup_demand_callback(from_index):

        from_node = manager.IndexToNode(from_index)

        if customers[from_node]["type"] == "Pickup":
            return int(customers[from_node]["weight"])

        return 0


    pickup_demand_index = (
        routing.RegisterUnaryTransitCallback(
            pickup_demand_callback
        )
    )


    routing.AddDimensionWithVehicleCapacity(
        pickup_demand_index,
        0,
        [37000] * NUM_VEHICLES,
        True,
        "PickupCapacity"
    )


        # -------------------
    #       Backhaul
    # -------------------

    def backhaul_callback(from_index, to_index):

        to_node = manager.IndexToNode(to_index)

        if customers[to_node]["type"] == "Pickup":
            return 1

        return 0

    backhaul_index = routing.RegisterTransitCallback(
        backhaul_callback
    )

    routing.AddDimension(
        backhaul_index,
        0,
        len(pickup),
        True,
        "BackhaulOrder"
    )

    backhaul_dimension = routing.GetDimensionOrDie(
        "BackhaulOrder"
    )


    for node in delivery:

        index = manager.NodeToIndex(node)

        backhaul_dimension.CumulVar(index).SetRange(
            0,
            0
        )

    for node in pickup:

        index = manager.NodeToIndex(node)

        backhaul_dimension.CumulVar(index).SetRange(
            1,
            len(pickup)
        )

    # -------------------
    #    Time Dimension
    # -------------------

    def time_callback(from_index, to_index):

        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)

        travel_time = time_matrix[from_node, to_node]

        service_time = customers[from_node]["service"]

        return int(
            round(travel_time + service_time)
        )


    time_callback_index = (
        routing.RegisterTransitCallback(
            time_callback
        )
    )


    routing.AddDimension(
        time_callback_index,
        28800,
        28800,
        False,
        "Time"
    )


    time_dimension = routing.GetDimensionOrDie(
        "Time"
    )


    for node in customers:

        index = manager.NodeToIndex(node)

        arr = customers[node]["arr"]
        due = customers[node]["due"]

        time_dimension.CumulVar(index).SetRange(
            int(arr),
            int(due)
        )


    # -------------------
    #    Araç Zamanı
    # -------------------

    for vehicle_id in range(NUM_VEHICLES):

        start_index = routing.Start(vehicle_id)
        end_index = routing.End(vehicle_id)

        time_dimension.CumulVar(
            start_index
        ).SetRange(
            0,
            28800
        )

        time_dimension.CumulVar(
            end_index
        ).SetRange(
            0,
            28800
        )


    return manager, routing