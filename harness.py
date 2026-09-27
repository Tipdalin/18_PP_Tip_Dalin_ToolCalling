from pydantic import ValidationError

from schemas import (
    SearchPhoneInput,
    CheckStockInput,
    DeletePhoneInput,
)

from tools import (
    search_phone,
    check_stock,
    delete_phone,
)

#check max tool call
MAX_TOOL_CALLS = 3

PERMISSIONS = {
    "customer": {
        "search_phone",
        "check_stock",
    },
    "admin": {
        "search_phone",
        "check_stock",
        "delete_phone",
    },
}

class Harness:
    def __init__(self, role: str = "customer"):
        self.role = role.lower()
        self.tool_calls = 0

    def check_permission(self, tool_name: str):
        """
        Check whether the current role can use the tool.
        """

        allowed_tools = PERMISSIONS.get(self.role, set())

        if tool_name not in allowed_tools:
            return {
                "allowed": False,
                "error": "PERMISSION_DENIED",
                "message": (
                    f"Role '{self.role}' is not allowed "
                    f"to use '{tool_name}'."
                ),
            }

        return {
            "allowed": True,
        }

    def check_limit(self):
        """
        Prevent an endless agent loop.
        """

        if self.tool_calls >= MAX_TOOL_CALLS:
            return {
                "allowed": False,
                "error": "TOOL_CALL_LIMIT",
                "message": (
                    f"Maximum tool call limit of "
                    f"{MAX_TOOL_CALLS} reached."
                ),
            }

        return {
            "allowed": True,
        }

    def execute_tool(self, tool_name: str, arguments: dict):
        """
        Validate, authorize, and execute a tool.
        """

        limit_result = self.check_limit()

        if not limit_result["allowed"]:
            return limit_result

        permission_result = self.check_permission(tool_name)

        if not permission_result["allowed"]:
            return permission_result

        try:

            if tool_name == "search_phone":

                validated = SearchPhoneInput(**arguments)

                result = search_phone(
                    validated.query
                )

            elif tool_name == "check_stock":

                validated = CheckStockInput(**arguments)

                result = check_stock(
                    validated.phone_id
                )

            elif tool_name == "delete_phone":

                validated = DeletePhoneInput(**arguments)

                result = delete_phone(
                    validated.phone_id
                )

            else:

                return {
                    "success": False,
                    "error": "UNKNOWN_TOOL",
                    "message": f"Unknown tool: {tool_name}",
                }

        except ValidationError as e:

            return {
                "success": False,
                "error": "VALIDATION_ERROR",
                "message": str(e),
            }

        except Exception as e:

            return {
                "success": False,
                "error": "TOOL_EXECUTION_ERROR",
                "message": str(e),
            }

        self.tool_calls += 1

        return result

