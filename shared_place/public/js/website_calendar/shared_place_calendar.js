import Vue from 'vue/dist/vue.js';
import FullCalendar from "vue-full-calendar";
import 'fullcalendar-scheduler';
import VModal from 'vue-js-modal';

import SharedPlaceCalendar from "./SharedPlaceCalendar.vue";

Vue.use(FullCalendar);
Vue.use(VModal, { dialog: true });

if (!window.Vue) {
	Vue.prototype.__ = window.__;
	Vue.prototype.frappe = window.frappe;
	window.Vue = Vue;
}

frappe.ready(function() {
	frappe.call({
		method: "shared_place.get_website_user_lang",
		freeze: true,
		callback: function(r) {
			Vue.prototype.frappe.lang = r.message
			if (Vue.prototype.frappe.lang == 'fr') {
				Vue.prototype.frappe._messages = {
					'Rooms/Resources': 'Salles/Ressources',
					'No slot available': 'Aucun créneau disponible',
					'Add or remove a slot': 'Ajoutez ou supprimez un créneau',
					'Select an option': 'Sélectionnez une option',
					'Close': 'Fermer',
					'Add to cart': 'ajouter au panier',
					'Resource Type': 'Type de ressource',
					'Buy units without selecting a slot': 'Acheter des unités sans sélectionner un créneau'
				}
			}
		}
	})

	new Vue({
		el: '#mainview',
		template: "<SharedPlaceCalendar/>",
		components: { SharedPlaceCalendar }
	})

});