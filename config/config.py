import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuration class for loading environment variables."""

    @staticmethod
    def load_config():
        """Load the configuration values from environment variables."""
        config = {
            'POP_SERVER': os.getenv('POP_SERVER'),
            'POP_PORT': os.getenv('POP_PORT'),
            'POP_USERNAME': os.getenv('POP_USERNAME'),
            'POP_PASSWORD': os.getenv('POP_PASSWORD'),
        }

        # Perform checks for mandatory values
        if not config['POP_SERVER']:
            raise EnvironmentError("POP_SERVER environment variable is not set. "
                                   "Please ensure it's defined in the .env file.")

        if not config['POP_PORT'] or not config['POP_PORT'].isdigit():
            raise EnvironmentError("POP_PORT environment variable is either not set or invalid. "
                                   "Please ensure it's a valid integer in the .env file.")

        if not config['POP_USERNAME']:
            raise EnvironmentError("POP_USERNAME environment variable is not set. "
                                   "Please ensure it's defined in the .env file.")

        if not config['POP_PASSWORD']:
            raise EnvironmentError("POP_PASSWORD environment variable is not set. "
                                   "Please ensure it's defined in the .env file.")

        # Convert POP_PORT to an integer after validation
        config['POP_PORT'] = int(config['POP_PORT'])

        return config
