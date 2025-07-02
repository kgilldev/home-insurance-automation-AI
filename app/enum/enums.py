from enum import Enum

class DecisionStatus(str, Enum):
    ACCEPT = "ACCEPT"
    REJECT = "REJECT"
    ESCALATED = "ESCALATED"