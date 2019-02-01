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
	new Vue({
		el: '#mainview',
		template: "<SharedPlaceCalendar/>",
		components: { SharedPlaceCalendar }
	})

});