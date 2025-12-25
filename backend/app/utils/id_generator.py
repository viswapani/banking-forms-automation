import uuid
from datetime import datetime


def generate_ack_id() -> str:
    """
    Generate a unique acknowledgment ID.
    Format example: ACK-20241220-9F3C1A2B
    """
    now = datetime.utcnow().strftime("%Y%m%d")
    # Take 8 chars from a random UUID
    random_part = uuid.uuid4().hex[:8].upper()
    return f"ACK-{now}-{random_part}"