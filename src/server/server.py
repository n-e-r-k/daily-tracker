from manifest import Manifest
from log_config import create_logger
from flask import Flask, request, send_file
from flask_restful import Resource, Api

logger = create_logger("daily-tracker-server")

class DTServer():
    def __init__(self):
        pass
