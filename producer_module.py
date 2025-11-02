import os
import time
from io import BytesIO
from PIL import Image
from multiprocessing import Process
from logger_config import get_logger


log = get_logger("producer")


def producer_task(queue, input_dir, check_interval=3, idle_timeout=20, thumbnail_size=(128, 128), batch_size=5):
    """
    Monitors the input directory for new images.
    Converts them into thumbnails with size = thumbnail_size and pushes batches to the queue.
    """
    processed = set()
    last_new_time = time.time()

    log.info("Producer started watching directory...")

    batch = []

    while True:
        all_files = [
            f for f in os.listdir(input_dir)
            if f.lower().endswith(('.jpg', '.jpeg', '.png'))
        ]
        new_files = []
        for f in all_files:
            if f in processed:
                continue

            name, _ = os.path.splitext(f)
            thumbnail_name = f"{name}-thumbnail.jpg"
            thumbnail_path = os.path.join("consumer", thumbnail_name)

            if os.path.exists(thumbnail_path):
                log.info(f"Skipping already converted image: {f}")
                processed.add(f)
                continue

            new_files.append(f)

        if new_files:
            for file_name in new_files:
                file_path = os.path.join(input_dir, file_name)
                try:
                    img = Image.open(file_path)
                    img.thumbnail(thumbnail_size)

                    if img.mode in ("RGBA", "LA"):
                        background = Image.new("RGB", img.size, (255, 255, 255))
                        background.paste(img, mask=img.split()[-1])
                        img = background
                    else:
                        img = img.convert("RGB")

                    buf = BytesIO()
                    img.save(buf, format="JPEG")

                    batch.append((file_name, buf.getvalue()))
                    processed.add(file_name)

                    if len(batch) >= batch_size:
                        queue.put(batch)
                        log.info(f"Queued batch of {len(batch)} thumbnails.")
                        batch = []  # reset batch
                        last_new_time = time.time()

                except Exception as e:
                    log.error(f"Error processing {file_name}: {e}")

        # Send remaining items if any exist before sleeping
        if batch:
            queue.put(batch)
            log.info(f"Queued remaining batch of {len(batch)} thumbnails.")
            batch = []
            last_new_time = time.time()

        # exit if idle for too long
        if time.time() - last_new_time > idle_timeout:
            log.info("No new files detected recently. Producer exiting.")
            break

        time.sleep(check_interval)

    # Signal consumer to stop
    queue.put(None)
    log.info(f"Producer done. Total images processed: {len(processed)}")


def start_producer(queue, input_dir, check_interval=3, idle_timeout=20, thumbnail_size=(128, 128), batch_size=5):
    p = Process(
        target=producer_task,
        args=(queue, input_dir, check_interval, idle_timeout, thumbnail_size, batch_size)
    )
    p.start()
    return p
