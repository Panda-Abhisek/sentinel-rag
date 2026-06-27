import logging

LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format=LOG_FORMAT,
        force=True,
    )

    noisy_loggers = (
        "httpx",
        "huggingface_hub",
        "sentence_transformers",
    )

    for logger_name in noisy_loggers:
        logging.getLogger(logger_name).setLevel(logging.WARNING)