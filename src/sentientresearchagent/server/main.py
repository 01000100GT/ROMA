"""
Main Server Module

Contains the main server class and factory functions.
"""

from loguru import logger
import os
from typing import Optional

from .app import create_app, create_socketio, register_routes
from .services import ProjectService, ExecutionService
from ..core.system_manager import SystemManager
from .utils import BroadcastManager
from ..config import SentientConfig, auto_load_config
from ..config import auto_load_config


class SentientServer:
    """
    Main server class that orchestrates all components.
    
    This class follows the application factory pattern and provides
    a clean, testable interface for the server.
    """
    
    def __init__(self, config_input: Optional[SentientConfig] = None):
        """
        Initialize the server.
        
        Args:
            config: Optional configuration dictionary
        """
        # Ensure self.config is ALWAYS a SentientConfig instance
        if config_input is None:
            logger.info("SentientServer: No config provided, auto-loading SentientConfig...")
            self.config: SentientConfig = auto_load_config()
        elif isinstance(config_input, SentientConfig):
            self.config: SentientConfig = config_input
            logger.info("SentientServer: Initialized with provided SentientConfig instance.")
        else:
            # This case should ideally not be hit if callers adhere to type hints.
            # If it could be a dict, we need to convert it.
            logger.warning(f"SentientServer: Received config_input of type {type(config_input)}, not SentientConfig. Attempting to parse as SentientConfig.")
            if isinstance(config_input, dict):
                try:
                    self.config: SentientConfig = SentientConfig(**config_input)
                except Exception as e:
                    logger.error(f"SentientServer: Failed to parse dict config_input into SentientConfig: {e}. Falling back to auto_load_config.")
                    self.config: SentientConfig = auto_load_config()
            else: # Not None, not SentientConfig, not dict - unexpected.
                logger.error(f"SentientServer: Unexpected config_input type {type(config_input)}. Falling back to auto_load_config.")
                self.config: SentientConfig = auto_load_config()
        
        # Verify that self.config is indeed a SentientConfig object
        if not isinstance(self.config, SentientConfig):
            logger.critical(f"SentientServer: self.config is NOT a SentientConfig object after init (type: {type(self.config)}). This is a critical error. Defaulting again.")
            self.config = SentientConfig() # Fallback to a default Pydantic model

        self.app = None
        self.socketio = None
        self.system_manager = None
        self.project_service = None
        self.execution_service = None
        self.broadcast_manager = None
        
    def create(self):
        """
        Create and configure all server components.
        
        Returns:
            Tuple of (app, socketio) for running the server
        """
        logger.info("🚀 Creating Sentient Research Agent Server...")
        
        # Create Flask app and SocketIO
        self.app = create_app(self.config)
        self.socketio = create_socketio(self.app)
        
        # Initialize core services
        logger.info("🔧 Initializing core services...")
        self.system_manager = SystemManager(config=self.config)
        
        # MODIFIED: Get default_profile directly from the SentientConfig Pydantic model
        # The default value is set in SentientConfig definition itself.
        # If a sentient.yaml file overrides 'default_profile', Pydantic will load that.
        default_profile_to_use = self.config.default_profile 
        logger.info(f"🎯 Using default profile from config: {default_profile_to_use}")
        
        try:
            self.system_manager.initialize_with_profile(default_profile_to_use)
        except Exception as e:
            logger.error(f"Failed to initialize SystemManager with profile '{default_profile_to_use}': {e}")
            # Decide if this is a fatal error for the server.
            # For now, let it propagate if SystemManager.initialize_with_profile re-raises.
            # Or, handle it by trying a fallback or logging a critical failure.
            raise # Re-raise for now to see full impact

        # Setup WebSocket HITL integration IMMEDIATELY after system init
        logger.info("🔌 Setting up WebSocket HITL integration...")
        self.system_manager.setup_websocket_hitl(self.socketio) # Assumes system_manager.config is now profile-aware
        
        # Verify WebSocket HITL is ready
        # Accessing system_manager.config, which should be the same instance as self.config
        if self.system_manager.config and self.system_manager.config.execution.enable_hitl:
            if self.system_manager.is_websocket_hitl_ready():
                logger.info("✅ WebSocket HITL verified as ready")
            else:
                logger.error("❌ WebSocket HITL setup failed or not available!")
        
        # Create broadcast manager
        self.broadcast_manager = BroadcastManager(
            self.socketio, 
            self.system_manager, 
            None  # Will be set after project_service is created
        )
        
        # Create project service with broadcast callback
        self.project_service = ProjectService(
            self.system_manager,
            self.broadcast_manager.broadcast_graph_update
        )
        
        # Update broadcast manager with project service and wire up cross-references
        self.broadcast_manager.project_service = self.project_service
        self.project_service.broadcast_manager = self.broadcast_manager
        
        # Create execution service
        self.execution_service = ExecutionService(
            self.project_service,
            self.system_manager
        )
        
        # Register all routes and event handlers
        logger.info("📡 Registering routes and event handlers...")
        register_routes(
            self.app, 
            self.socketio, 
            self.system_manager, 
            self.project_service, 
            self.execution_service
        )
        
        # Final readiness check
        if self.system_manager.config and self.system_manager.config.execution.enable_hitl:
            hitl_status = self.system_manager.get_websocket_hitl_status()
            logger.info(f"🎮 Final HITL Status: {hitl_status}")
        
        # Log current profile info
        current_profile_active = self.system_manager.get_current_profile()
        logger.info(f"🤖 Active Agent Profile in SystemManager: {current_profile_active}")
        # Also log from the main config for verification
        logger.info(f"🤖 Active Agent Profile in SentientConfig: {self.config.active_profile_name}")

        
        logger.info("✅ Server created successfully!")
        return self.app, self.socketio
    
    def run(self, host='0.0.0.0', port=5000, debug=False):
        """
        Run the server.
        
        Args:
            host: Host to bind to
            port: Port to bind to
            debug: Enable debug mode
        """
        if not self.app or not self.socketio:
            self.create()
        
        logger.info(f"🚀 Starting Sentient Research Agent Server on {host}:{port}")
        logger.info("📡 WebSocket: http://localhost:5000")
        logger.info("🌐 Frontend: http://localhost:3000")
        logger.info("📊 System Info: http://localhost:5000/api/system-info")
        logger.info("")
        logger.info("🎯 Simple API Endpoints:")
        logger.info("   POST /api/simple/execute - Execute any goal")
        logger.info("   POST /api/simple/research - Quick research tasks")
        logger.info("   POST /api/simple/analysis - Quick analysis tasks")
        logger.info("   GET  /api/simple/status - Simple API status")
        logger.info("   WebSocket: simple_execute_stream - Streaming execution")
        logger.info("")
        logger.info("📚 Example usage:")
        logger.info("   curl -X POST http://localhost:5000/api/simple/research \\")
        logger.info("        -H 'Content-Type: application/json' \\")
        logger.info("        -d '{\"topic\": \"quantum computing applications\"}'")
        
        try:
            self.socketio.run(
                self.app, 
                debug=debug, 
                host=host, 
                port=port, 
                use_reloader=False
            )
        except Exception as e:
            logger.error(f"❌ Server startup error: {e}")
            import traceback
            traceback.print_exc()


def create_server(config: Optional[SentientConfig] = None) -> SentientServer:
    """
    Factory function to create a server instance.
    
    Args:
        config: Optional SentientConfig instance. If None, it will be auto-loaded.
        
    Returns:
        SentientServer instance
    """
    return SentientServer(config)


# For backward compatibility with the original server
# This main() function now also benefits from the auto-loaded SentientConfig
# DEPRECATED: Consider removing if direct module execution is not the primary way to start.
# The __main__.py in the server package or visualization_server.py are preferred entry points.
# def main():
# """Main entry point for the server."""
# server = create_server() 
# server.run() 


# if __name__ == '__main__':
# # This allows running the server module directly.
# # Example: python -m src.sentientresearchagent.server
# # (Assuming __main__.py in the server package calls this main function or similar)
# main() 