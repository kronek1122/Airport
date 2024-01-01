import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import time
from unittest.mock import patch
from client import PlaneSocket

@pytest.fixture
def mock_socket():
    with patch('client.s.socket') as mock_socket:
        yield mock_socket.return_value

def test_data_dictionary(mock_socket):
    with patch('client.PlaneGenerator') as mock_plane_generator:
        mock_plane_generator.return_value.position_generator.return_value = [1, 2, 3]
        mock_plane_generator.return_value.vector_generator.return_value = [4, 5, 6]

        plane_socket = PlaneSocket(flight_num='ABC123')

        plane_socket.fuel_empty_time = 0

        data = plane_socket.data_dictionary()

    assert isinstance(data, dict)
    assert 'flight_number' in data
    assert 'position_x' in data
    assert 'position_y' in data
    assert 'position_z' in data
    assert 'velocity_vector' in data
    assert 'IS_FUEL' in data
    assert 'status' in data
    assert data['position_x'] == 1
    assert data['position_y'] == 2
    assert data['position_z'] == 3
    assert data['velocity_vector'] == [4, 5, 6]
    assert data['IS_FUEL']
    assert data['status'] == 'IN_AIR'

def test_json_data_converter(mock_socket):
    plane_socket = PlaneSocket(flight_num='ABC123')

    plane_socket.fuel_empty_time = 0

    json_data = plane_socket.json_data_converter()

    assert isinstance(json_data, str)
    assert 'flight_number' in json_data
    assert 'position_x' in json_data
    assert 'position_y' in json_data
    assert 'position_z' in json_data
    assert 'velocity_vector' in json_data
    assert 'IS_FUEL' in json_data
    assert 'status' in json_data

def test_vector_update(mock_socket):
    plane_socket = PlaneSocket(flight_num='ABC123')

    data = {'velocity_vector': [7, 8, 9]}
    plane_socket.vector_update(data)

    assert plane_socket.velocity == [7, 8, 9]

def test_position_update(mock_socket):
    plane_socket = PlaneSocket(flight_num='ABC123')

    plane_socket.velocity = [1, 2, 3]
    plane_socket.position_x = 0
    plane_socket.position_y = 0
    plane_socket.position_z = 0

    plane_socket.position_update()

    expected_position = [1, 2, 3]

    assert plane_socket.position_x == expected_position[0]
    assert plane_socket.position_y == expected_position[1]
    assert plane_socket.position_z == expected_position[2]

def test_fuel_gauge_check(mock_socket):
    plane_socket = PlaneSocket(flight_num='ABC123')

    plane_socket.fuel_empty_time = time.time() - 1 

    plane_socket.fuel_gauge_check()

    assert not plane_socket.is_fuel


