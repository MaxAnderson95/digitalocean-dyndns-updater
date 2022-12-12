from logger import configure_logging
from config import settings
from ip import get_public_ip
from records import search_record, create_record, update_record

logger = configure_logging(__name__)

logger.info(
    f"Processing record '{settings.RECORD_NAME}' in DNS zone '{settings.ZONE_NAME}'")

# Get the current public ip address
public_ip = get_public_ip()

# Check if record exists
record = search_record(
    record_name=settings.RECORD_NAME,
    zone_name=settings.ZONE_NAME,
    token=settings.DIGITALOCEAN_TOKEN
)

# If record doesn't exist, create it and set the value to the public IP
if record:
    # Check if current value matches the current public_ip
    if record.data != public_ip:
        logger.info(
            "DNS record exists but the value doesn't match the current IP address. Updating record...")
        update_record(record=record, ip_address=public_ip)
    else:
        logger.info("DNS record already exists and has the current IP.")
else:  # Else update the existing record
    logger.info("DNS record doesn't exist. Creating it and settings its value.")
    create_record(
        record_name=settings.RECORD_NAME,
        zone_name=settings.ZONE_NAME,
        type='A',
        ip_address=public_ip,
        ttl=settings.TTL,
        token=settings.DIGITALOCEAN_TOKEN
    )
