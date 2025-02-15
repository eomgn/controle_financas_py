## Criar o Ambiente Virtual

### Linux
```sh
python3 -m venv venv
```

### Windows
```sh
python -m venv venv
```

## Ativar o Ambiente Virtual

### Linux
```sh
source venv/bin/activate
```

### Windows
```sh
venv\Scripts\Activate
```

## Caso algum comando retorne um erro de permissão, execute o código abaixo e tente novamente:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

## Instalação das Bibliotecas Necessárias
```sh
pip install sqlmodel
pip install matplotlib
