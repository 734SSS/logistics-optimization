from src.route_checker import route_cost


def swap_route(route, i, j):

    new_route = route.copy()

    new_route[i], new_route[j] = new_route[j], new_route[i]

    return new_route


def local_search(
    route,
    customers,
    mesafe_np,
    seyahat_süresi_np
):

    best_route = route.copy()

    best_cost = route_cost(
        best_route,
        customers,
        mesafe_np,
        seyahat_süresi_np
    )

    improved = True

    while improved:

        improved = False

        for i in range(1, len(best_route) - 1):

            for j in range(i + 1, len(best_route) - 1):

                new_route = swap_route(
                    best_route,
                    i,
                    j
                )

                new_cost = route_cost(
                    new_route,
                    customers,
                    mesafe_np,
                    seyahat_süresi_np
                )

                if new_cost < best_cost:

                    best_cost = new_cost
                    best_route = new_route
                    improved = True

    return best_route, best_cost




def greedy_routes(
    delivery,
    pickup,
    customers,
    mesafe_np,
    seyahat_süresi_np
):

    unvisited = delivery + pickup

    routes = []
    route = [0]

    current_time = 0
    current_node = 0

    while len(unvisited) > 0:

        feasible_customers = []

        # Uygun müşterileri bul
        for i in range(len(unvisited)):

            node = unvisited[i]

            travel_time = seyahat_süresi_np[current_node, node]

            arrival_time = current_time + travel_time

            earliest_time = customers[node]["arr"]

            if earliest_time > arrival_time:
                waiting_time = earliest_time - arrival_time
            else:
                waiting_time = 0

            service_start = arrival_time + waiting_time

            if service_start > customers[node]["due"]:
                print(node, "uygun değil")

            else:
                print(node, "uygun")
                feasible_customers.append(node)

        print("Uygun müşteriler:", feasible_customers)

        # Hiç uygun müşteri yoksa mevcut rotayı bitir
        if not feasible_customers:

            route.append(0)
            routes.append(route)

            route = [0]
            current_node = 0
            current_time = 0

            continue

        # Uygun müşteriler arasından en yakını seç
        best_distance = float("inf")
        best_node = None

        for node in feasible_customers:

            if mesafe_np[current_node, node] < best_distance:

                best_distance = mesafe_np[current_node, node]
                best_node = node

        # Seçilen müşteriye git
        travel_time = seyahat_süresi_np[current_node, best_node]

        arrival_time = current_time + travel_time

        earliest_time = customers[best_node]["arr"]

        if earliest_time > arrival_time:
            waiting_time = earliest_time - arrival_time
        else:
            waiting_time = 0

        service_start = arrival_time + waiting_time

        service_time = customers[best_node]["service"]

        current_time = service_start + service_time

        current_node = best_node

        route.append(best_node)

        unvisited.remove(best_node)

    # Son rotayı kaydet
    route.append(0)
    routes.append(route)

    return routes