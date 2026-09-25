from ortools.constraint_solver import (
    pywrapcp,
    routing_enums_pb2
)

from src.data_loader import load_data
from src.ortools_solver import create_model


def run():

    # -------------------------
    #       VERİLERİ YÜKLE
    # -------------------------

    customers, distance_matrix, time_matrix, delivery, pickup = load_data()

    # -------------------------
    #        MODELİ OLUŞTUR
    # -------------------------

    manager, routing = create_model(
        customers,
        distance_matrix,
        time_matrix,
        delivery,
        pickup
    )

    # Time dimension
    time_dimension = routing.GetDimensionOrDie("Time")

    # -------------------------
    #     ARAMA PARAMETRELERİ
    # -------------------------

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()

    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION
    )

    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    )

    search_parameters.time_limit.seconds = 30

    search_parameters.log_search = True

    # -------------------------
    #          ÇÖZ
    # -------------------------

    solution = routing.SolveWithParameters(
        search_parameters
    )

    # -------------------------
    #      ÇÖZÜM KONTROLÜ
    # -------------------------

    if solution:

        routes = []

        print("Çözüm bulundu!")
        print(f"Objective: {solution.ObjectiveValue()}")

        # -------------------------
        #      ROTALARI ÇIKAR
        # -------------------------

        for vehicle_id in range(routing.vehicles()):

            if not routing.IsVehicleUsed(solution, vehicle_id):
                continue

            # Başlangıç ve bitiş indexleri
            start_index = routing.Start(vehicle_id)
            end_index = routing.End(vehicle_id)

            index = start_index

            route = []
            route_distance = 0

            # -------------------------
            #       ROTA OLUŞTUR
            # -------------------------

            while not routing.IsEnd(index):

                node = manager.IndexToNode(index)

                next_index = solution.Value(
                    routing.NextVar(index)
                )

                next_node = manager.IndexToNode(next_index)

                # Mesafeyi hesapla
                route_distance += distance_matrix[node][next_node]

                # Node'u rotaya ekle
                route.append(node)

                # Bir sonraki node'a geç
                index = next_index

            # Depot'a dönüşü ekle
            route.append(
                manager.IndexToNode(index)
            )

            # -------------------------
            #       ROTA SÜRESİ
            # -------------------------

            start_time = solution.Value(
                time_dimension.CumulVar(start_index)
            )

            end_time = solution.Value(
                time_dimension.CumulVar(end_index)
            )

            route_time = end_time - start_time

            # -------------------------
            #       SONUÇLARI KAYDET
            # -------------------------

            routes.append({
                "vehicle_id": vehicle_id,
                "route": route,
                "distance": route_distance,
                "time": route_time
            })

            # -------------------------
            #          YAZDIR
            # -------------------------

            print(
                f"Araç {vehicle_id}: "
                + " -> ".join(map(str, route))
            )

            print(
                f"Mesafe: {route_distance}"
            )

            print(
                f"Süre: {route_time}"
            )

        # -------------------------
        #     TOPLAM MESAFE
        # -------------------------

        total_distance = sum(
            route["distance"]
            for route in routes
        )

        # -------------------------
        #       TOPLAM SÜRE
        # -------------------------

        total_time = sum(
            route["time"]
            for route in routes
        )

        # -------------------------
        #      ARAÇ SAYISI
        # -------------------------

        vehicles_used = len(routes)

        print(
            f"Toplam mesafe: {total_distance}"
        )

        print(
            f"Toplam süre: {total_time}"
        )

        print(
            f"Kullanılan araç sayısı: {vehicles_used}"
        )

        # -------------------------
        #        SONUÇLAR
        # -------------------------

        return {
            "objective": solution.ObjectiveValue(),
            "routes": routes,
            "total_distance": total_distance,
            "total_time": total_time,
            "vehicles_used": vehicles_used
        }

    else:

        print("Çözüm bulunamadı.")

        return None