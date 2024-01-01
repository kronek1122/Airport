import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import pytest
from control_tower import ControlTower


sample_data = {
    'position_x': 1000,
    'position_y': -2000,
    'position_z': 500,
    'flight_number': 'ABC123',
    'status': 'ON AIR',
    'velocity_vector': [150, 100, 50]
}


class MockConnection:
    def get_coordinates(self):
        return [(2000, -1500, 600, 'XYZ456'), (-1000, 1000, 400, 'DEF789')]


def test_dictionary_data_pack():
    connection_mock = MockConnection()
    control_tower = ControlTower(sample_data, connection_mock)
    result = control_tower.dictionary_data_pack()
    assert result == {'msg': 'Change direction', 'status': 'ON AIR', 'velocity_vector': [150, 100, 50]}

def test_distance_calculation():
    connection_mock = MockConnection()
    control_tower = ControlTower(sample_data, connection_mock)
    point_one = (3000, -3000, 1000)
    point_two = (1000, -2000, 500)
    result = control_tower.distance_calculation(point_one, point_two)

    delta = 0.001

    assert result['distance'] == pytest.approx(2291.287, abs=delta)
    assert result['x'] == 2000
    assert result['y'] == -1000
    assert result['z'] == 500

def test_calc_time_at_const_speed():
    connection_mock = MockConnection()
    control_tower = ControlTower(sample_data, connection_mock)
    distance = 1000
    speed = 100
    result = control_tower.calc_time_at_const_speed(distance, speed)
    assert result == 10.0

def test_vector_change_adjustment():
    connection_mock = MockConnection()
    control_tower = ControlTower(sample_data, connection_mock)
    x, y, z, time = 100, 200, 50, 5
    control_tower.vector_change_adjustment(x, y, z, time)
    assert control_tower.velocity == [20, 40, 10]

def test_guidance_system_sector_A():
    connection_mock = MockConnection()
    control_tower = ControlTower(sample_data, connection_mock)
    control_tower.position_x = 4000
    control_tower.position_y = -3000
    result = control_tower.guidance_system()
    assert result['status'] == 'ON AIR'
    assert result['msg'] == 'Change direction'

def test_guidance_system_sector_B():
    connection_mock = MockConnection()
    control_tower = ControlTower(sample_data, connection_mock)
    control_tower.position_x = -2600
    control_tower.position_y = -3500
    result = control_tower.guidance_system()
    assert result['status'] == 'ON AIR'
    assert result['msg'] == 'Change direction'

def test_guidance_system_sector_C():
    connection_mock = MockConnection()
    control_tower = ControlTower(sample_data, connection_mock)
    control_tower.position_x = -3600
    control_tower.position_y = 2500
    result = control_tower.guidance_system()
    assert result['status'] == 'ON AIR'
    assert result['msg'] == 'Change direction'

def test_guidance_system_sector_D():
    connection_mock = MockConnection()
    control_tower = ControlTower(sample_data, connection_mock)
    control_tower.position_x = 2000
    control_tower.position_y = 3500
    result = control_tower.guidance_system()
    assert result['status'] == 'ON AIR'
    assert result['msg'] == 'Change direction'

def test_guidance_system_sector_E():
    connection_mock = MockConnection()
    control_tower = ControlTower(sample_data, connection_mock)
    control_tower.position_x = -2600
    control_tower.position_y = -3200
    result = control_tower.guidance_system()
    assert result['status'] == 'ON AIR'
    assert result['msg'] == 'Change direction'

def test_guidance_system_sector_F():
    connection_mock = MockConnection()
    control_tower = ControlTower(sample_data, connection_mock)
    control_tower.position_x = 2600
    control_tower.position_y = 3200
    result = control_tower.guidance_system()
    assert result['status'] == 'ON AIR'
    assert result['msg'] == 'Change direction'

def test_guidance_system_sector_G():
    connection_mock = MockConnection()
    control_tower = ControlTower(sample_data, connection_mock)
    control_tower.position_x = 2500
    control_tower.position_y = -2500
    result = control_tower.guidance_system()
    assert result['status'] == 'ON AIR'
    assert result['msg'] == 'Change direction'

def test_guidance_system_sector_H():
    connection_mock = MockConnection()
    control_tower = ControlTower(sample_data, connection_mock)
    control_tower.position_x = -2500
    control_tower.position_y = 2500
    result = control_tower.guidance_system()
    assert result['status'] == 'ON AIR'
    assert result['msg'] == 'Change direction'

def test_guidance_system_sector_I():
    connection_mock = MockConnection()
    control_tower = ControlTower(sample_data, connection_mock)
    control_tower.position_x = 2600
    control_tower.position_y = -1200
    result = control_tower.guidance_system()
    assert result['status'] == 'ON AIR'
    assert result['msg'] == 'Change direction'

