"""
WebSocket-based Human-in-the-Loop utilities
"""
import asyncio
import uuid
import os
from datetime import datetime
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

# Global reference to the socketio instance
_socketio_instance = None

# Global storage for pending HITL requests
_pending_requests = {}

# Global timeout setting (will be set by the system)
_hitl_timeout_seconds = 1800.0  # Default 30 minutes, but will be overridden

def set_socketio_instance(socketio):
    """Set the global socketio instance for HITL communication"""
    global _socketio_instance
    _socketio_instance = socketio
    logger.info("WebSocket HITL: socketio instance registered")

def set_hitl_timeout(timeout_seconds: float):
    """Set the HITL timeout from configuration"""
    global _hitl_timeout_seconds
    _hitl_timeout_seconds = timeout_seconds
    logger.info(f"WebSocket HITL: timeout set to {timeout_seconds} seconds")

async def websocket_human_review(
    checkpoint_name: str,
    context_message: str,
    data_for_review: Optional[Any] = None,
    node_id: Optional[str] = "N/A",
    current_attempt: int = 1
) -> Dict[str, Any]:
    """
    WebSocket-based human review that broadcasts HITL requests to frontend
    """
    global _socketio_instance, _pending_requests, _hitl_timeout_seconds
    
    logger.info(f"🤔 HITL WebSocket: Broadcasting checkpoint '{checkpoint_name}' for node {node_id}")
    
    if not _socketio_instance:
        logger.error("🚨 HITL WebSocket: No socketio instance available!")
        return {
            "user_choice": "approved",
            "message": f"Auto-approved checkpoint '{checkpoint_name}' (no socketio instance)",
            "modification_instructions": None
        }
    
    # Debug: Check if socketio is available and connected clients
    logger.info(f"🔍 DEBUG: socketio object exists: {_socketio_instance is not None}")
    if _socketio_instance:
        try:
            # Get connected clients count
            connected_clients = len(_socketio_instance.server.manager.rooms.get('/', {}).keys()) if hasattr(_socketio_instance.server, 'manager') else 0
            logger.info(f"🔍 DEBUG: Connected clients: {connected_clients}")
            
            # List all rooms
            if hasattr(_socketio_instance.server, 'manager') and hasattr(_socketio_instance.server.manager, 'rooms'):
                rooms = _socketio_instance.server.manager.rooms
                logger.info(f"🔍 DEBUG: All rooms: {list(rooms.keys())}")
                if '/' in rooms:
                    logger.info(f"🔍 DEBUG: Clients in default room: {list(rooms['/'].keys())}")
        except Exception as e:
            logger.error(f"🔍 DEBUG: Error checking socketio state: {e}")
    
    # Create HITL request
    request_id = str(uuid.uuid4())
    hitl_request = {
        "checkpoint_name": checkpoint_name,
        "context_message": context_message,
        "data_for_review": data_for_review,
        "node_id": node_id,
        "current_attempt": current_attempt,
        "request_id": request_id,
        "timestamp": datetime.now().isoformat()
    }
    
    # Store the request for response handling
    response_future = asyncio.Future()
    _pending_requests[request_id] = response_future
    
    try:
        logger.info("📡 Emitting HITL request to frontend")
        _socketio_instance.emit('hitl_request', hitl_request)
        logger.info("✅ HITL request emitted successfully")
        
        # Wait for response with configured timeout (NO AUTO-APPROVAL ON TIMEOUT)
        try:
            logger.info(f"⏳ Waiting for user response to HITL request {request_id} (timeout: {_hitl_timeout_seconds}s)...")
            response = await asyncio.wait_for(response_future, timeout=_hitl_timeout_seconds)
            logger.info(f"✅ Received HITL response: {response}")
            return response
        except asyncio.TimeoutError:
            logger.warning(f"⏰ HITL request {request_id} timed out after {_hitl_timeout_seconds} seconds")
            # Instead of auto-approving, we should raise an exception or return a timeout status
            # This prevents the modal from disappearing due to auto-approval
            return {
                "user_choice": "timeout",
                "message": f"HITL request timed out after {_hitl_timeout_seconds} seconds",
                "modification_instructions": None
            }
        
    except Exception as e:
        logger.error(f"❌ Error during HITL request: {e}")
        return {
            "user_choice": "error",
            "message": f"Error during HITL request: {e}",
            "modification_instructions": None
        }
    finally:
        # Clean up
        _pending_requests.pop(request_id, None)

def handle_hitl_response(response_data: Dict[str, Any]):
    """Handle HITL response from frontend"""
    global _pending_requests
    
    request_id = response_data.get('request_id')
    if not request_id:
        logger.error("❌ HITL response missing request_id")
        return
    
    future = _pending_requests.get(request_id)
    if not future:
        logger.warning(f"⚠️ No pending request found for ID: {request_id}")
        return
    
    action = response_data.get('action')
    modification_instructions = response_data.get('modification_instructions')
    
    # Convert frontend action to backend format
    if action == 'approve':
        user_choice = 'approved'
        message = f"User approved checkpoint '{response_data.get('checkpoint_name')}'"
    elif action == 'modify':
        user_choice = 'request_modification'
        message = f"User requested modification for '{response_data.get('checkpoint_name')}'"
    elif action == 'abort':
        user_choice = 'aborted'
        message = f"User aborted checkpoint '{response_data.get('checkpoint_name')}'"
    else:
        user_choice = 'approved'
        message = f"Unknown action '{action}', defaulting to approved"
    
    result = {
        "user_choice": user_choice,
        "message": message,
        "modification_instructions": modification_instructions
    }
    
    # Resolve the future with the response
    if not future.done():
        future.set_result(result)
        logger.info(f"✅ HITL response processed for request {request_id}: {user_choice}")