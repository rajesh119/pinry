<template>
  <div class="pins-for-user">
    <PHeader></PHeader>
    <PLooks :pin-filters="filters"></PLooks>
  </div>
</template>

<script>
import PHeader from '../components/PHeader.vue';
import PLooks from '../components/PLooks.vue';

export default {
  name: 'looks',
  data() {
    return {
      filters: { userFilter: null },
    };
  },
  components: {
    PHeader,
    PLooks,
  },
  created() {
    this.initializeBoard();
  },
  beforeRouteUpdate(to, from, next) {
    this.filters = { userFilter: to.params.user };
    next();
  },
  methods: {
    initializeBoard() {
      this.filters = { userFilter: this.$route.params.user };
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
</style>
