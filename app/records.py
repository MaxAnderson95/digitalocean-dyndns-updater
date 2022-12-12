import digitalocean
from digitalocean.Record import Record
from logger import configure_logging

logger = configure_logging(__name__)


def search_record(record_name: str, zone_name: str, token: str) -> Record:
    domain = digitalocean.Domain(
        token=token,
        name=zone_name
    )
    records = domain.get_records()
    for record in records:
        if record.name == record_name and record.type == 'A':
            return record

    return None


def create_record(record_name: str, zone_name: str, type: str, ip_address: str, ttl: int, token: str) -> None:
    domain = digitalocean.Domain(
        token=token,
        name=zone_name
    )
    domain.create_new_domain_record(
        type=type,
        name=record_name,
        data=ip_address,
        ttl=ttl
    )

    logger.info("DNS record created successfully")


def update_record(record: Record, ip_address: str) -> None:
    record.data = ip_address
    record.save()

    logger.info("DNS record updated successfully")
