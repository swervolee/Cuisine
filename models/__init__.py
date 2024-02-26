#!/usr/bin/python3
"""Basemodel and filestorage connect"""
from models.engine.file_storage import FileStorage


storage = FileStorage()
storage.reload()
