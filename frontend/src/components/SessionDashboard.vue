<template>
  <div v-show="loaded">
    <div>
      <h4>Start a New Session:</h4>
      <div v-for="j in options" :key="j" class="newSession">
        <button @click="newSession(j)">{{ j }}</button>
      </div>
    </div>
    <div v-if="sessions.length > 0">
      <h4>Continue an Existing Session:</h4>
      <div v-for="s,i in sessions" :key="s[0]">
        <button @click="this.$emit('selectSession',s,i,false)">{{ s[1] }} ({{ i+1 }})</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  props: ["sessions","hash"],
  data() {
    return {
    name: 'SessionDashboard',
    options: [],
    loaded: false
    };
  },
  mounted() {
    axios.post(process.env.VUE_APP_API_URL+"/loadsessions", {"sessions":this.sessions,})
        .then(response => {
            this.options = response.data.options;
            this.loaded = true
        })
        .catch(error => {
            console.error('Error:', error);
        });
  },
  methods: {
    newSession(j){
      axios.post(process.env.VUE_APP_API_URL+"/newsession", {"track":j,"hash":this.hash})
          .then(response => {
            this.$emit('selectSession',response.data.session,this.sessions.length,true)
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
.newSession{
  display: inline-block;
}

.newButton{
  margin-left: 4px;
  margin-right: 4px;
}

button{
  margin-left: 4px;
  margin-right: 4px;
  margin-bottom: 4px;;
}
</style>
