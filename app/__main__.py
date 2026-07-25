from app.config import load_config
from app.server import run_server


def main() -> None:
    run_server(load_config())


if __name__ == "__main__":
    main()

