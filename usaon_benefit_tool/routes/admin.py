from flask import Blueprint, Response
from flask_login import login_required
import csv
import io
import zipfile
from datetime import date

from usaon_benefit_tool._types import RoleName
from usaon_benefit_tool.models.tables import (
    Assessment, AssessmentNode, AssessmentNodeSubtypeApplication,
    Link, Node, NodeSubtypeOther, NodeSubtypeSocietalBenefitArea,
    User
)
from usaon_benefit_tool.util.rbac import forbid_except_for_roles

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/export-database', methods=['GET'])
@login_required
def export_database():
    """Export all database tables as CSV files in a zip archive."""
    forbid_except_for_roles([RoleName.ADMIN])
    
    from usaon_benefit_tool import db
    from sqlalchemy import text
    
    # Create an in-memory zip file
    memory_file = io.BytesIO()
    
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        # List of tables to export
        table_names = [
            'assessment',
            'assessment_node',
            'assessment_node_subtype_application',
            'link',
            'node',
            'node_subtype_other',
            'node_subtype_societal_benefit_area',
            'user',
        ]
        
        for table_name in table_names:
            # Query directly with raw SQL to avoid session issues
            full_table_name = f'"usaon-benefit-tool".{table_name}'
            result = db.session.execute(text(f'SELECT * FROM {full_table_name}'))
            
            rows = result.fetchall()
            if not rows:
                continue
            
            # Get column names
            columns = result.keys()
            
            # Create CSV in memory
            csv_buffer = io.StringIO()
            writer = csv.writer(csv_buffer)
            
            # Write header
            writer.writerow(columns)
            
            # Write data
            for row in rows:
                writer.writerow(row)
            
            # Add to zip
            zf.writestr(f'{table_name}.csv', csv_buffer.getvalue())
    
    memory_file.seek(0)
    
    return Response(
        memory_file.getvalue(),
        mimetype='application/zip',
        headers={
            'Content-Disposition': f'attachment; filename=database-export-{date.today()}.zip'
        }
    )
