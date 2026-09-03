#!/usr/bin/env python3
"""Smoke tests for microduck_description's URDF xacro (mirrors pt_description in pantilt_ros2)."""

import os
import subprocess
import xml.etree.ElementTree as ET

from ament_index_python.packages import get_package_share_directory

_SHARE = get_package_share_directory('microduck_description')
_XACRO_FILE = os.path.join(_SHARE, 'urdf', 'microduck.urdf.xacro')
_STATIC_URDF_FILE = os.path.join(_SHARE, 'urdf', 'microduck.urdf')

_LEG_JOINTS = ('hip_yaw', 'hip_roll', 'hip_pitch', 'knee', 'ankle')
_HEAD_JOINTS = ('neck_pitch', 'head_pitch', 'head_yaw', 'head_roll')
_ALL_JOINTS = frozenset(
    f'{side}_{j}' for side in ('left', 'right') for j in _LEG_JOINTS
) | frozenset(_HEAD_JOINTS) | frozenset({'jaw'})


def _run_xacro(*args):
    result = subprocess.run(['xacro', *args], capture_output=True, text=True, timeout=30)
    assert result.returncode == 0, f'xacro failed for {args}:\n{result.stderr}'
    return result.stdout


def _process_urdf():
    return ET.fromstring(_run_xacro(_XACRO_FILE))


def _mesh_paths(root):
    for mesh in root.iter('mesh'):
        filename = mesh.get('filename')
        if filename and filename.startswith('package://microduck_description/'):
            yield filename.removeprefix('package://microduck_description/')


def test_processes_to_valid_xml():
    root = _process_urdf()
    assert root.tag == 'robot'
    assert root.get('name') == 'microduck'


def test_all_15_joints_present_with_valid_limits():
    root = _process_urdf()
    joints = {j.get('name'): j for j in root.findall('joint') if j.get('type') != 'fixed'}
    assert set(joints) == _ALL_JOINTS
    for name, joint in joints.items():
        limit = joint.find('limit')
        assert limit is not None, f'{name} has no <limit>'
        lower, upper = float(limit.get('lower')), float(limit.get('upper'))
        assert lower < upper, f'{name} lower={lower} >= upper={upper}'


def test_referenced_meshes_exist_on_disk():
    root = _process_urdf()
    paths = list(_mesh_paths(root))
    assert paths, 'no mesh references found'
    for rel_path in paths:
        full_path = os.path.join(_SHARE, rel_path)
        assert os.path.isfile(full_path), f'missing mesh {full_path}'


def test_leg_parent_child_chains():
    root = _process_urdf()
    parent_of = {j.find('child').get('link'): j.find('parent').get('link')
                 for j in root.findall('joint')}
    for side in ('left', 'right'):
        assert parent_of[f'yaw2roll_{side}'] == 'trunk_base'
        assert parent_of[f'hip_{side}'] == f'yaw2roll_{side}'
        assert parent_of[f'upper_leg_{side}'] == f'hip_{side}'
        assert parent_of[f'leg_{side}'] == f'upper_leg_{side}'
        assert parent_of[f'ankle_{side}'] == f'leg_{side}'


def _canonicalize_ignoring_mesh_path_scheme(xml_string):
    # microduck.urdf deliberately uses ../meshes/... instead of package:// (works in any viewer).
    root = ET.fromstring(xml_string)
    for mesh in root.iter('mesh'):
        filename = mesh.get('filename')
        if filename:
            mesh.set('filename', filename.removeprefix(
                'package://microduck_description/').removeprefix('../'))
    return ET.canonicalize(ET.tostring(root, encoding='unicode'), strip_text=True)


def test_static_urdf_matches_xacro_output():
    """Guards microduck.urdf against drifting out of sync with the xacro sources."""
    generated = _canonicalize_ignoring_mesh_path_scheme(_run_xacro(_XACRO_FILE))
    with open(_STATIC_URDF_FILE) as f:
        static = _canonicalize_ignoring_mesh_path_scheme(f.read())
    assert generated == static, (
        'microduck.urdf is stale — regenerate it with: '
        'xacro urdf/microduck.urdf.xacro > urdf/microduck.urdf, then re-apply the ../meshes/ '
        'path substitution'
    )


def test_static_urdf_mesh_paths_resolve_on_disk():
    urdf_dir = os.path.dirname(_STATIC_URDF_FILE)
    root = ET.parse(_STATIC_URDF_FILE).getroot()
    paths = [m.get('filename') for m in root.iter('mesh') if m.get('filename')]
    assert paths, 'no mesh references found in microduck.urdf'
    for rel_path in paths:
        assert rel_path.startswith('../meshes/'), f'unexpected mesh path scheme: {rel_path}'
        assert os.path.isfile(os.path.join(urdf_dir, rel_path)), f'missing mesh {rel_path}'
