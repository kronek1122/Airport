import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import MagicMock
from plane_manager import PlaneManager

@pytest.fixture
def mock_db_connection():
    return MagicMock()

def test_plane_signal_landed(mock_db_connection):
    dictionary = {
        'flight_number': 123,
        'position_x': 100,
        'position_y': 200,
        'position_z': 0,
        'status': 'IN_AIR',
        'velocity_vector': (1, 2, 3)
    }
    plane_manager = PlaneManager(dictionary, mock_db_connection)
    mock_db_connection.change_status.return_value = {'msg': 'landed', 'status': 'LANDED'}

    result = plane_manager.plane_signal()

    assert result == {'msg': 'landed', 'status': 'LANDED'}
    mock_db_connection.change_status.assert_called_once_with(123, 'LANDED')

def test_plane_signal_crashed(mock_db_connection):
    dictionary = {
        'flight_number': 123,
        'position_x': 100,
        'position_y': 200,
        'position_z': -10,
        'status': 'IN_AIR',
        'velocity_vector': (1, 2, 3)
    }
    plane_manager = PlaneManager(dictionary, mock_db_connection)

    result = plane_manager.plane_signal()

    assert result == {'msg': 'plane crashed', 'status': 'CRASHED'}
    mock_db_connection.change_status.assert_called_once_with(123, 'CRASHED')

def test_plane_signal_add_plane_successful(mock_db_connection):
    dictionary = {
        'flight_number': 123,
        'position_x': 100,
        'position_y': 200,
        'position_z': 500,
        'status': 'IN_AIR',
        'velocity_vector': (1, 2, 3)
    }
    plane_manager = PlaneManager(dictionary, mock_db_connection)
    mock_db_connection.get_num_of_planes_by_status.return_value = 99
    mock_db_connection.plane_status.return_value = 'IN_AIR'
    mock_db_connection.add_plane.return_value = {'msg': 'Success'}
    mock_db_connection.change_plane_information.return_value = {'msg': 'Plane information updated'}
    plane_manager.control_tower_system = MagicMock(return_value={'msg': 'Control tower result'})

    result = plane_manager.plane_signal()

    assert result == {'msg': 'Control tower result'}
    mock_db_connection.add_plane.assert_called_once_with(123, 'IN_AIR', 100, 200, 500, 1, 2, 3)
    mock_db_connection.change_plane_information.assert_not_called()

def test_plane_signal_add_plane_error(mock_db_connection):
    dictionary = {
        'flight_number': 123,
        'position_x': 100,
        'position_y': 200,
        'position_z': 500,
        'status': 'IN_AIR',
        'velocity_vector': (1, 2, 3)
    }
    plane_manager = PlaneManager(dictionary, mock_db_connection)
    mock_db_connection.get_num_of_planes_by_status.return_value = 99
    mock_db_connection.plane_status.return_value = 'IN_AIR'
    mock_db_connection.add_plane.return_value = {'msg': 'Error adding new plane to db'}
    mock_db_connection.change_plane_information.return_value = {'msg': 'Plane information updated'}
    plane_manager.control_tower_system = MagicMock(return_value={'msg': 'Control tower result'})

    result = plane_manager.plane_signal()

    assert result == {'msg': 'Control tower result'}
    mock_db_connection.add_plane.assert_called_once_with(123, 'IN_AIR', 100, 200, 500, 1, 2, 3)
    mock_db_connection.change_plane_information.assert_called_once_with(123, 'IN_AIR', 100, 200, 500, 1, 2, 3)

def test_plane_signal_too_many_planes(mock_db_connection):
    dictionary = {
        'flight_number': 123,
        'position_x': 100,
        'position_y': 200,
        'position_z': 500,
        'status': 'IN_AIR',
        'velocity_vector': (1, 2, 3)
    }
    plane_manager = PlaneManager(dictionary, mock_db_connection)
    mock_db_connection.get_num_of_planes_by_status.return_value = 100
    mock_db_connection.plane_status.return_value = 'ON_GROUND'
    mock_db_connection.add_plane.return_value = {'msg': 'Success'}
    plane_manager.control_tower_system = MagicMock(return_value={'msg': 'Control tower result'})

    result = plane_manager.plane_signal()

    assert result == {'msg': 'to many planes in the air', 'status': 'REDIRECTED'}
    assert plane_manager.status == 'REDIRECTED'
    mock_db_connection.add_plane.assert_called_once_with(123, 'REDIRECTED', 100, 200, 500, 1, 2, 3)
