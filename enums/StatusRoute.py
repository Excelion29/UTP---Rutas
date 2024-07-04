import enum

class StatusRoute(enum.Enum):
    pendiente = "pendiente"
    en_progreso = "en_progreso"
    completado = "completado"
    cancelado = "cancelado"