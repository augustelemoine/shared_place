# Copyright (c) 2019, Dokos and Contributors
# License: GNU General Public License v3. See license.txt

from frappe.data_migration.doctype.data_migration_connector.connectors.calendar_connector import CalendarConnector
import frappe
from datetime import datetime
from frappe.utils.background_jobs import get_jobs
import time

class SharedPlaceConnector(CalendarConnector):
	def __init__(self, connector):
		super(SharedPlaceConnector, self).__init__(connector)

	def insert(self, doctype, doc):
		super(SharedPlaceConnector, self).insert(doctype, doc)
		if doctype == 'Shared Place Events':
			if doc["start_datetime"] >= datetime.now():
				try:
					doctype = "Shared Place Booking"
					e = self.insert_events(doctype, doc)
					return e
				except Exception:
					frappe.log_error(frappe.get_traceback(), "GCalendar Synchronization Error")

	def update(self, doctype, doc, migration_id):
		super(SharedPlaceConnector, self).update(doctype, doc, migration_id)
		if doctype == 'Shared Place Events':
			if doc["start_datetime"] >= datetime.now() and migration_id is not None:
				try:
					doctype = "Shared Place Booking"
					return self.update_events(doctype, doc, migration_id)
				except Exception:
					frappe.log_error(frappe.get_traceback(), "GCalendar Synchronization Error")

	def delete(self, doctype, migration_id):
		super(SharedPlaceConnector, self).delete(doctype, migration_id)
		if doctype == 'Shared Place Events':
			try:
				return self.delete_events(migration_id)
			except Exception:
				frappe.log_error(frappe.get_traceback(), "GCalendar Synchronization Error")

def sync_accounts():
	frappe.has_permission('GCalendar Settings', throw=True)

	accounts = frappe.get_all("GCalendar Account", filters={'enabled': 1})

	queued_jobs = get_jobs(site=frappe.local.site, key='job_name')[frappe.local.site]
	for account in accounts:
		job_name = 'google_calendar_sp_sync|{0}'.format(account.name)
		if job_name not in queued_jobs:
			frappe.enqueue('shared_place.shared_place.gcalendar_connector.run_sync', queue='long', timeout=1500, job_name=job_name, account=account)
			time.sleep(5)

def run_sync(account):
	exists = frappe.db.exists('Data Migration Run', dict(status=('in', ['Fail', 'Error'])))
	if exists:
		failed_run = frappe.get_doc("Data Migration Run", dict(status=('in', ['Fail', 'Error'])))
		failed_run.delete()

	started = frappe.db.exists('Data Migration Run', dict(status=('in', ['Started'])))
	if started:
		return

	try:
		doc = frappe.get_doc({
			'doctype': 'Data Migration Run',
			'data_migration_plan': 'GCalendar Shared Place Sync',
			'data_migration_connector': 'Shared Place Calendar Connector-' + account.name
		}).insert()
		try:
			doc.run()
		except Exception:
			frappe.log_error(frappe.get_traceback())
	except Exception:
		frappe.log_error(frappe.get_traceback())