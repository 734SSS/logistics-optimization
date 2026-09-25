import numpy as np
def check_route(route, customers, mesafe_np, seyahat_süresi_np):

    current_time = 0
    total_waiting = 0
    route_feasible = True
    total_distance = 0

    for i in range(len(route) - 1):

        current_node = route[i]
        next_node = route[i + 1]

        travel_time = seyahat_süresi_np[current_node, next_node]

        total_distance += mesafe_np[current_node, next_node]

        print(current_node, "->", next_node, ":", travel_time)

        current_time += travel_time

        # Eğer bir sonraki düğüm depo ise
        if next_node == 0:

            if current_time > customers[0]["due"]:
                print("Depoya dönüş zamanı aşıldı!")
                route_feasible = False

            continue

        # Müşterinin en erken servis zamanı
        earliest_time = customers[next_node]["arr"]

        waiting_time = earliest_time - current_time

        if waiting_time > 0:
            print("bekleme süresi:", waiting_time)
            current_time += waiting_time
            total_waiting += waiting_time

        service_start = current_time

        # Müşteri zaman penceresi kontrolü
        if service_start > customers[next_node]["due"]:
            print("Zaman penceresi ihlali!")
            route_feasible = False
            break

        service_time = customers[next_node]["service"]

        current_time += service_time

    return route_feasible, current_time, total_waiting, total_distance


def route_cost(route, customers, mesafe_np, seyahat_süresi_np):

    result = check_route(
        route,
        customers,
        mesafe_np,
        seyahat_süresi_np
    )

    feasible = result[0]
    total_distance = result[3]

    if feasible:
        return total_distance

    return float("inf")