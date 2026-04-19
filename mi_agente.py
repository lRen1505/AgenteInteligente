"""
mi_agente.py — Aquí defines tu agente.
╔══════════════════════════════════════════════╗
║  ✏️  EDITA ESTE ARCHIVO                      ║
╚══════════════════════════════════════════════╝

Tu agente debe:
    1. Heredar de la clase Agente
    2. Implementar el método decidir(percepcion)
    3. Retornar: 'arriba', 'abajo', 'izquierda' o 'derecha'

Lo que recibes en 'percepcion':
───────────────────────────────
percepcion = {
    'posicion':       (3, 5),          # Tu fila y columna actual
    'arriba':         'libre',         # Qué hay arriba
    'abajo':          'pared',         # Qué hay abajo
    'izquierda':      'libre',         # Qué hay a la izquierda
    'derecha':        None,            # None = fuera del mapa

    # OPCIONAL — brújula hacia la meta.
    # No es percepción real del entorno, es información global.
    # Usarla hace el ejercicio más fácil. No usarla es más realista.
    'direccion_meta': ('abajo', 'derecha'),
}

Valores posibles de cada dirección:
    'libre'  → puedes moverte ahí
    'pared'  → bloqueado
    'meta'   → ¡la meta! ve hacia allá
    None     → borde del mapa, no puedes ir

Si tu agente retorna un movimiento inválido (hacia pared o
fuera del mapa), simplemente se queda en su lugar.
"""

from entorno import Agente


class MiAgente(Agente):
    """
    Tu agente de navegación.

    Implementa el método decidir() para que el agente
    llegue del punto A al punto B en el grid.
    """

    def __init__(self):
        super().__init__(nombre="Mi Agente")
        self.visitadas = {}
        self.ultima_posicion = None

    def al_iniciar(self):
        self.visitadas = {}
        self.ultima_posicion = None
        

    def siguiente_posicion(self,posicion,accion):
        dr,dc = self.DELTAS[accion]
        return(posicion[0]+dr,posicion[1]+dc)

    def decidir(self, percepcion):
        
        """
        Decide la siguiente acción del agente.
        
        Parámetros:
            percepcion – diccionario con lo que el agente puede ver

        Retorna:
            'arriba', 'abajo', 'izquierda' o 'derecha'
        """
        posicion = percepcion["posicion"]
        vert, horiz = percepcion['direccion_meta']
        
        # Registrar visita actual
        self.visitadas[posicion] = self.visitadas.get(posicion, 0) + 1

        # 1. Si la meta está al lado, ir directo
        for accion in self.ACCIONES:
            if percepcion[accion] == "meta":
                self.ultima_posicion = posicion
                return accion

        # 2. Movimientos válidos
        movimientos_validos = [
            accion for accion in self.ACCIONES
            if percepcion[accion] in ("libre", "meta")
        ]

        if not movimientos_validos:
            return "abajo"

        # 3. Evaluar cada acción
        mejor_accion = None
        mejor_puntaje = float("-inf")

        for accion in movimientos_validos:
            nueva_pos = self.siguiente_posicion(posicion, accion)
            visitas = self.visitadas.get(nueva_pos, 0)

            puntaje = 0

            # Priorizar dirección hacia la meta
            if accion == vert:
                puntaje += 3
            if accion == horiz:
                puntaje += 3

            # Preferir celdas menos visitadas
            puntaje -= visitas * 2

            # Penalizar volver inmediatamente atrás
            if nueva_pos == self.ultima_posicion:
                puntaje -= 4

            if puntaje > mejor_puntaje:
                mejor_puntaje = puntaje
                mejor_accion = accion

        self.ultima_posicion = posicion
        return mejor_accion if mejor_accion else "abajo"