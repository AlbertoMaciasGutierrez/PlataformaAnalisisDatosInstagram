# PlataformaAnalisisDatosInstagram

Pequeña aplicación web para la recopilación de datos de cuentas y publicaciones de Instagram desarrollada en Django 4.0.3 y Python 3.8.9

## Instalación 
Primero clonamos el repositorio (también podemos descargar el repositorio en formato ZIP):

```  
git clone https://github.com/AlbertoMaciasGutierrez/PlataformaAnalisisDatosInstagram.git  
```

Una vez descargado el repositorio debemos de instalar los paquetes de python necesitados en nuestro entorno virtual:  

```  
pip install -r requirements.txt  
```
  ---
## Ejecución del proyecto
Para poder ejecutar el proyecto es necesario crear un archivo llamado ***".env"*** donde se introducen las credenciales de la cuenta de Instagram por defecto que va a usar la aplicación para recopilar la información. Para crear este hay que seguir el modelo descrito en el archivo ***"env.example.txt"***.

Una vez llegado a este punto es necesario descomentar varias líneas que se encuentran al principio del archivo ***"datosUsuarioInstagram/instaloader_funciones.py"*** tal que así:
```  
USER = config('INSTAGRAM_USER')
PASS = config('INSTAGRAM_PASS')

INSTAGRAM = 'https://www.instagram.com/'
POST = 'p/'
HIGHLIGHT = 'stories/highlights/'



L = Instaloader()
L.login(USER,PASS)                            #Loguearse
L.save_session_to_file()                      #Guardar sesión en archivo para no tener que volver a loguearnos
#L.load_session_from_file(USER)                 #Carga la sesión guardada del inicio de sesión anterior.
```   

Accediendo dentro del directorio del proyecto al mismo nivel que se encuentra el documento "manage.py", abrimos un terminal, creamos las migraciones y migramos los modelos a la base de datos con estos dos comandos:
```  
python manage.py makemigrations  
```   

```  
python manage.py migrate  
```   

Una vez realizadas las migraciones volvemos a comentar las líneas descomentadas en el archivo ***"datosUsuarioInstagram/instaloader_funciones.py"***  ya que nuestro sistema ya habrá guardado la sesión iniciada de Instagram.
```
USER = config('INSTAGRAM_USER')
#PASS = config('INSTAGRAM_PASS')

INSTAGRAM = 'https://www.instagram.com/'
POST = 'p/'
HIGHLIGHT = 'stories/highlights/'



L = Instaloader()
#L.login(USER,PASS)                            #Loguearse
#L.save_session_to_file()                      #Guardar sesión en archivo para no tener que volver a loguearnos
L.load_session_from_file(USER)                 #Carga la sesión guardada del inicio de sesión anterior.
```
Por último lanzamos la aplicación con el siguiente comando:
```
python manage.py runserver --insecure 0.0.0.0:8000
```
Para acceder a la aplicación debemos acceder a la dirección http://127.0.0.1:8000/analisisInsta/
