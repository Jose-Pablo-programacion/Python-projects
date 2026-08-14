import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import json

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)



schema = {
    "required" : [
        "pregunta",
        "opcion_a",
        "opcion_b",
        "opcion_c",
        "opcion_d",
        "respuesta_correcta",
    ], 
    "properties" : {
        "pregunta" : {"type" : "STRING"},
        "opcion_a" : {"type" : "STRING"},
        "opcion_b" : {"type" : "STRING"},
        "opcion_c" : {"type" : "STRING"},
        "opcion_d" : {"type" : "STRING"},
        "respuesta_correcta" : {"type" : "STRING"},
    },
    "type" : "OBJECT" ,  
}

response = client.models.generate_content(
    model ='gemini-3-flash-preview',
    contents = "Hazme una pregunta de 4 opciones sobre estructuras de datos en python",
    config = types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema = schema,
    ),
)
print(response.text)

pregunta_diccionario = json.loads(response.text)
print(pregunta_diccionario)
print(pregunta_diccionario["pregunta"])

print(
    f"a) {pregunta_diccionario["opcion_a"]}",
    f"b) {pregunta_diccionario["opcion_b"]}",
    f"c) {pregunta_diccionario["opcion_c"]}",
    f"d) {pregunta_diccionario["opcion_d"]}",
    sep="\n"
    )

respuesta_usuario = input("Cual es la opcion correcta: ")

if respuesta_usuario.lower() == pregunta_diccionario["respuesta_correcta"]:
    print("Correcto!")
else:
    print("Incorrecto")#cambiar a un while para qeu mientras se la saque mal, que lo deje volverr a intentar
