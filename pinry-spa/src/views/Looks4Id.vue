<template>
  <div class="pins-for-tag">
    <PHeader></PHeader>
    <PLooks :pin-filters="filters"></PLooks>
  </div>
</template>

<script>
import PHeader from '../components/PHeader.vue';
import PLooks from '../components/PLooks.vue';

export default {
  name: 'Looks4Id',
  data() {
    return {
      filters: { idFilter: null },
    };
  },
  components: {
    PHeader,
    PLooks,
  },
  created() {
    this.initialize();
  },
  beforeRouteUpdate(to, from, next) {
    this.filters = { idFilter: to.params.pinId };
    next();
  },
  methods: {
    initialize() {
      this.filters = { idFilter: this.$route.params.pinId };
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
</style>
