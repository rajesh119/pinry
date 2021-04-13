<template>

  <div class="pins">
    <section class="section">
      <div id="pins-container" class="container" v-if="blocks">
          <template v-for="item in blocks">
          <div class="card" v-bind:key="item.id">
          <div>
            <div style="float:left;width:45%;" >
              <img :src="item.original_image_url" alt="Image">
            </div>
            <div style="float:right;width:45%;">
                <Products></Products>
            </div>
          </div>
          <div class="card-content">
            <div class="content">
                <p class="description title" v-html="niceLinks(item.description)"></p>
            </div>
            <div class="media">
              <div class="media-left">
                <figure class="image is-48x48">
                  <img :src="item.avatar" alt="Image">
                </figure>
              </div>
              <div class="media-content">
                <div class="is-pulled-left">
                  <p class="title is-4 pin-meta-info"><span class="dim">Pinned by </span><span class="author">{{ item.author }}</span></p>
                  <p class="subtitle is-6" v-show="item.tags.length > 0">
                    <span class="subtitle dim">in&nbsp;</span>
                    <template v-for="tag in item.tags">
                      <b-tag v-bind:key="tag" type="is-info" class="pin-preview-tag">{{ tag }}</b-tag>
                    </template>
                  </p>
                </div>
                <div class="is-pulled-right">
                  <a :href="item.referer" target="_blank">
                    <b-button
                        v-show="item.referer !== null"
                        class="meta-link"
                        type="is-warning">
                      Source
                    </b-button>
                  </a>
                  <a :href="item.original_image_url" target="_blank">
                    <b-button
                        v-show="item.original_image_url !== null"
                        class="meta-link"
                        type="is-link">
                        Original Image
                    </b-button>
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div></template>
      </div>
    </section>
  </div>
</template>

<script>
import API from './api';
import pinHandler from './utils/PinHandler';
import scroll from './utils/scroll';
import bus from './utils/bus';
import niceLinks from './utils/niceLinks';
import Products from './Productsnew.vue';

function createImageItem(pin) {
  const image = {};
  // image.url = pinHandler.escapeUrl(pin.image_url);
  image.url = pin.image_url;
  image.id = pin.id;
  // image.owner_id = pin.submitter.id;
  // image.private = pin.private;
  image.description = pin.description;
  image.tags = pin.tags;
  // image.author = pin.submitter.username;
  // image.avatar = `//gravatar.com/avatar/${pin.submitter.gravatar}`;
  image.large_image_url = pinHandler.escapeUrl(pin.image_url);
  image.original_image_url = pin.image_url;
  // image.referer = pin.referer;
  // image.orgianl_width = pin.image.width;
  image.style = {
    width: `${image.width}px`,
    height: `${image.height}px`,
  };
  image.class = {};
  console.log(image);
  return image;
}

function initialData() {
  return {
    blocks: [],
    blocksMap: {},
    status: {
      loading: false,
      hasNext: true,
      offset: 0,
    },
    editorMeta: {
      currentEditId: null,
      currentBoard: {},
      user: {
        loggedIn: false,
        meta: {},
      },
    },
  };
}

