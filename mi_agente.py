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
        pass

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
        
        #Registramos la visita de la posicion actual
        if posicion not in self.visitadas:
            self.visitadas[posicion] = 0
            self.visitadas[posicion] += 1
   
        #Si la meta está al lado ir directamente  
        for accion in self.ACCIONES:
            if percepcion[accion] == "meta":
                self.ultima_posicion = posicion
                return accion
            
        #Obtener movimientos válidos
        movimientos_validos = []
        for accion in self.ACCIONES:
            if percepcion[accion] in ("libre", "meta"):
                movimientos_validos.append(accion)


        #Priorizar direcciones hacia la meta
        prioridades = []
        if vert != "ninguna":
            prioridades.append(vert)
        if horiz != "ninguna":
            prioridades.append(horiz)

        for accion in prioridades:
            if accion in movimientos_validos:
                nueva_pos = self.siguiente_posicion(posicion, accion)
        
        #Elegir la opción menos visitada
        mejor_accion = None
        menor_visitas = float("inf")

        for accion in movimientos_validos:
            nueva_pos = self.siguiente_posicion(posicion, accion)
            visitas = self.visitadas.get(nueva_pos, 0)

            if nueva_pos == self.ultima_posicion:
                continue

            if visitas < menor_visitas:
                menor_visitas = visitas
                mejor_accion = accion
        
        # 5. Si no hay otra opción, retroceder
        if mejor_accion is None and movimientos_validos:
            mejor_accion = movimientos_validos[0]

        self.ultima_posicion = posicion
        return mejor_accion if mejor_accion else "abajo"