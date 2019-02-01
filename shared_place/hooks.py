# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "shared_place"
app_title = "Shared Place"
app_publisher = "Dokos"
app_description = "Specific functionalities for shared places"
app_icon = "fa fa-slideshare"
app_color = "#86d8f7"
app_email = "hello@dokos.io"
app_license = "GPLv3"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/shared_place/css/shared_place.css"
# app_include_js = "/assets/shared_place/js/shared_place.js"

# include js, css files in header of web template
# web_include_css = "/assets/shared_place/css/shared_place.css"
web_include_js = "/assets/js/shared_place.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "shared_place.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

calendars = ["Shared Place Booking"]

# Installation
# ------------

# before_install = "shared_place.install.before_install"
# after_install = "shared_place.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "shared_place.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Quotation": {
		"on_trash": "shared_place.shared_place.utils.on_quotation_delete"
	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"shared_place.tasks.all"
# 	],
# 	"daily": [
# 		"shared_place.tasks.daily"
# 	],
# 	"hourly": [
# 		"shared_place.tasks.hourly"
# 	],
# 	"weekly": [
# 		"shared_place.tasks.weekly"
# 	]
# 	"monthly": [
# 		"shared_place.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "shared_place.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
override_whitelisted_methods = {
	"erpnext.shopping_cart.cart.place_order": "shared_place.shared_place.utils.shared_place_order"
}

