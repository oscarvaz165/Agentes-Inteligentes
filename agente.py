"""
Actividad 4 - Agente recolector (Agentes Inteligentes, Unidad II)
Ciclo: ENTORNO -> SENSORES -> PERCEPCION -> DECISION -> ACCION -> ACTUADORES -> ENTORNO
"""
import copy

MAX_ACCIONES = 50
DIRECCIONES = {            # orden fijo = orden de prioridad en empates
    "ARRIBA":    (-1, 0),
    "DERECHA":   (0, 1),
    "ABAJO":     (1, 0),
    "IZQUIERDA": (0, -1),
}

ESCENARIOS = {
    1: ["...P.",
        ".X...",
        "A..XP",
        "..P..",
        ".X..."],
    2: ["P.X..",
        "..X.P",
        "..A..",
        "X....",
        "P.X.."],
    3: [".X..P",
        ".X.X.",
        "..A..",
        "PX.X.",
        "....P"],
}


class Simulacion:
    def __init__(self, mapa, verbose=True):
        # ENTORNO: cuadrícula sin el agente (el agente se guarda aparte)
        self.entorno = []
        self.pos = None
        for i, fila in enumerate(mapa):
            f = []
            for j, c in enumerate(fila):
                if c == "A":
                    self.pos = [i, j]
                    c = "."
                f.append(c)
            self.entorno.append(f)
        self.total_paquetes = sum(f.count("P") for f in self.entorno)
        self.recogidos = 0
        self.movimientos = 0
        self.penalizaciones = 0
        self.puntuacion = 0
        self.acciones = 0
        self.verbose = verbose
        # MEMORIA INTERNA del agente (solo lo que ha percibido/visitado)
        self.visitas = {tuple(self.pos): 1}

    # ---------------- MEDIDA DE RENDIMIENTO ----------------
    def actualizar_rendimiento(self, evento):
        puntos = {"RECOGER": +10, "MOVER": -1, "FUERA": -5,
                  "OBSTACULO": -5, "TODO": +20}[evento]
        self.puntuacion += puntos
        if evento in ("FUERA", "OBSTACULO"):
            self.penalizaciones += 1

    # ---------------- SENSORES / PERCEPCION ----------------
    def _contenido(self, i, j):
        if not (0 <= i < len(self.entorno) and 0 <= j < len(self.entorno[0])):
            return "FUERA_DEL_TABLERO"
        return {".": "VACIA", "P": "PAQUETE", "X": "OBSTACULO"}[self.entorno[i][j]]

    def percibir(self):
        i, j = self.pos
        percepcion = {"posicion": (i, j), "actual": self._contenido(i, j)}
        for nombre, (di, dj) in DIRECCIONES.items():
            percepcion[nombre] = self._contenido(i + di, j + dj)
        return percepcion

    # ---------------- FUNCION DEL AGENTE (DECISION) ----------------
    def decidir(self, p):
        # Regla 1: si hay paquete en mi celda -> recoger
        if p["actual"] == "PAQUETE":
            return "RECOGER"
        # Regla 2: si hay paquete adyacente -> ir hacia él
        for d in DIRECCIONES:
            if p[d] == "PAQUETE":
                return d
        # Reglas 3 y 4: nunca ir a obstáculo ni fuera del tablero;
        # entre las direcciones seguras elegir la MENOS visitada
        i, j = p["posicion"]
        seguras = [d for d in DIRECCIONES if p[d] in ("VACIA", "PAQUETE")]
        if not seguras:
            return "RECOGER"   # Regla 5: atrapado, no hay movimiento valido
        def veces(d):
            di, dj = DIRECCIONES[d]
            return self.visitas.get((i + di, j + dj), 0)
        return min(seguras, key=veces)   # empate -> orden ARRIBA, DERECHA, ABAJO, IZQUIERDA

    # ---------------- ACTUADORES / ACCION ----------------
    def actuar(self, accion):
        i, j = self.pos
        if accion == "RECOGER":
            if self.entorno[i][j] == "P":
                self.entorno[i][j] = "."
                self.recogidos += 1
                self.actualizar_rendimiento("RECOGER")
                if self.recogidos == self.total_paquetes:
                    self.actualizar_rendimiento("TODO")
            return
        di, dj = DIRECCIONES[accion]
        ni, nj = i + di, j + dj
        contenido = self._contenido(ni, nj)
        if contenido == "FUERA_DEL_TABLERO":
            self.actualizar_rendimiento("FUERA")
        elif contenido == "OBSTACULO":
            self.actualizar_rendimiento("OBSTACULO")
        else:
            self.pos = [ni, nj]
            self.movimientos += 1
            self.actualizar_rendimiento("MOVER")
            self.visitas[(ni, nj)] = self.visitas.get((ni, nj), 0) + 1

    def quedan_paquetes(self):
        return self.recogidos < self.total_paquetes

    def mostrar_entorno(self):
        for i, fila in enumerate(self.entorno):
            print(" ".join("A" if [i, j] == self.pos else c for j, c in enumerate(fila)))
        print(f"Pos: {tuple(self.pos)} | Puntuación: {self.puntuacion}\n")

    def ejecutar(self):
        if self.verbose:
            print("Estado inicial:")
            self.mostrar_entorno()
        while self.quedan_paquetes() and self.acciones < MAX_ACCIONES:
            percepcion = self.percibir()          # PERCEPCIONES
            accion = self.decidir(percepcion)     # DECISIONES
            self.actuar(accion)                   # ACCIONES
            self.acciones += 1
            if self.verbose:
                print(f"Acción {self.acciones}: {accion}")
                self.mostrar_entorno()            # posición tras cada acción
        return (self.recogidos, self.total_paquetes, self.movimientos,
                self.penalizaciones, self.puntuacion, self.acciones)


if __name__ == "__main__":
    resumen = []
    for n, mapa in ESCENARIOS.items():
        print("=" * 30, f"ESCENARIO {n}", "=" * 30)
        r = Simulacion(mapa).ejecutar()
        resumen.append((n, r))
    print("\nRESUMEN")
    print("Esc | Paquetes | Movimientos | Penalizaciones | Puntuación | Acciones")
    for n, r in resumen:
        print(f" {n}  | {r[0]}/{r[1]}      | {r[2]:>3}         | {r[3]:>3}            | {r[4]:>4}       | {r[5]}")