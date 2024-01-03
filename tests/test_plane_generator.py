import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch
from plane_generator import PlaneGenerator  

def test_position_generator():
    generator = PlaneGenerator()
    position = generator.position_generator()

    if 'NNE' in generator.direction:
        assert 0 <= position[0] <= 5000
        assert 4500 <= position[1] <= 5000
    elif 'ENE' in generator.direction:
        assert 4500 <= position[0] <= 5000
        assert 0 <= position[1] <= 5000
    elif 'NNW' in generator.direction:
        assert -5000 <= position[0] <= 0
        assert 4500 <= position[1] <= 5000
    elif 'WNW' in generator.direction:
        assert -5000 <= position[0] <= 0
        assert 0 <= position[1] <= 5000
    elif 'SSE' in generator.direction:
        assert 0 <= position[0] <= 5000
        assert -5000 <= position[1] <= 0
    elif 'ESE' in generator.direction:
        assert 4500 <= position[0] <= 5000
        assert -5000 <= position[1] <= 0
    elif 'SSW' in generator.direction:
        assert -5000 <= position[0] <= 0
        assert -5000 <= position[1] <= 0
    elif 'WSW' in generator.direction:
        assert -5000 <= position[0] <= 0
        assert 0 <= position[1] <= 5000

    assert 2000 <= position[2] <= 5000

def test_vector_generator():
    generator = PlaneGenerator()
    vector = generator.vector_generator()

    if 'NNE' in generator.direction or 'ENE' in generator.direction:
        assert 0 <= abs(vector[0]) <= generator.velocity
        assert vector[1] == -int((generator.velocity**2 - vector[0]**2)**0.5)
        assert vector[2] == 0
    elif 'NNW' in generator.direction or 'WNW' in generator.direction:
        assert 0 <= abs(vector[0]) <= generator.velocity
        assert vector[1] == -int((generator.velocity**2 - vector[0]**2)**0.5)
        assert vector[2] == 0
    elif 'SSE' in generator.direction or 'ESE' in generator.direction:
        assert 0 <= abs(vector[0]) <= generator.velocity
        assert vector[1] == int((generator.velocity**2 - vector[0]**2)**0.5)
        assert vector[2] == 0
    elif 'SSW' in generator.direction or 'WSW' in generator.direction:
        assert 0 <= abs(vector[0]) <= generator.velocity
        assert vector[1] == int((generator.velocity**2 - vector[0]**2)**0.5)
        assert vector[2] == 0
