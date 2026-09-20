# =========================
# 1. Kütüphaneler
# =========================

import pandas as pd
import numpy as np


# =========================
# 2. Verileri yükleme
# =========================

özellikler = pd.read_csv(
    r"C:\Users\emirs\Desktop\#1 optimizasyon\data\Section3_real_case_data.csv"
)

mesafe = pd.read_csv(
    r"C:\Users\emirs\Desktop\#1 optimizasyon\data\real_case_distance_matrix.csv",
    header=None
)

seyahat_süresi = pd.read_csv(
    r"C:\Users\emirs\Desktop\#1 optimizasyon\data\real_case_time_matrix.csv",
    header=None
)


# =========================
# 3. NumPy matrislerine çevirme
# =========================

mesafe_np = mesafe.to_numpy()
seyahat_süresi_np = seyahat_süresi.to_numpy()


# =========================
# 4. Müşteri bilgilerini sözlükte tutma
# =========================

customers = {}

for index, row in özellikler.iterrows():

    node_id = row["id"]

    customers[node_id] = {
        "type": row["stop_type"],
        "weight": row["weight"],
        "service": row["Stop Duration"],
        "arr": row["Arr"],
        "due": row["Due"]
    }


# =========================
# 5. Delivery / Pickup listeleri
# =========================

delivery = []
pickup = []

for i in customers.keys():

    if customers[i]["type"] == "Delivery":
        delivery.append(i)

    elif customers[i]["type"] == "Pickup":
        pickup.append(i)


# =========================
# 6. Kontroller
# =========================

print("Toplam node:", len(customers))
print("Delivery:", len(delivery))
print("Pickup:", len(pickup))

print(customers[13])
print(customers[14])

print("0 → 13:", seyahat_süresi_np[0, 13])
print("13 → 14:", seyahat_süresi_np[13, 14])

# =========================
# 7. Rota zaman kontrolü
# =========================


def check_route(route):
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


def route_cost(route):
    result = check_route(route)

    feasible = result[0]
    total_distance = result[3]

    if feasible:
        return total_distance
    else:
        return float("inf")

    

route = [0, 13, 14, 29, 26, 28, 31, 0]

cost = route_cost(route)

print(cost)

route2 = [0, 13, 14, 29, 26, 31, 28, 0]

cost1 = route_cost(route)

cost2 = route_cost(route2)

print("cost1:", cost1)
print("cost2:", cost2)



def swap_route(route, i, j):
    new_route = route.copy()

    new_route[i],new_route[j]=new_route[j],new_route[i]

    return new_route


route = [0, 13, 14, 29, 26, 28, 31, 0]

new_route = swap_route(route, 5, 6)
new_cost = route_cost(new_route)
old_cost = route_cost(route)

print("Eski maliyet:", old_cost)
print("Yeni maliyet:", new_cost)

print("-----------------------------------------------------------------")


def local_search(route):
    

    best_route = route
    best_cost = route_cost(route)

    improved = True

    while improved:
        improved = False

        for i in range(1, len(best_route) - 1):
            for j in range(i + 1, len(best_route) - 1):

                new_route = swap_route(best_route, i, j)
                new_cost = route_cost(new_route)

                if new_cost < best_cost:
                    best_cost = new_cost
                    best_route = new_route
                    improved = True

    return best_route, best_cost


best_route, best_cost = local_search(route)

print("En iyi rota:", best_route)
print("En iyi maliyet:", best_cost)



routes = [
    [0, 53, 56, 54, 51, 57, 42, 0],
    [0, 55, 15, 2, 16, 17, 18, 19, 20, 21, 22, 24, 23, 27, 52, 30, 0],
    [0, 44, 47, 45, 46, 43, 50, 49, 25, 59, 48, 0],
    [0, 33, 32, 37, 36, 34, 35, 38, 39, 40, 41, 58, 0],
    [0, 13, 14, 29, 26, 28, 31, 0]
]

print("-----------------------------------------------------------------")
for route in routes:
    result = check_route(route)
    print(result)

print("gggggggggggggggggggggggggggggggggggggggggggggggggggggggggg")

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

        # Müşteriye ulaşmak için gereken seyahat süresi
        travel_time = seyahat_süresi_np[current_node, node]

        # Müşteriye varış zamanı
        arrival_time = current_time + travel_time

        # Müşterinin en erken servis zamanı
        earliest_time = customers[node]["arr"]

        # Bekleme süresi
        if earliest_time > arrival_time:
            waiting_time = earliest_time - arrival_time
        else:
            waiting_time = 0

        # Servisin başlayacağı zaman
        service_start = arrival_time + waiting_time

        # Due kontrolü
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
    best_distance = float('inf')
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


# WHILE BİTTİ
# Son rotayı da kaydet
route.append(0)
routes.append(route)


print(routes)


all_visited = []

for route in routes:
    for node in route:
        if node != 0:
            all_visited.append(node)

print("Ziyaret edilen:", len(all_visited))
print("Farklı:", len(set(all_visited)))

all_customers = set(delivery + pickup)
visited_customers = set(all_visited)

print("Eksik:", all_customers - visited_customers)
print("Fazla/tekrar:", len(all_visited) - len(set(all_visited)))



for route in routes:
    print("\nROTA:", route)

    result = check_route(route)

    print("Sonuç:", result)