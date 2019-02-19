<template>		
	<div class="help-text">
		<div v-html="helpText"></div>
	</div>
</template>

<script>


export default {
	name: 'helpText',
	props: ['helpText']
}
</script>

<style>
.help-text {
	margin-bottom: 20px;
}
</style>