export default {
  name: 'PLooks4Id1',
  data() {
    return initialData();
  },
  components:
  {
    Products,
  },
  props: {
    pinFilters: {
      type: Object,
      default() {
        return {
          tagFilter: null,
          userFilter: null,
          boardFilter: null,
        };
      },
    },
  },
  watch: {
    pinFilters() {
      this.reset();
    },
  },
  methods: {
    shouldShowEdit(id) {
      if (!this.editorMeta.user.loggedIn) {
        return false;
      }
      return this.editorMeta.currentEditId === id;
    },
    showEditButtons(id) {
      this.editorMeta.currentEditId = id;
    },
    hideEditButtons() {
      this.editorMeta.currentEditId = null;
    },
    onPinImageLoaded(itemId) {
      this.blocksMap[itemId].class = {
        'image-loaded': true,
      };
      this.blocksMap[itemId].style.height = 'auto';
    },
    registerScrollEvent() {
      const self = this;
      scroll.bindScroll2Bottom(
        () => {
          if (self.status.loading || !self.status.hasNext) {
            return;
          }
          self.fetchMore();
        },
      );
    },
    buildBlocks(results) {
      const blocks = [];
      results.forEach(
        (pin) => {
          const item = createImageItem(pin);
          blocks.push(
            item,
          );
        },
      );
      return blocks;
    },
    shouldFetchMore(created) {
      if (!created) {
        if (this.status.loading) {
          return false;
        }
        if (!this.status.hasNext) {
          return false;
        }
      }
      return true;
    },
    initialize() {
      this.initializeMeta();
      this.fetchMore(true);
    },
    initializeMeta() {
      const self = this;
      API.User.fetchUserInfo().then(
        (user) => {
          if (user === null) {
            self.editorMeta.user.loggedIn = false;
            self.editorMeta.user.meta = {};
          } else {
            self.editorMeta.user.meta = user;
            self.editorMeta.user.loggedIn = true;
          }
        },
      );
    },
    reset() {
      const data = initialData();
      Object.entries(data).forEach(
        (kv) => {
          const [key, value] = kv;
          this[key] = value;
        },
      );
      this.initialize();
    },
    fetchMore(created) {
      if (!this.shouldFetchMore(created)) {
        return;
      }
      this.status.loading = true;
      let promise;
      if (this.pinFilters.tagFilter) {
        promise = API.fetchLooks(this.status.offset, this.pinFilters.tagFilter);
      } else if (this.pinFilters.userFilter) {
        promise = API.fetchLooks(this.status.offset, null, this.pinFilters.userFilter);
      } else if (this.pinFilters.boardFilter) {
        promise = new Promise(
          (resolve, reject) => {
            API.fetchPinsForBoard(this.pinFilters.boardFilter).then(
              (resp) => {
                this.editorMeta.currentBoard = resp.data.board;
                resolve(resp);
              },
              (error) => {
                reject(error);
              },
            );
          },
        );
      } else if (this.pinFilters.idFilter) {
        promise = API.fetchLook(this.pinFilters.idFilter);
      } else {
        promise = API.fetchLooks(this.status.offset);
      }
      promise.then(
        (resp) => {
          const { results, next } = resp.data;
          console.log(results);
          let newBlocks = this.buildBlocks(results);
          newBlocks.forEach(
            (item) => { this.blocksMap[item.id] = item; },
          );
          newBlocks = this.blocks.concat(newBlocks);
          this.blocks = newBlocks;
          this.status.offset = newBlocks.length;
          this.status.hasNext = !(next === null);
          this.status.loading = false;
        },
        () => { this.status.loading = false; },
      );
    },
    niceLinks,
  },
  created() {
    bus.bus.$on(bus.events.refreshPin, this.reset);
    this.registerScrollEvent();
    this.initialize();
  },
};
</script>

<style lang="scss" scoped>
/* grid */
@import 'utils/pin';

.grid-sizer,
.grid-item { width: $pin-preview-width; }
.grid-item {
  margin-bottom: 15px;
}
.gutter-sizer {
  width: 15px;
}

/* pin-image transition */
.pin-masonry.image-loaded{
  opacity: 1;
  transition: opacity .3s;
}
.pin-masonry {
  opacity: 0;
}

/* card */
$pin-footer-position-fix: -6px;
$avatar-width: 30px;
$avatar-height: 30px;
@import './utils/fonts';
@import './utils/loader.scss';

.pin-card{
  .pin-preview-image {
    cursor: zoom-in;
  }
  > img {
    min-width: $pin-preview-width;
    background-color: white;
    border-radius: 3px 3px 0 0;
    @include loader('../assets/loader.gif');
  }
  .avatar {
    height: $avatar-height;
    width: $avatar-width;
    border-radius: 3px;
  }
  .pin-tag {
    margin-right: 0.2rem;
  }
}
.pin-footer {
  position: relative;
  top: $pin-footer-position-fix;
  background-color: white;
  border-radius: 0 0 3px 3px ;
  box-shadow: 0 1px 0 #bbb;
  .description {
    @include description-font;
    padding: 8px;
    border-bottom: 1px solid #DDDDDD;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .details {
    @include secondary-font;
    padding: 10px;
    > .pin-info {
      line-height: 16px;
      width: 220px;
      padding-left: $avatar-width + 5px;
    }
    .pin-info a {
      font-weight: bold;
    }
  }
}

@import 'utils/grid-layout';
@include screen-grid-layout("#pins-container")

</style>
