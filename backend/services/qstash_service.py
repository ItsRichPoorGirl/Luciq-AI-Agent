import os
import json
from typing import Dict, Any, Optional
from qstash.client import QStash
from utils.logger import logger
from utils.config import config, EnvMode


class QStashService:
    """Service for QStash immediate message delivery for real-time agent execution."""
    
    def __init__(self):
        self._qstash_token = os.getenv("QSTASH_TOKEN")
        self._webhook_base_url = os.getenv("WEBHOOK_BASE_URL", "http://localhost:8000")
        
        if not self._qstash_token:
            logger.warning("QSTASH_TOKEN not found. QStash immediate delivery will not work without it.")
            self._qstash = None
            self._available = False
        else:
            self._qstash = QStash(token=self._qstash_token)
            self._available = True
            logger.info(f"QStash service initialized with webhook base: {self._webhook_base_url}")
    
    @property
    def available(self) -> bool:
        """Check if QStash service is available for use."""
        return self._available and config.ENV_MODE == EnvMode.PRODUCTION
    
    async def send_immediate_agent_execution(
        self,
        agent_run_id: str,
        thread_id: str,
        instance_id: str,
        project_id: str,
        model_name: str,
        enable_thinking: Optional[bool],
        reasoning_effort: Optional[str],
        stream: bool,
        enable_context_manager: bool,
        agent_config: Optional[dict] = None,
        is_agent_builder: Optional[bool] = False,
        target_agent_id: Optional[str] = None,
        request_id: Optional[str] = None,
    ) -> bool:
        """
        Send immediate agent execution request via QStash.
        Returns True if successfully sent, False otherwise.
        """
        if not self.available:
            logger.debug("QStash service not available, falling back to dramatiq")
            return False
        
        try:
            # Prepare the payload for the webhook
            payload = {
                "type": "agent_execution",
                "data": {
                    "agent_run_id": agent_run_id,
                    "thread_id": thread_id,
                    "instance_id": instance_id,
                    "project_id": project_id,
                    "model_name": model_name,
                    "enable_thinking": enable_thinking,
                    "reasoning_effort": reasoning_effort,
                    "stream": stream,
                    "enable_context_manager": enable_context_manager,
                    "agent_config": agent_config,
                    "is_agent_builder": is_agent_builder,
                    "target_agent_id": target_agent_id,
                    "request_id": request_id,
                }
            }
            
            # Send immediate message to our webhook endpoint
            webhook_url = f"{self._webhook_base_url}/api/qstash/agent-execute"
            
            response = self._qstash.message.publish(
                destination=webhook_url,
                body=json.dumps(payload),
                headers={"Content-Type": "application/json"}
            )
            
            logger.info(f"QStash immediate agent execution sent: {agent_run_id} -> {webhook_url}")
            logger.debug(f"QStash response: {response}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to send QStash immediate agent execution: {e}")
            return False
    
    async def health_check(self) -> Dict[str, Any]:
        """Check QStash service health."""
        if not self._available:
            return {
                "status": "unavailable",
                "reason": "QSTASH_TOKEN not configured"
            }
        
        try:
            # Try to get QStash info to verify connection
            info = self._qstash.message.list(limit=1)
            return {
                "status": "healthy",
                "webhook_base_url": self._webhook_base_url,
                "env_mode": config.ENV_MODE.value
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }


# Global QStash service instance
qstash_service = QStashService()