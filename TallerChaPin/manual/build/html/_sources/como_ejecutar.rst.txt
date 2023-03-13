==============================
⚙️ Cómo ejecutar la aplicación
==============================

***********
Instalación
***********

**Paso 1: clonar repositorio y crear entorno virtual**


| ``git clone https://github.com/UNPSJB/TallerChaPin``
| ``cd TallerChaPin``
| ``python -m venv <venv>``


**Paso 2: activar entorno virtual e instalar requerimientos**


Para activar venv, se debe ejecutar uno de los siguientes comandos, dependiendo el sistema operativo y el shell utilizado

+---------+-----------------+------------------------------------+
| SO      | Shell           | Comando                            |
+=========+=================+====================================+
| POSIX   | bash/zsh        | $ source <venv>/bin/activate       |
+---------+-----------------+------------------------------------+
|         | fish            | $ source <venv>/bin/activate.fish  |
+---------+-----------------+------------------------------------+
|         | csh/tcsh        | $ source <venv>/bin/activate.csh   |
+---------+-----------------+------------------------------------+
|         | PowerShell Core | $ <venv>/bin/Activate.ps1          |
+---------+-----------------+------------------------------------+
| Windows | cmd.exe         | C:> <venv>\Scripts\activate.bat    |
+---------+-----------------+------------------------------------+
|         | PowerShell      | PS C:> <venv>\Scripts\Activate.ps1 |
+---------+-----------------+------------------------------------+

Para instalar los requerimientos, utilizar

| ``pip install -r requirements.txt``

**Paso 3: establecer SECRET_KEY**

Ejecutar

| ``echo "SECRET_KEY=<contraseña>" > .env``

**Paso 4: ejecutar la aplicación y aplicar migraciones**


| ``cd TallerChaPin``
| ``python manage.py runserver``
| ``python manage.py migrate``

*********************************
Ejecución luego de la instalación
*********************************

Una vez realizados los pasos mencionados (1 al 4), la próxima vez que se quiera iniciar la aplicación solo se debe activar el entorno virtual y luego ejecutar el comando: 

| ``python manage.py runserver``
| Luego de esto el sistema ya estará en funcionamiento.