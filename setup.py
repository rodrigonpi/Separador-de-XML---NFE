from cx_Freeze import setup, Executable

# Nome do seu aplicativo
nome_app = "Organizador NFe"
versao = "1.0"
descricao = "Move arquivos de NFe onde tpNF == 0"

# Configura o executável
executavel = Executable(
    script="move_nfe.py",          # seu script principal
    base="Win32GUI",              # não abre janela de terminal
    icon="icone.ico"              # ícone opcional
)

# Setup do instalador
setup(
    name=nome_app,
    version=versao,
    description=descricao,
    executables=[executavel],
    options={
        "build_exe": {
            "packages": ["os", "shutil", "xml", "tkinter", "customtkinter"],
            "include_files": ["icone.ico"]
        },
        "bdist_msi": {
            "upgrade_code": "{9A2F3B99-2A9F-4B82-AF08-37DE857D2D8C}",  # GUID única
            "add_to_path": False,
            "initial_target_dir": r"[ProgramFilesFolder]\OrganizadorNFe"
        }
    }
)
