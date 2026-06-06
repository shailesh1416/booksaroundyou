from flask import Blueprint, jsonify
from app import db

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'service': 'admin'}), 200

# Placeholder routes for admin features

@admin_bp.route('/dashboard', methods=['GET'])
def get_dashboard():
    """Master admin dashboard with global stats"""
    return jsonify({'message': 'Feature for later: Admin dashboard'}), 501

@admin_bp.route('/users', methods=['GET'])
def get_all_users():
    """Get all users"""
    return jsonify({'message': 'Feature for later: Get users'}), 501

@admin_bp.route('/listings/<int:listing_id>/moderate', methods=['POST'])
def moderate_listing(listing_id):
    """Moderate/flag a book listing"""
    return jsonify({'message': 'Feature for later: Moderate listing'}), 501
