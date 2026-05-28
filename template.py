import os
import argparse

def template_report(path_glob: str, path:str, namefile: str)-> None:
    template_report = f"""#{namefile}

## Description de la vulnérabilité
Decrire la vulnérabilité

## Méthode d'exploitation
Decrire la methode d'exploitation

## Remédiation
Decrire la remediation
"""

    with open(f"{path}/{namefile}.md", "w") as f:
        f.write(template_report)
    print(f"Template repport '{path}/{namefile}.md' created successfully.")

    with open(f"{path_glob}/flag", "w") as f:
        f.write("[replace flag here]")
    print(f"Template flag created successfully.")


def create_folders(directory_name: str) -> None:
    """
    Creation du template
    Une dossier avec le bon nom et les fichiers de bases
    """
    try:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        directory_path = f"{dir_path}/{directory_name}"
        ressources_path = f"{directory_path}/Resources"
        os.mkdir(directory_name)
        os.mkdir(ressources_path)
        print(f"Directory '{directory_name}' created successfully.")
        template_report(directory_path, ressources_path, "README")
    except FileExistsError:
        print(f"Directory '{directory_name}' already exists.")
    except PermissionError:
        print(f"Permission denied: Unable to create '{directory_name}'.")

def main():
    """
    Main fonction where you ask for a vulnerability name.
    """
    parser = argparse.ArgumentParser(
                    prog='Template_generator',
                    description='This script generate a template for the vuln.')
    parser.add_argument('-n',
                        '--name',
                        type=str,
                        help='Name you want to use for the template',
                        nargs=1)
    args = parser.parse_args()
    if args.name:
        create_folders(args.name[0])
    else:
        print("Wrong usage need name for template folder")


if __name__ == "__main__":
    main()
