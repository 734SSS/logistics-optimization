import pandas as pd


def load_data():

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

    mesafe_np = mesafe.to_numpy()
    seyahat_süresi_np = seyahat_süresi.to_numpy()

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

    delivery = []
    pickup = []

    for i in customers.keys():

        if customers[i]["type"] == "Delivery":
            delivery.append(i)

        elif customers[i]["type"] == "Pickup":
            pickup.append(i)
    
    return customers, mesafe_np, seyahat_süresi_np, delivery, pickup

data=load_data()