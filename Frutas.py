import json
import os

# En esta clase se utiliza el atributo __dict__ del objeto
# Y se agrega un Json de mas de 1000 elementos a dicha propiedad
# Así evitamos generar un modelo con mas de 1000 atributos en codigo
# se puede acceder a un elemento del json cargado en el __dict__ usando el mismo atributo al llamarlo
class Frutas:
    def __init__(self):
        with open(self.file(), 'r', encoding="utf-8") as file:
            contenido = file.read()
        self.__dict__.update(json.loads(contenido))

    # Ruta del archivo, en caso de actualzarlo o mandarlo llamar al inicializar el objeto
    def file(self):
        return f'{os.getcwd()}/Json/Frutas.json'

    # Metodo para convertir el objeto en el archivo Json de origen de datos, en caso de modificaciones
    def dictToJson(self):
        json_str = json.dumps(self.__dict__, indent=4, ensure_ascii=False)
        with open(self.file(), 'w', encoding="utf-8") as file:
            file.write(json_str)