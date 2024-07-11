from neo4j import GraphDatabase
from fastapi import APIRouter
from models.models import Node

router = APIRouter()

# URI examples: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"
URI = "neo4j+s://68558f39.databases.neo4j.io"
AUTH = ("neo4j", "VPQtRVplG-LixSUaPd8EK9HKfF8-5g-wMF6z2av_4Mo")

#Retorna la conexion de la DB
def connection():
    driver=GraphDatabase.driver(URI, auth=AUTH)
    return driver

#Query return count nodes
@router.get("/")
async def count_nodes():
    driver_neo4j=connection()
    session=driver_neo4j.session()
    result= session.run("MATCH (n) RETURN count(n) AS NodeCount")
    node_count = result.single()["NodeCount"]
    driver_neo4j.close() #Close Connection
    return {"node_count":node_count}

#Method Post nodes
@router.post("/create")
async def create_node(node: Node):
    driver_neo4j=connection()
    session=driver_neo4j.session()
    query=""" create(n:Persona{name:$name, edad:$edad, actividad:$actividad, gusto1:$gusto1 ,gusto2:$gusto2 ,disguto:$disgusto}) """

    #Organizing the data
    data={"name":node.name, "edad":node.edad, "actividad":node.actividad, 
          "gusto1":node.gusto1,"gusto2":node.gusto2, "disgusto":node.disgusto}
    
    #Send Query to the database
    results=session.run(query,data)

    session.close()
    driver_neo4j.close() #Close Connection

@router.put("/update")
async def update_node(node: Node):
    driver_neo4j=connection()
    session=driver_neo4j.session()
    query= """ match(n:Persona{id:$node.id}) set n.name=$name, return n.name as name """

    data={"name": node.name}
    results= session.run(query,data)

@router.delete("/delete/{name}")
async def delete_node(name: str):
    driver_neo4j=connection()
    session=driver_neo4j.session()
    query=""" match(n:Persona{name:$name}) delete n"""

    data={"name":name}

    session.run(query,data)
    session.close()
    driver_neo4j.close()
    return("Node drop sucessful")

#Query For Search all nodes with the atribute Estudiantes
@router.get("/students")
async def search_students():
    driver_neo4j=connection()
    session=driver_neo4j.session()
    query= """ MATCH (p:Persona{actividad:"Estudiante"}) RETURN p """

    result= session.run(query)
    estudiantes = [record["p"] for record in result]

    session.close()
    driver_neo4j.close()

    return{"estudiantes": estudiantes}