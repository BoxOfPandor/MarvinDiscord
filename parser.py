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

        current_test = None
        error_message = None

        for i, line in enumerate(content):
            line = line.strip()

            if not line:
                continue

            # Détecter un groupe de tests (contient "tests" à la fin)
            if " tests" in line:
                self.current_group = line.split(" tests")[0].strip()
                continue

            # Pour les traces finales (OK/KO)
            if self.is_final_trace and ":" in line and any(status in line for status in ["OK", "KO"]):
                test_name = line.split(":")[0].strip()
                status = "OK" if "OK" in line else "KO"

                # Récupérer le message d'erreur si KO
                if status == "KO":
                    error_lines = []
                    j = i + 1
                    while j < len(content) and content[j].strip() and not content[j].strip().endswith(": OK") and not content[j].strip().endswith(": KO"):
                        error_lines.append(content[j].strip())
                        j += 1
                    error_message = "\n".join(error_lines)

                if self.current_group:
                    test_name = f"{self.current_group} / {test_name}"

                self.results[test_name] = {
                    "name": test_name,
                    "passed": 100 if status == "OK" else 0,
                    "crashed": 0,
                    "failed": 0 if status == "OK" else 100,
                    "error": error_message if status == "KO" else None
                }
                continue

            # Pour les traces daily (pourcentages)
            if not self.is_final_trace:
                if line.endswith(':') and not line.startswith(' '):
                    current_test = line[:-1]
                    continue

                if line.startswith('Passed:') and current_test:
                    passed_line = line.split(':')[1].strip().replace(' %', '')
                    next_line = next((l for l in content if 'Crashed:' in l), '')
                    crashed_line = next_line.split(':')[1].strip().replace(' %', '')

                    try:
                        passed = float(passed_line)
                        crashed = float(crashed_line)
                        failed = 100 - passed - crashed

                        self.results[current_test] = {
                            "name": current_test,
                            "passed": passed,
                            "crashed": crashed,
                            "failed": failed
                        }
                    except ValueError:
                        continue

    def format_for_discord(self):
        discord_message = f"📝 **Résultats des tests automatiques - {self.project_name}**\n\n"

        current_category = None
        for test_name, test_data in self.results.items():
            # Gérer les catégories
            category = test_name.split(" / ")[0] if " / " in test_name else test_name
            if category != current_category:
                current_category = category
                discord_message += f"\n**{category}**\n"

            # Formater le résultat du test
            passed = test_data['passed']
            emoji = "✅" if passed == 100 else "⚠️" if test_data.get('crashed', 0) > 0 else "❌"
            test_display_name = test_name.split(" / ")[-1] if " / " in test_name else test_name

            discord_message += f"🔹 {test_display_name} - {emoji} "
            if self.is_final_trace:
                discord_message += "OK" if passed == 100 else "KO"
                if test_data.get('error'):
                    discord_message += f"\n```{test_data['error']}```"
            else:
                discord_message += f"{passed:.0f}% Passed"
                if test_data.get('crashed', 0) > 0:
                    discord_message += f" ({test_data['crashed']:.0f}% Crashed)"

            discord_message += "\n"

        return discord_message.strip()

# Test du parser
if __name__ == "__main__":
    parser = TestResultParser("trace.txt")
    parser.parse()
    print(parser.format_for_discord())