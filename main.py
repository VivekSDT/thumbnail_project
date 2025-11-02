import time
from multiprocessing import Queue
from producer_module import start_producer
from consumer_module import start_consumer
from config_loader import load_config
from logger_config import get_logger

log = get_logger("main")

def main():
    """Main entry point — sets up config, spawns producer & consumers."""
    cfg = load_config()

    queue = Queue()
    input_dir = cfg["producer_dir"]
    output_dir = cfg["consumer_dir"]

    num_consumers = cfg["num_consumers"]
    log.info(f"Starting Producer and {num_consumers} Consumer(s)...")

    start_time = time.time()

    # Start producer
    producer = start_producer(
        queue,
        input_dir,
        check_interval=cfg["check_interval"],
        idle_timeout=cfg["idle_timeout"],
        thumbnail_size=cfg["thumbnail_size"],
        batch_size=cfg["batch_size"]
    )

    # start consumer processes
    consumers = []
    for i in range(num_consumers):
        c = start_consumer(queue, output_dir, consumer_id=i + 1)
        consumers.append(c)

    # Wait for producer to finish
    producer.join()

    # signal each consumer to stop
    for _ in range(num_consumers):
        queue.put(None)

    # wait for consumers to finish
    for c in consumers:
        c.join()

    total_time = round(time.time() - start_time, 2)
    log.info(f"All processes finished in {total_time}s.")
    print(f"\nCheck '{output_dir}/' for thumbnails and 'process.log' for logs.\n")


if __name__ == "__main__":
    main()
