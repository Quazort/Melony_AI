import sys

from celery.signals import setup_logging, worker_ready, worker_process_init

from core.logger import get_logger
from workers.celery_config import app


def main():
    argv = [
        'worker',
        '--loglevel=info',
    ]
    if sys.platform == 'win32':
        argv.extend(['-P', 'solo'])
    else:
        argv.extend(['-c', '2'])
    app.worker_main(argv=argv)


@worker_process_init.connect
def init_worker_logger(*args, **kwargs):
    get_logger("celery-worker")

@worker_ready.connect
def on_worker_ready(*args, **kwargs):
    logger = get_logger("celery-worker")
    logger.info("Селери загружен")


@setup_logging.connect
def setup_celery_logger(*args, **kwargs):
    get_logger("celery-worker")
    return


if __name__ == "__main__":
    main()
