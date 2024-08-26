<template>
  <div v-show="loaded">
    <!-- <hr class="solid"> -->
    <div v-if="isPair">
      <div>
        <h4>Compare Items:</h4>
      </div>
      <button id="leftItem" @click="submit_and_load_pair(0)">&larr; 1.</button>
      <button id="rightItem" @click="submit_and_load_pair(1)">2. &rarr;</button>
      <div>
      <ol>
        <li v-for="i in pair" :key="i.link_id">
          {{ i.name }}
        </li>
      </ol>
      </div>
    </div>
    <div v-else>
      <h4>Nothing to Compare!</h4>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  components: {
  },
  props: ["sessionID"],
  data() {
    return {
      pair: [{"link_id": -1,"name":""},{"link_id": -2,"name":""}],
      loaded: false,
      isPair: false,
    };
  },
  mounted() {
    this.submit_and_load_pair()
    window.addEventListener('keydown', this.handleKeydown);
  },
  unmounted() {
    window.removeEventListener('keydown', this.handleKeydown);
  },
  methods: {
    submit_and_load_pair(selection=0){
      const payload = {"sessionID":this.sessionID, "pair":this.pair, "selection":selection}
      axios.post(process.env.VUE_APP_API_URL+"/submitloadpair", payload)
        .then(response => {
            this.pair = response.data.new;
            this.isPair = this.pair[0]["name"] !== ""
            this.loaded = true
        })
        .catch(error => {
            console.error('Error:', error);
        });
    },
    handleKeydown(event) {
      if (event.key === 'ArrowLeft') {
        const button = document.querySelector('#leftItem');
        if (button) {
          button.click();
        }      
      }
      if (event.key === 'ArrowRight') {
        const button = document.querySelector('#rightItem');
        if (button) {
          button.click();
        }      
      }
    },
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
button{
  margin-left: 4px;
  margin-right: 4px;
}
ol { display: inline-block; text-align: left}
hr.solid {
  border-top: 3px solid #bbb;
}
</style>
  