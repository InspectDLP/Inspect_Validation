import json
import logging
import os
from typing import Dict, Any
from my_proof.models.proof_response import ProofResponse
from my_proof.checks import TwitterDataValidator

class Proof:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        logging.info(f"Config: {self.config}")
        self.proof_response = ProofResponse(dlp_id=config['dlp_id'])

    def generate(self) -> ProofResponse:
        input_data = ''
        for input_filename in os.listdir(self.config['input_dir']):
            input_file = os.path.join(self.config['input_dir'], input_filename)
            if os.path.splitext(input_file)[1].lower() == '.zip':
                print(f"Reading file: {input_file}")
                with open(input_file, 'r') as f:
                    input_data = json.load(f)

        qualityRes = Quality(input_data)
        
        self.proof_response.score = qualityRes
        self.proof_response.authenticity = 1.0
        self.proof_response.uniqueness = 1.0
        self.proof_response.valid = True 
        
        if qualityRes < 0.0:
            self.proof_response.valid = False
            self.proof_response.score = 0.0
            return self.proof_response

        print(f"Final proof response: {self.proof_response.__dict__}")
        return self.proof_response

def Quality(data: Dict[str, Any]) -> float:
    validator = TwitterDataValidator()
    result = validator.validate(data)
    return result
