"""Integration probe for the dedicated fictional agape.localhost development site."""
import json
from pathlib import Path
import frappe
from frappe.utils import add_days, nowdate, getdate

def run(verify_only=False):
    if frappe.local.site != "agape.localhost":
        raise RuntimeError("This probe is restricted to the dedicated agape.localhost test site.")
    frappe.set_user("Administrator")
    evidence = Path(frappe.get_site_path("private", "files", "agape-smoke.json"))
    if verify_only:
        state = json.loads(evidence.read_text())
        for doctype, name in state.items():
            if not frappe.db.exists(doctype, name):
                raise RuntimeError(f"Record missing after restart: {doctype}")
        invoice = frappe.get_doc("Sales Invoice", state["Sales Invoice"])
        if invoice.docstatus != 0 or float(invoice.grand_total) != 90.0:
            raise RuntimeError("Fictional draft invoice has unexpected status/amount.")
        return {"persisted": True, "checked_doctypes": list(state)}
    if evidence.exists():
        return run(verify_only=True)
    # Use ERPNext's own setup presets on this fictional development site.
    # These establish groups, units and warehouse types required by Company.
    from erpnext.setup.setup_wizard.operations.install_fixtures import install as install_presets
    install_presets("Brazil")
    for doctype, name in (("Warehouse Type", "Transit"), ("Customer Group", "Individual"),
                          ("Territory", "Brazil"), ("UOM", "Nos"), ("Party Type", "Customer")):
        if not frappe.db.exists(doctype, name):
            raise RuntimeError(f"ERPNext setup preset missing: {doctype} / {name}")
    state = {}
    company_name = "Doctor Agape DEMO"
    company = frappe.db.exists("Company", company_name)
    if not company:
        company = frappe.get_doc({
            "doctype": "Company", "company_name": company_name, "abbr": "DAD",
            "country": "Brazil", "default_currency": "BRL",
            "create_chart_of_accounts_based_on": "Standard Template",
            "chart_of_accounts": "Standard"
        }).insert().name
    state["Company"] = company
    company_doc = frappe.get_doc("Company", company)
    year = getdate(nowdate()).year
    fiscal_name = f"{year} DEMO Agape"
    if not frappe.db.exists("Fiscal Year", fiscal_name):
        frappe.get_doc({"doctype": "Fiscal Year", "year": fiscal_name,
                        "year_start_date": f"{year}-01-01", "year_end_date": f"{year}-12-31",
                        "companies": [{"company": company}]}).insert()
    price_list_name = "DEMO Agape BRL"
    if not frappe.db.exists("Price List", price_list_name):
        frappe.get_doc({"doctype": "Price List", "price_list_name": price_list_name,
                        "currency": "BRL", "selling": 1, "enabled": 1}).insert()

    settings = frappe.get_single("Healthcare Settings")
    settings.link_customer_to_patient = 0
    settings.show_payment_popup = 0
    settings.collect_registration_fee = 0
    settings.save()
    group = "Individual"
    territory = "Brazil"
    customer = frappe.get_doc({
        "doctype": "Customer", "customer_name": "Paciente Ficticio DEMO",
        "customer_type": "Individual", "customer_group": group, "territory": territory
    }).insert()
    state["Customer"] = customer.name
    gender = frappe.db.get_value("Gender", {}, "name")
    if not gender:
        gender = frappe.get_doc({"doctype": "Gender", "gender": "Other"}).insert().name
    patient = frappe.get_doc({
        "doctype": "Patient", "first_name": "Paciente", "last_name": "Ficticio DEMO",
        "sex": gender, "customer": customer.name, "invite_user": 0
    }).insert()
    state["Patient"] = patient.name
    practitioner = frappe.get_doc({
        "doctype": "Healthcare Practitioner", "first_name": "Profissional Ficticio DEMO",
        "status": "Active"
    }).insert()
    state["Healthcare Practitioner"] = practitioner.name
    appointment_type_name = "Consulta DEMO Agape"
    if not frappe.db.exists("Appointment Type", appointment_type_name):
        frappe.get_doc({"doctype": "Appointment Type", "appointment_type": appointment_type_name,
                        "default_duration": 30, "allow_booking_for": "Practitioner"}).insert()
    appointment = frappe.get_doc({
        "doctype": "Patient Appointment", "patient": patient.name, "company": company,
        "practitioner": practitioner.name, "appointment_for": "Practitioner",
        "appointment_type": appointment_type_name, "appointment_date": add_days(nowdate(), 1),
        "appointment_time": "09:00:00", "duration": 30
    }).insert()
    state["Patient Appointment"] = appointment.name
    encounter = frappe.get_doc({
        "doctype": "Patient Encounter", "patient": patient.name, "company": company,
        "practitioner": practitioner.name, "appointment": appointment.name,
        "encounter_date": nowdate(), "encounter_time": "09:00:00",
        "status": "Open"
    }).insert()
    state["Patient Encounter"] = encounter.name
    item_code = "AGAPE-DEMO-CONSULTA"
    if not frappe.db.exists("Item", item_code):
        item_group = "Services"
        uom = "Nos"
        frappe.get_doc({"doctype": "Item", "item_code": item_code,
                        "item_name": "Consulta ficticia de demonstracao", "item_group": item_group,
                        "stock_uom": uom, "is_stock_item": 0}).insert()
    invoice = frappe.get_doc({
        "doctype": "Sales Invoice", "customer": customer.name, "company": company,
        "posting_date": nowdate(), "due_date": nowdate(), "currency": "BRL",
        "conversion_rate": 1, "selling_price_list": price_list_name,
        "price_list_currency": "BRL", "plc_conversion_rate": 1,
        "debit_to": company_doc.default_receivable_account,
        "items": [{"item_code": item_code, "qty": 1, "rate": 90,
                   "income_account": company_doc.default_income_account,
                   "cost_center": company_doc.cost_center}]

    }).insert()
    if invoice.docstatus != 0 or float(invoice.grand_total) != 90.0:
        raise RuntimeError("Draft invoice validation failed.")
    state["Sales Invoice"] = invoice.name
    frappe.db.commit()
    evidence.parent.mkdir(parents=True, exist_ok=True)
    evidence.write_text(json.dumps(state))
    return {"created_fictional_records": list(state), "draft_invoice_total": 90, "charged": False}
