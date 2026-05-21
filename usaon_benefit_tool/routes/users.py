import csv
import io
from datetime import datetime

import pytz
from flask import Blueprint, Response, render_template
from flask_login import login_required

from usaon_benefit_tool._types import RoleName
from usaon_benefit_tool.models.tables import User
from usaon_benefit_tool.util.rbac import forbid_except_for_roles

users_bp = Blueprint('users', __name__, url_prefix='/users')


@users_bp.route('', methods=['GET'])
@login_required
def get():
    forbid_except_for_roles([RoleName.ADMIN])

    users = User.query.order_by(User.name).all()
    return render_template(
        'users.html',
        users=users,
    )


@users_bp.route('/export', methods=['GET'])
@login_required
def export():
    """Export users table as CSV."""
    forbid_except_for_roles([RoleName.ADMIN])

    users = User.query.order_by(User.name).all()

    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)

    # Write header
    writer.writerow(
        ['ID', 'Email', 'Name', 'ORCID', 'Role', 'Biography', 'Affiliation'],
    )

    # Write user data
    for user in users:
        writer.writerow(
            [
                user.id,
                user.email,
                user.name,
                user.orcid,
                user.role_id.value if user.role_id else '',
                user.biography,
                user.affiliation,
            ],
        )

    # Prepare response
    output.seek(0)
    today = datetime.now(pytz.UTC).date()

    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={
            'Content-Disposition': (
                f'attachment; filename=usaon-benefit-tool-users-{today}.csv'
            ),
        },
    )
