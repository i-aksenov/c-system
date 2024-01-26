from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)
from flask_login import current_user, login_required

from models import Client, Document

main = Blueprint("main", __name__)


@main.route("/")
@login_required
def index():
    if current_user.perm_read_private_docs:
        documents = Document.query.all()
    else:
        documents = Document.query.filter_by(is_private=False).all()

    if current_user.perm_give_out_food:
        clients = [client.name for client in Client.query.all()]
    else:
        clients = []

    return render_template(
        "index.html",
        documents=documents,
        clients=clients,
        username=current_user.username,
    )


@main.route("/coupon", methods=["POST"])
@login_required
def get_coupon():
    if not current_user.perm_give_out_food:
        flash("У пользователя недостаточно прав для выдачи талонов на питание.")
        return redirect(url_for("main.index"))

    selected_name = request.form.get("selected_option")
    client = Client.query.filter_by(name=selected_name).first()

    if client:
        coupon = client.coupon

        flash(f"Выданный талон на питание: {coupon}")
    else:
        flash("Данный получатель не зарегистрирован в системе.")

    return redirect(url_for("main.index"))


@main.route("/document/<int:document_id>")
@login_required
def document(document_id):
    doc = Document.query.get_or_404(document_id)

    return send_from_directory("documents", doc.path)
