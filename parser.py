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
    
            # Détecter un groupe de tests
            if " tests" in line and not line.startswith("    "):
                current_group = line.split(" - ")[0].strip()
                # Ajouter le groupe lui-même dans les résultats
                self.results[current_group] = {
                    "name": line,
                    "passed": 100 if "OK" in line else 0,
                    "crashed": 0,
                    "failed": 0 if "OK" in line else 100,
                    "error": None,
                    "is_group": True
                }
                i += 1
                continue
    
            # Détecter un test individuel
            if line.startswith("    ") and (": OK" in line or ": KO" in line) and not line.startswith("      Test failure:"):
                test_name = line.strip()
                status = "OK" if ": OK" in line else "KO"
                
                full_test_name = f"{current_group} / {test_name}"
                self.results[full_test_name] = {
                    "name": test_name,
                    "passed": 100 if status == "OK" else 0,
                    "crashed": 0,
                    "failed": 0 if status == "OK" else 100,
                    "error": None,
                    "is_group": False
                }
    
            # Si c'est un module sans tests individuels (comme Build status)
            elif not line.startswith("    ") and ": " in line and ("OK" in line or "KO" in line):
                status = "OK" if "OK" in line else "KO"
                self.results[line] = {
                    "name": line,
                    "passed": 100 if status == "OK" else 0,
                    "crashed": 0,
                    "failed": 0 if status == "OK" else 100,
                    "error": None,
                    "is_group": False
                }
    
            i += 1
    
    def format_for_discord(self):
        discord_message = f"📝 **Résultats des tests automatiques - {self.project_name}**\n"
    
        current_group = None
        for test_name, test_data in self.results.items():
            if test_data.get("is_group", False):
                if current_group != test_name:
                    current_group = test_name
                    discord_message += f"\n\n**{test_data['name']}**"
            elif "/" in test_name:  # C'est un sous-test
                test_display_name = test_name.split(" / ")[1]
                passed = test_data['passed']
                emoji = "✅" if passed == 100 else "⚠️" if test_data.get('crashed', 0) > 0 else "❌"
                discord_message += f"🔹 {test_display_name} {emoji}\n"
            else:  # C'est un test standalone (comme Build status)
                if not test_name.startswith("Test failure"):
                    emoji = "✅" if test_data['passed'] == 100 else "❌"
                    discord_message += f"\n**{test_data['name']}** {emoji}"
    
        return discord_message.strip()

# Test du parser
if __name__ == "__main__":
    parser = TestResultParser("trace.txt")
    parser.parse()
    print(parser.format_for_discord())