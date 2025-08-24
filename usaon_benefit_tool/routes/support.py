from flask import Blueprint, render_template

support_bp = Blueprint('user_support', __name__)

@support_bp.route('/user-support/what-is-benefit-assessment')
def what_is_benefit_assessment():
    return render_template('what_is_benefit_assessment.html')

@support_bp.route('/user-support/user-guide')
def user_guide():
    return render_template('user_support/user_guide.html')

@support_bp.route('/user-support/rating-rubric')
def rating_rubric():
    return render_template('rating_rubric.html')

@support_bp.route('/user-support/glossary')
def glossary():
    return render_template('glossary.html')

@support_bp.route('/user-support/faqs')
def faqs():
    return render_template('faqs.html')
