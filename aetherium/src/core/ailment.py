from typing import Dict, Any
import time

class AetheriumAilment(Exception):
    def __init__(self, fault_code: int, message: str):
        self.fault_code = fault_code
        self.message = message
        super().__init__(message)

    def to_struct(self) -> Dict[str, Any]:
        """
        Converts the ailment to a Structure Report compatible dictionary.
        Structure Report {
            Gauge Fault_Code;
            Coffer Report_Message[128];
            Coffer Timestamp[20]; 
        }
        """
        # Simple timestamp simulation
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        
        return {
            'Fault_Code': self.fault_code,
            'Report_Message': self.message,
            'Timestamp': timestamp
        }
