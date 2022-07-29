# Taller ChaPin

Aplicación Django para gestión de taller de chapa y pintura

## Autores

- Barea, Matías
- Canario, Ramiro

## Proyecto

[Tablero](https://github.com/UNPSJB/TallerChaPin/projects/1)

## Instalar

```bash
git clone https://github.com/UNPSJB/TallerChaPin
cd TallerChaPin
python3 -m venv <venv>
source <venv>/bin/activate
pip install -r requirements.txt
```

### Activar venv

| Platform | Shell           | Command to activate virtual environment |
| -------- | --------------- | --------------------------------------- |
| POSIX    | bash/zsh        | $ source <venv>/bin/activate            |
|          | fish            | $ source <venv>/bin/activate.fish       |
|          | csh/tcsh        | $ source <venv>/bin/activate.csh        |
|          | PowerShell Core | $ <venv>/bin/Activate.ps1               |
| Windows  | cmd.exe         | C:\> <venv>\Scripts\activate.bat        |
|          | PowerShell      | PS C:\> <venv>\Scripts\Activate.ps1     |

## Configurar variables de entorno dotenv

```bash
cd TallerChaPin
echo "SECRET_KEY=..." > .env
```

## ¿Cómo ejecutar?

`python manage.py runserver`
