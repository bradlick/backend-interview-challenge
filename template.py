"""
Avatar Processing Service - Coding Challenge Template (Simplified)

Choose your preferred language and adapt this structure accordingly.
This Python template can be converted to Go, Java, TypeScript, etc.

Mock LLM API Endpoint:
POST /api/v1/moderate-content
Headers: Authorization: Bearer <token>
Body: {
  "content": "description of the generated avatar",
  "user_id": "user123"
}

Response: {
  "approved": true,
  "reason": "Content appears safe"
}
"""

import time
import uuid
import requests
from dataclasses import dataclass
from typing import Optional, Dict
from datetime import datetime

@dataclass
class ModerationResponse:
    is_approved: bool
    reason: Optional[str] = None


@dataclass
class AvatarJob:
    id: str
    user_id: str
    status: str  # pending, completed, failed, rejected
    input_data: str  # user's avatar prompt
    output_url: Optional[str] = None  # generated avatar URL
    created_at: datetime = None
    error_message: Optional[str] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


class AvatarProcessingService:
    def __init__(self, moderation_api_url: str, api_token: str):
        """
        Initialize the avatar processing service.
        
        Args:
            moderation_api_url: Base URL for the moderation API
            api_token: Bearer token for API authentication
        """
        self.moderation_api_url = moderation_api_url
        self.api_token = api_token
        self._jobs = {}
        # TODO: Initialize your storage, HTTP client, etc.
        #pass

    def submit_job(self, user_id: str, input_data: str) -> AvatarJob:
        """
        Submit a new avatar generation job and process it synchronously.
        
        Args:
            user_id: ID of the user requesting the avatar
            input_data: User's avatar generation prompt/description
            
        Returns:
            AvatarJob: The completed job object
            
        Should:
        1. Create a new job with unique ID
        2. Generate a mock avatar URL
        3. Call moderation API
        4. Update job status based on moderation result
        5. Store and return the job
        """
        # TODO: Implement job creation and full processing
        _job = AvatarJob(
                id=uuid.uuid4(),
                user_id=user_id,
                status="pending",  # pending, completed, failed, rejected
                input_data=input_data,  # user's avatar prompt
                output_url=self._generate_mock_avatar_url(input_data)
        )
        self._jobs[_job.id] = _job

        try:
            response = self.call_moderation_api(input_data, user_id)

            if response.is_approved:
                _job.status = "completed"
                _job.error_message = None
            else:
                _job.status = "rejected"
                _job.error_message = response.reason
        except Exception as e:
            _job.status = "failed"
            _job.error_message = str(e)


        return _job

    def get_job_status(self, job_id: str) -> Optional[AvatarJob]:
        """
        Retrieve the current status of a job.
        
        Args:
            job_id: ID of the job to check
            
        Returns:
            AvatarJob or None: The job object if found, None otherwise
        """
        if job_id in self._jobs:
            return self._jobs[job_id]
        return None

    def call_moderation_api(self, content: str, user_id: str) -> ModerationResponse:
        """
        Call the content moderation API to check if avatar passes guidelines.
        
        Args:
            content: Description of the generated avatar
            user_id: ID of the user who requested the avatar
            
        Returns:
            ModerationResponse: Moderation result
            
        Should:
        - Make HTTP POST request to moderation API
        - Handle timeouts and basic errors
        - Parse response into ModerationResponse object
        - Optional: Add simple retry logic
        """
        # TODO: Implement HTTP client call with error handling
        
        headers = {
            "Authorization": f"Bearer {self.api_token}",
        }
        
        data = {
            "content": content,
            "user_id": user_id
        }


        response = requests.post(self.moderation_api_url, headers=headers, data=data)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)

        _body = response.json()
        return ModerationResponse(
            is_approved=_body["approved"],
            reason=_body["reason"]
        )


    def _generate_mock_avatar_url(self, prompt: str) -> str:
        """
        Generate a mock avatar URL (simulate avatar generation).
        
        Args:
            prompt: User's avatar description
            
        Returns:
            str: Mock URL to the generated avatar
        """
        # TODO: Return a unique mock URL like "https://avatars.example.com/avatar_123.png"
        # TODO: return partital hash
        return f"https://avatars.example.com/{hash(prompt)}_{time.time()}.png"


# Example usage and testing
def main():
    """
    Example usage of the avatar processing service.
    You can use this to test your implementation.
    """
    service = AvatarProcessingService(
        moderation_api_url="https://api.example.com",
        api_token="your-api-token-here"
    )
    
    # Submit a job
    job = service.submit_job("user123", "A friendly robot avatar with blue eyes")
    print(f"Job submitted: {job.id}, Status: {job.status}")
    
    # Check status
    retrieved_job = service.get_job_status(job.id)
    print(f"Retrieved job status: {retrieved_job.status if retrieved_job else 'Not found'}")


if __name__ == "__main__":
    main()


"""
IMPLEMENTATION NOTES:

1. Storage: Use a simple in-memory dictionary
   - jobs = {}  # job_id -> AvatarJob

2. HTTP Client: Use requests library or similar
   - Set timeout (e.g., 5 seconds)
   - Handle basic HTTP errors

3. Error Handling: Focus on:
   - API timeout
   - API returns error status
   - Network issues
   - Invalid response format

4. Job Flow:
   - Create job with "pending" status
   - Generate mock avatar URL
   - Call moderation API
   - Update status to "completed" or "rejected"
   - Handle errors by setting status to "failed"

5. Mock Avatar URL: 
   - Return something like f"https://avatars.example.com/{job_id}.png"

6. Keep It Simple:
   - Synchronous processing is fine
   - Basic error handling is sufficient
   - Focus on the API integration
"""
