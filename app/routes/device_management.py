from flask import Blueprint, jsonify, request
from ..models import Device, Room, db
from datetime import datetime

device_bp = Blueprint('device', __name__)

@device_bp.route('/rooms/<int:room_id>/devices', methods=['GET'])
def get_room_devices(room_id):
    devices = Device.query.filter_by(room_id=room_id).all()
    return jsonify([{
        'id': device.id,
        'type': device.device_type,
        'status': device.status,
        'last_ping': device.last_ping,
        'configuration': device.configuration
    } for device in devices])

@device_bp.route('/devices/<int:device_id>/configure', methods=['PUT'])
def configure_device(device_id):
    device = Device.query.get_or_404(device_id)
    config = request.json
    device.configuration = config
    db.session.commit()
    return jsonify({'message': 'Device configured successfully'})

@device_bp.route('/devices/<int:device_id>/status', methods=['PUT'])
def update_device_status(device_id):
    device = Device.query.get_or_404(device_id)
    device.status = request.json.get('status', 'active')
    device.last_ping = datetime.utcnow()
    db.session.commit()
    return jsonify({'message': 'Status updated successfully'}) 