import logging


def get_logger(name: str = "k8s_self_service_platform") -> logging.Logger:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )
    return logging.getLogger(name)

