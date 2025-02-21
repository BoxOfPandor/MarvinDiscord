class TestResultParser:
    def __init__(self, file_path, project_name="Unknown Project"):
        self.file_path = file_path
        self.project_name = project_name
        self.results = {}
        self.current_group = None
        self.is_final_trace = "Final" in file_path
        
    def extract_project_name(self):
            """Extrait le nom du projet depuis la première ligne du fichier."""
            try:
                with open(self.file_path, 'r', encoding='utf-8') as file:
                    first_line = file.readline().strip()
                    if first_line:
                        self.project_name = first_line
            except Exception as e:
                print(f"Erreur lors de l'extraction du nom du projet: {str(e)}")

    def parse(self):
        self.extract_project_name()
        
        with open(self.file_path, 'r', encoding='utf-8') as file:
            content = file.readlines()
    
        current_group = None
        i = 0
        while i < len(content):
            line = content[i].strip()
    
            if not line:
                i += 1
                continue
    
            # Détecter un groupe principal (avec "tests")
            if " tests" in line and not line.startswith("    "):
                current_group = line
                self.results[current_group] = {
                    "name": line,
                    "passed": 0,
                    "crashed": 0,
                    "failed": 0,
                    "error": None,
                    "is_group": True,
                    "tests": []  # Ajout d'une liste pour stocker les tests du groupe
                }
                i += 1
                continue
    
            # Détecter un test individuel qui appartient à un groupe
            if " - " in line and not line.startswith("    "):
                status = "OK" if "OK" in line else "KO"
                test_data = {
                    "name": line,
                    "passed": 100 if status == "OK" else 0,
                    "crashed": 0,
                    "failed": 0 if status == "OK" else 100,
                    "error": None,
                    "is_group": False
                }
                
                # Si nous sommes dans un groupe, ajouter le test à ce groupe
                if current_group and current_group in self.results:
                    self.results[current_group]["tests"].append(test_data)
                else:
                    # Sinon, c'est un test standalone
                    self.results[line] = test_data

            i += 1

    def format_for_discord(self):
        """Formate les résultats des tests pour l'affichage Discord."""
        
        # En-tête du message
        message_parts = [
            f"📝 **Résultats des tests automatiques - {self.project_name}**"
        ]
        
        # Traitement des tests standalone (comme Build status)
        standalone_tests = [
            (name, data) for name, data in self.results.items() 
            if not data.get("is_group") and not isinstance(data.get("tests"), list)
        ]
        for name, data in standalone_tests:
            if not name.startswith("Test failure"):
                emoji = "✅" if data['passed'] == 100 else "❌"
                message_parts.append(f" -  {name} {emoji}")
    
        # Formatage des groupes et leurs tests
        for name, group_data in self.results.items():
            if group_data.get("is_group"):
                # En-tête du groupe
                message_parts.append(f"\n**{group_data['name']}**")
                
                # Tests du groupe
                for test in group_data.get("tests", []):
                    emoji = "✅" if test['passed'] == 100 else "⚠️" if test.get('crashed', 0) > 0 else "❌"
                    message_parts.append(f"🔹 {test['name']} {emoji}")
    
        # Assemblage du message final
        return "\n".join(message_parts)

# Test du parser
if __name__ == "__main__":
    parser = TestResultParser("trace.txt")
    parser.parse()
    print(parser.format_for_discord())