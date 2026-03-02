from app.api.fast_api import run_app
from environment_printer import EnvironmentPrinter


if __name__ == "__main__":
    EnvironmentPrinter.print_environment_variables()
    app = run_app()
