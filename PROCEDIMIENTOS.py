import requests

API_KEY = "EwJEKKiCHUrO3W9R2TkJwbtL25VpQooc"

# Lista de monedas válidas (puedes ampliarla)
MONEDAS_VALIDAS = ["USD", "EUR", "MXN", "GBP", "JPY", "CAD", "AUD", "CHF"]


def convertir_moneda(origen, destino, cantidad):
    url = f"https://api.apilayer.com/exchangerates_data/convert?from={origen}&to={destino}&amount={cantidad}&apikey={API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        datos = response.json()

        if datos.get("success", True) is False:
            print("Error de la API:", datos.get("error"))
            return

        resultado = datos.get("result")
        if resultado is not None:
            print(f"\n{cantidad} {origen} equivalen a {resultado:.2f} {destino}")
        else:
            print("\nNo se pudo realizar la conversión. Respuesta completa:")
            print(datos)

    except requests.exceptions.RequestException as e:
        print("Error al consultar el servicio:", e)


def main():
    print("=== Conversor de Monedas ===")
    print("Monedas válidas:", ", ".join(MONEDAS_VALIDAS))

    while True:
        origen = input("\nIngresa la moneda de origen (por ejemplo USD, EUR) o 'salir' para terminar: ").upper()
        if origen == "SALIR":
            break
        if origen not in MONEDAS_VALIDAS:
            print("Moneda inválida. Intenta de nuevo.")
            continue

        destino = input("Ingresa la moneda de destino: ").upper()
        if destino not in MONEDAS_VALIDAS:
            print("Moneda inválida. Intenta de nuevo.")
            continue

        try:
            cantidad = float(input(f"Ingresa la cantidad de {origen} a convertir: "))
        except ValueErrCAMBIor:
            print("Cantidad inválida. Intenta de nuevo.")
            continue

        convertir_moneda(origen, destino, cantidad)


if _name_ == "_main_":
    main()