<template>
  <div v-show="loaded">
    <!-- <hr class="solid"> -->
    <div>
        <h4>Compare Items:</h4>
    </div>
    <div>
      <button @click="submit_and_load_pair(0)">1.</button>
      <button @click="submit_and_load_pair(1)">2.</button>
      <div>
      <ol>
        <li v-for="i in pair" :key="i.link_id">
          {{ i.name }}
        </li>
      </ol>
      </div>
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
    };
  },
  mounted() {
    this.submit_and_load_pair()
  },
  methods: {
    submit_and_load_pair(selection=0){
      const payload = {"sessionID":this.sessionID, "pair":this.pair, "selection":selection}
      axios.post(process.env.VUE_APP_API_URL+"/submitloadpair", payload)
        .then(response => {
            this.pair = response.data.new;
            this.loaded = true
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
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
  