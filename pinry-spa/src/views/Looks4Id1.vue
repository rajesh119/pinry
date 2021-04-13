<template>
  <div class="pins-for-tag">
    <PHeader></PHeader>
    <PLooks4Id1 :pin-filters="filters"></PLooks4Id1>
    Related Posts<Products></Products>
  </div>
</template>

<script>
import PHeader from '../components/PHeader.vue';
import PLooks4Id1 from '../components/PLooks4Id1.vue';
import Products from '../components/Productsnew.vue';


export default {
  name: 'Looks4Id1',
  data() {
    return {
      filters: { idFilter: null },
    };
  },
  components: {
    PHeader,
    PLooks4Id1,
    Products,
  },
  created() {
    this.initialize();
  },
  beforeRouteUpdate(to, from, next) {
    console.log(to.params.pinId);
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
