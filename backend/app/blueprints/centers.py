from flask import Blueprint, jsonify, request
from app import db
from app.models import LocalCenter

centers_bp = Blueprint('centers', __name__)

@centers_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'service': 'centers'}), 200

# Placeholder routes for center management

@centers_bp.route('/', methods=['GET'])
def get_all_centers():
    """Get all local centers, optionally filtered by proximity"""
    return jsonify({'message': 'Get all centers'}), 501

@centers_bp.route('/<int:center_id>', methods=['GET'])
def get_center(center_id):
    """Get details of a specific center"""
    return jsonify({'message': 'Get center'}), 501

@centers_bp.route('/<int:center_id>/dropoff-confirm', methods=['POST'])
def confirm_dropoff(center_id):
    """Center admin confirms book drop-off"""
    return jsonify({'message': 'Feature 5: Confirm dropoff'}), 501

@centers_bp.route('/<int:center_id>/handover-confirm', methods=['POST'])
def confirm_handover(center_id):
    """Center admin confirms book handover to borrower"""
    return jsonify({'message': 'Feature 5: Confirm handover'}), 501
