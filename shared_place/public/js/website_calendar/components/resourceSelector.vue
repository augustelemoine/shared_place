<template>
	<div class="text-center">
		<div class="res-selector dropdown btn-group">
			<button class="btn btn-primary btn-lg dropdown-toggle" type="button" id="resourceSelector" data-toggle="dropdown" aria-haspopup="true" aria-expanded="true">
				{{ selectedResource.title || __("Resource Type") }}
				<span class="caret"></span>
			</button>
			<ul class="dropdown-menu" aria-labelledby="resourceSelector">
				<li v-for="resource in resources" :key="resource.id"><a @click="selectResource(resource)">{{ resource.title }}</a></li>
			</ul>
		</div>
	</div>
</template>

<script>


export default {
	name: 'resourceSelector',
	props: ['resources', 'selectResource', 'selectedResource']
}
</script>

<style>
.res-selector {
	margin-bottom: 20px;
}
</style>