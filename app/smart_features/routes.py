from flask import Blueprint, jsonify, request
from flask_login import current_user
from .guest_interface import SmartRoomController
from ..services.ai_service import AIService
from ..auth.decorators import require_permission
from ..auth.permissions import Permission
from ..auth.models import User
from ..auth.utils import can_access_room

smart_bp = Blueprint('smart', __name__)
ai_service = AIService()

@smart_bp.route('/rooms/<int:room_id>/smart/status', methods=['GET'])
@require_permission(Permission.VIEW_ROOM)
def get_room_status(room_id):
    """Get real-time room status"""
    # Verify user has access to this room
    if not can_access_room(current_user, room_id):
        return jsonify({'error': 'Access denied'}), 403
    
    controller = SmartRoomController(room_id)
    data = controller.get_realtime_data()
    if not data:
        return jsonify({'error': 'No data available'}), 404
    return jsonify(data)

@smart_bp.route('/rooms/<int:room_id>/smart/history', methods=['GET'])
def get_room_history(room_id):
    """Get historical room data"""
    hours = request.args.get('hours', 24, type=int)
    controller = SmartRoomController(room_id)
    data = controller.get_historical_data(hours)
    return jsonify(data)

@smart_bp.route('/rooms/<int:room_id>/smart/control', methods=['POST'])
def control_room_device(room_id):
    """Control room devices"""
    data = request.get_json()
    device_type = data.get('device_type')
    command = data.get('command')
    parameters = data.get('parameters', {})
    
    if not all([device_type, command]):
        return jsonify({'error': 'Missing required fields'}), 400
        
    controller = SmartRoomController(room_id)
    success, message = controller.control_device(device_type, command, parameters)
    
    if success:
        return jsonify({'message': message})
    return jsonify({'error': message}), 400 

@smart_bp.route('/rooms/<int:room_id>/smart/assistant', methods=['POST'])
async def process_assistant_request(room_id):
    """Process natural language requests for room control"""
    user_input = request.json.get('input')
    if not user_input:
        return jsonify({'error': 'No input provided'}), 400
        
    # Get current room context
    controller = SmartRoomController(room_id)
    room_context = {
        'current_status': controller.get_realtime_data(),
        'room_id': room_id
    }
    
    # Process with AI
    response = await ai_service.process_request(user_input, room_context)
    
    return jsonify({
        'response': response,
        'room_status': room_context['current_status']
    })