def test_guidance_system_sector_J():
    connection_mock = MockConnection()
    control_tower = ControlTower(sample_data, connection_mock)
    control_tower.position_x = -2600
    control_tower.position_y = 1200
    result = control_tower.guidance_system()
    assert result['status'] == 'ON AIR'
    assert result['msg'] == 'Change direction'

def test_guidance_system_sector_K():
    connection_mock = MockConnection()
    control_tower = ControlTower(sample_data, connection_mock)
    control_tower.position_x = 1500
    control_tower.position_y = -1000
    result = control_tower.guidance_system()
    assert result['status'] == 'ON AIR'
    assert result['msg'] == 'Change direction'

def test_guidance_system_sector_L():
    connection_mock = MockConnection()
    control_tower = ControlTower(sample_data, connection_mock)
    control_tower.position_x = -1500
    control_tower.position_y = 1000
    result = control_tower.guidance_system()
    assert result['status'] == 'ON AIR'
    assert result['msg'] == 'Change direction'

def test_guidance_system_sector_R1():
    connection_mock = MockConnection()
    control_tower = ControlTower(sample_data, connection_mock)
    control_tower.position_x = -900
    control_tower.position_y = -1000
    result = control_tower.guidance_system()
    assert result['status'] == 'ON AIR'
    assert result['msg'] == 'Change direction'

def test_guidance_system_sector_R2():
    connection_mock = MockConnection()
    control_tower = ControlTower(sample_data, connection_mock)
    control_tower.position_x = 900
    control_tower.position_y = 1000
    result = control_tower.guidance_system()
    assert result['status'] == 'ON AIR'
    assert result['msg'] == 'Change direction'

def test_guidance_system_collision_emergency_direction_change():
    connection_mock = MockConnection()
    control_tower = ControlTower(sample_data, connection_mock)
    control_tower.position_x = 1500
    control_tower.position_y = 800
    control_tower.emergency_direction_change()
    result = control_tower.guidance_system()
    assert result['status'] == 'ON AIR'
    assert result['msg'] == 'Change direction'

def test_collision_detector_no_collision():
    connection_mock = MockConnection()
    control_tower = ControlTower(sample_data, connection_mock)
    control_tower.position_x = 500
    control_tower.position_y = -1000
    assert not control_tower.collision_detector(200)

def test_collision_detector_collision():
    connection_mock = MockConnection()
    control_tower = ControlTower(sample_data, connection_mock)
    control_tower.position_x = 2000
    control_tower.position_y = -1500
    assert control_tower.collision_detector(200)

def test_collision_detector_self_collision():
    connection_mock = MockConnection()
    control_tower = ControlTower(sample_data, connection_mock)
    control_tower.position_x = 1000
    control_tower.position_y = -2000
    assert not control_tower.collision_detector(200)

def test_collision_detector_collision_same_coordinates_other_flight():
    connection_mock = MockConnection()
    control_tower = ControlTower(sample_data, connection_mock)
    control_tower.position_x = 1000
    control_tower.position_y = -2000
    assert control_tower.collision_detector(200)

def test_collision_detector_no_collision_other_flight_far():
    connection_mock = MockConnection()
    control_tower = ControlTower(sample_data, connection_mock)
    control_tower.position_x = 5000
    control_tower.position_y = -4000
    assert not control_tower.collision_detector(200)

def test_collision_detector_collision_nearby_planes_other_flight():
    connection_mock = MockConnection()
    control_tower = ControlTower(sample_data, connection_mock)
    control_tower.position_x = 1500
    control_tower.position_y = -1000
    assert not control_tower.collision_detector(200)

def test_collision_detector_collision_same_coordinates_other_flight():
    connection_mock = MockConnection()
    control_tower = ControlTower(sample_data, connection_mock)
    control_tower.position_x = 1000
    control_tower.position_y = -2000
    assert not control_tower.collision_detector(200)

def test_collision_detector_collision_far_planes_other_flight():
    connection_mock = MockConnection()
    control_tower = ControlTower(sample_data, connection_mock)
    control_tower.position_x = 5000
    control_tower.position_y = -4000
    assert not control_tower.collision_detector(200)

def test_collision_detector_no_collision_other_flight_near():
    connection_mock = MockConnection()
    control_tower = ControlTower(sample_data, connection_mock)
    control_tower.position_x = 1500
    control_tower.position_y = -1000
    assert not control_tower.collision_detector(50)

def test_collision_detector_collision_other_flight_near():
    connection_mock = MockConnection()
    control_tower = ControlTower(sample_data, connection_mock)
    control_tower.position_x = 1500
    control_tower.position_y = -1000
    assert not control_tower.collision_detector(50)

def test_emergency_direction_change():
    connection_mock = MockConnection()
    control_tower = ControlTower(sample_data, connection_mock)
    control_tower.position_x = 2500
    control_tower.position_y = 1000
    control_tower.emergency_direction_change()