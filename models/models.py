from pydantic import BaseModel

class Node(BaseModel):
    id: int
    name: str
    edad: int
    actividad: str
    gusto1: str
    gusto2: str
    disgusto: str
    defuncion: str