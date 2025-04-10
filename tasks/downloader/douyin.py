import http.client
import os
import socket
import time
from uuid import uuid4


def download_file(url, max_retries=3):
    target_dir = "/srv/videos/douyin-downloads"
    os.makedirs(target_dir, exist_ok=True)

    # Set socket timeout
    socket.setdefaulttimeout(100)  # 30 seconds timeout

    for attempt in range(max_retries):
        conn = None
        try:
            # Create new connection for each attempt
            conn = http.client.HTTPConnection("localhost", 5679, timeout=100)
            conn.request(
                "GET",
                f"/api/download?url={url}",
                headers={"Connection": "close"},  # Force connection close
            )

            response = conn.getresponse()

            if response.status != 200:
                raise Exception(f"HTTP Error: {response.status} - {response.reason}")

            # Read data in chunks to avoid memory issues
            data = bytearray()
            chunk_size = 8192  # 8KB chunks
            while True:
                chunk = response.read(chunk_size)
                if not chunk:
                    break
                data.extend(chunk)

            print(response.headers)
            file_name = response.headers.get("file_name") or f"{uuid4().hex}.mp4"
            full_path = os.path.join(target_dir, file_name)

            with open(full_path, "wb") as f:
                f.write(data)

            return {"success": True, "file_path": full_path, "file_name": file_name}

        except socket.timeout:
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
            raise Exception("Connection timeout")

        except BlockingIOError:
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
            raise Exception("BlockingIOError occurred")

        except Exception as e:
            raise e

        finally:
            # Always close the connection
            if conn:
                conn.close()


if "__name__" == "__main__":
    # parse video_url from command line arguments
    video_url = "https://v.douyin.com/L4FJNR3/"
    result = download_file(video_url)
    print(result)
