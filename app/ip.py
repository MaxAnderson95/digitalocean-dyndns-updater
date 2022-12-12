import requests
import random
from logger import configure_logging

logger = configure_logging(__name__)

urls = [
    "https://ifconfig.io",
    "https://ipconfig.io",
    "https://ifconfig.co"
]

headers = {
    'User-Agent': 'curl'
}


def get_public_ip() -> str:
    # Randomize the url list so that it doesn't use the same service every time
    random.shuffle(urls)
    last_item = urls[-1]

    for url in urls:
        try:
            logger.debug(f"Sending request for public IP to {url}")
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                ip = response.text.strip()
                logger.info(f"Public IP address discovered: {ip}")
                return ip
        except requests.exceptions.RequestException as e:
            logger.debug(f"Failed to retreive IP from url {url}")
            if url != last_item:
                logger.debug("Trying next available IP lookup service.")
                continue
            else:
                logger.exception(
                    f"Failed to retreive public IP from any of the available lookup services")
                raise Exception(
                    f"Failed to retreive public IP from any of the available lookup services") from e
