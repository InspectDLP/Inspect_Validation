import json
from typing import Dict, Any, List

class TwitterDataValidator:
    def __init__(self, min_followers: int = 5, target_followers: int = 500):
        self.min_followers = min_followers
        self.target_followers = target_followers
        self.max_handle_length = 50
        self.max_description_length = 280

    def validate_basic_structure(self, data: Dict[str, Any]) -> float:
        if not isinstance(data, dict):
            return 0.0
        valid_points = 0
        total_points = 4  # Total checks we're performing

        # Check required fields exist
        required_fields = ["handle", "description", "followers"]
        if all(field in data for field in required_fields):
            valid_points += 1

        # Check types
        if isinstance(data.get("handle"), str):
            valid_points += 1
        if isinstance(data.get("description"), str):
            valid_points += 1
        if isinstance(data.get("followers"), list):
            valid_points += 1

        return valid_points / total_points

    def check_handle_format(self, handle: str) -> float:
        if not handle:
            return 0.0
            
        valid_points = 0
        total_points = 5
        
        # Check 1: Length between 4 and 15 characters
        if 4 <= len(handle) <= 15:
            valid_points += 1
            
        # Check 2: Starts with a letter or number
        if handle[0].isalnum():
            valid_points += 1
            
        # Check 3: Contains only letters, numbers, and underscores
        if all(c.isalnum() or c == '_' for c in handle):
            valid_points += 1

        # Check 4: Not empty
        if handle.strip():
            valid_points += 1

        # Check 5: Within maximum length
        if len(handle) <= self.max_handle_length:
            valid_points += 1
            
        return valid_points / total_points

    def check_description(self, description: str) -> float:
        if not description:
            return 0.0

        valid_points = 0
        total_points = 3

        # Check 1: Not empty
        if description.strip():
            valid_points += 1

        # Check 2: Within maximum length
        if len(description) <= self.max_description_length:
            valid_points += 1

        # Check 3: Contains meaningful content (basic check)
        if len(description.split()) > 2:  # At least 3 words
            valid_points += 1

        return valid_points / total_points

    def calculate_follower_score(self, followers: List[str]) -> float:
        if not followers:
            return 0.0
            
        num_followers = len(followers)
        

        # If below minimum followers, return 0
        if num_followers < self.min_followers:
            return 0.0
            
        # Calculate score based on follower count clamped at 1,0
        score = min(num_followers / self.target_followers, 1.0)
        
        return score

    def check_follower_handles(self, followers: List[str]) -> float:
        if not followers:
            return 0.0
            
        valid_handles = 0
        
        for handle in followers:
            if (isinstance(handle, str) and 
                handle.strip() and 
                self.check_handle_format(handle) > 0.5):
                valid_handles += 1
                
        return valid_handles / len(followers)

    def validate(self, data: Dict[str, Any]) -> float:
        print(f"\nStarting Twitter data validation")
        
        if not data:
            print("No data provided")
            return 0.0

        # Extract relevant fields
        handle = data.get("handle", "")
        description = data.get("description", "")
        followers = data.get("followers", [])
        ranking = data.get("ranking", {})
        tweets = data.get("tweets", [])
        
        # Run all checks
        checks = [
            ("Basic Structure", self.validate_basic_structure(data)),
            ("Handle Format", self.check_handle_format(handle)),
            ("Description", self.check_description(description)),
            ("Follower Count", self.calculate_follower_score(followers)),
            ("Follower Handles", self.check_follower_handles(followers))
        ]
        
        print("\nIndividual check results:")
        for name, value in checks:
            print(f"{name}: {value:.3f}")
            
        # Calculate weighted average
        weights = [0.2, 0.1, 0.1, 0.5, 0.1]  # Adjusted weights
        final_score = sum(score * weight for (_, score), weight in zip(checks, weights))
        if ranking:
            final_score += 0.1
        if tweets:
            final_score += 0.1

        final_score = min(final_score, 1.0)

        print(f"\nFinal weighted score: {final_score:.3f}")
        
        # If score is too low, return -1 to indicate invalid data, base score if valid and no followers is 0.2
        if final_score < 0.15:
            print("Failed validation - returning -1")
            return -1
            
        return final_score


if __name__ == "__main__":
    f = open("sample.json", "r")
    data = json.loads(f.read())
    validator = TwitterDataValidator()
    for i in data:
        result = validator.validate(i)
        print(len(i["followers"]))
        print(f"Validation result: {result}")

