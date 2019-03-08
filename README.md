## Shared Place

Specific functionalities for shared places

#### Installation

This application requires [Frappe](https://github.com/frappe/frappe) and [ERPNext](https://github.com/frappe/erpnext) v11.0.0 or higher.

1. `bench get-app shared_place https://github.com/dokos-io/shared_place
2. `bench install-app shared_place`
3. `bench restart && bench migrate`

This application is compatible with Python 3.6 and above.
You may experience issues with Python 2.7.

The application uses Frappe's scheduler.
Verify that your scheduler is enabled (`bench enable-scheduler`).

#### License

GPLv3
