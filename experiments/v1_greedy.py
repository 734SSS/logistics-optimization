from src.data_loader import load_data
from src.greedy import greedy_routes
from src.route_checker import check_route


def run_v1():

    customers, mesafe_np, seyahat_süresi_np, delivery, pickup = load_data()

    routes = greedy_routes(
        delivery,
        pickup,
        customers,
        mesafe_np,
        seyahat_süresi_np
    )

    print("\n==============================")
    print("V1 GREEDY SONUCU")
    print("==============================")

    print("Rotalar:")
    print(routes)

    all_visited = []

    for route in routes:

        for node in route:

            if node != 0:
                all_visited.append(node)

    print("\nZiyaret edilen:", len(all_visited))
    print("Farklı:", len(set(all_visited)))

    all_customers = set(delivery + pickup)
    visited_customers = set(all_visited)

    print("Eksik:", all_customers - visited_customers)
    print(
        "Fazla/tekrar:",
        len(all_visited) - len(set(all_visited))
    )

    print("\n==============================")
    print("ROTA KONTROLLERİ")
    print("==============================")

    for route in routes:

        result = check_route(
            route,
            customers,
            mesafe_np,
            seyahat_süresi_np
        )

        print("\nROTA:", route)
        print("Sonuç:", result)


if __name__ == "__main__":
    run_v1()