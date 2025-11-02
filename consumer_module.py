import os
from io import BytesIO
from PIL import Image
from multiprocessing import Process
from logger_config import get_logger

log = get_logger("consumer")


def consumer_task(queue, output_dir, consumer_id=1):
    """
    Reads thumbnail batches from the queue and writes them to disk.
    Multiple consumer setup.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    saved = 0
    log.info(f"Consumer-{consumer_id} started.")

    while True:
        batch = queue.get()
        if batch is None:
            log.info(f"Consumer-{consumer_id} exiting. Total saved: {saved}")
            break

        for file_name, img_bytes in batch:
            try:
                img = Image.open(BytesIO(img_bytes))
                name, _ = os.path.splitext(file_name)
                output_path = os.path.join(output_dir, f"{name}-thumbnail.jpg")
                img.save(output_path)
                saved += 1
                log.info(f"[Consumer-{consumer_id}] Saved: {output_path}")
            except Exception as e:
                log.error(f"[Consumer-{consumer_id}] Error saving {file_name}: {e}")


def start_consumer(queue, output_dir, consumer_id=1):
    c = Process(target=consumer_task, args=(queue, output_dir, consumer_id))
    c.start()
    return c
