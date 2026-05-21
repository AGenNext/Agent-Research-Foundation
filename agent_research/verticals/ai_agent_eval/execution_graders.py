import json


class StructuredOutputGrader:
    def grade_json(self, output: str, required_fields: list[str]) -> dict:
        try:
            parsed = json.loads(output)
        except Exception:
            return {
                "success": False,
                "missing_fields": required_fields,
            }

        missing = [field for field in required_fields if field not in parsed]

        return {
            "success": len(missing) == 0,
            "missing_fields": missing,
        }


class ExecutionBasedGrader:
    def run_python_assertions(self, namespace: dict, assertions: list[str]):
        failures = []

        for assertion in assertions:
            try:
                exec(assertion, namespace)
            except Exception as e:
                failures.append(str(e))

        return {
            "success": len(failures) == 0,
            "failures": failures,
        }
