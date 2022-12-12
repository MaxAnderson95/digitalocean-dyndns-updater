import logging
from dynaconf import Dynaconf, Validator

settings = Dynaconf(
    envvar_prefix=False,
    validators=[
        Validator("DIGITALOCEAN_TOKEN", must_exist=True),
        Validator("RECORD_NAME", must_exist=True),
        Validator("ZONE_NAME", must_exist=True),
        Validator("TTL", default=3600, must_exist=True,
                  is_type_of=int, gte=30),
        Validator("LOG_LEVEL", default=logging.INFO)
    ]
)

settings.validators.validate_all()
