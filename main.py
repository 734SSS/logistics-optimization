from experiments.v2_ortools import run


def main():

    result = run()

    if result is None:
        print("Çözüm bulunamadı.")
        return

    print("\n")
    print("=" * 40)
    print("        OR-TOOLS SONUÇLARI")
    print("=" * 40)

    print(f"Objective       : {result['objective']}")
    print(f"Kullanılan araç : {result['vehicles_used']}")
    print(f"Toplam mesafe   : {result['total_distance']}")

    print("\nAraçlar:")

    for vehicle in result["routes"]:

        print(
            f"Araç {vehicle['vehicle_id']}: "
            f"{vehicle['distance']}"
        )

    print("=" * 40)


if __name__ == "__main__":
    main()