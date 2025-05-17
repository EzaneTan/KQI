import json
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger("KQI Security Audit")

class AuditLogger:
    """
    Append-only JSON logger for critical security events.
    """

    def __init__(self, log_path: str = "./security/audit.log"):
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def record_event(self, event_type: str, payload: dict):
        """
        Write a timestamped event to the audit log.
        """
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "event_type": event_type,
            "payload": payload
        }
        with open(self.log_path, "a") as f:
            f.write(json.dumps(entry) + "\n")
        logger.info(f"Audit event recorded: {event_type}")
