<template>
  <div v-show="loaded">
    <!-- <hr class="solid"> -->
    <div>
      <h4>Recommended Item:</h4>
      <p> {{ item.name }}</p>
      <button @click="submit_and_load_item(0)">No</button>
      <button @click="submit_and_load_item(1)">Yes</button>
    </div>
    <div> 
      <h4> Search for an Item:</h4>
      <input v-model="searchField">
      <button @click="searchField = ''" :disabled="searchField === ''">clear</button>
      <div>
        <ul :style="{marginTop:'2px', marginBottom:'16px'}">
          <li v-for="i in searched" :key="i.id">
            <button @click="submit_searched(i)" class="addButton">Add</button>
            {{ i.name }}
          </li>
        </ul>
      </div>
    </div>
    <div>
      <h4 :style="{margin:'0px'}">Selected Items:</h4>
      <ul>
        <li v-for="i in selected" :key="i[0]">
          {{ i[1] }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  components: {
  },
  props: [ "sessionID"],
  data() {
    return {
      item: {"link_id": -1,"name":""},
      searchField: '',
      searched: [],
      selected: [],
      loaded: false
    };
  },
  mounted() {
    this.submit_and_load_item()
  },
  watch: {
    searchField(a){
      const payload = {"sessionID":this.sessionID, "string":a}
      axios.post(process.env.VUE_APP_API_URL+"/searchitems", payload)
        .then(response => {
          if (a === '' || a === null){
            this.searched = []
          }
          else {
            let new_searches = [];
            for (let i = 0; i < response.data.length; i++){
              new_searches.push({"id":response.data[i][0], "name":response.data[i][1]})
            }
            this.searched = new_searches.filter(x => !this.selected.map(x => x[0]).includes(x.id))
          }
        })
        .catch(error => {
            console.error('Error:', error);
        });
      },
  },
  methods: {
    submit_and_load_item(selection=0){
      const payload = {"sessionID":this.sessionID, "item":this.item, "selection":selection}
      axios.post(process.env.VUE_APP_API_URL+"/submitloaditem", payload)
        .then(response => {
          this.item = response.data.new;
          this.selected = response.data.selected;
          this.loaded = true
        })
        .catch(error => {
            console.error('Error:', error);
        });
    },
    submit_searched(i){
      const payload = {"sessionID":this.sessionID, "item":{"link_id":i.id,"name":i.name}, "selection":1}
      axios.post(process.env.VUE_APP_API_URL+"/submitloaditem", payload)
        .then(response => {
            this.item = response.data.new;
            this.selected = response.data.selected;
            this.searched = this.searched.filter(x => x.id !==i.id)
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
  }
};
</script>

<style scoped>
hr.solid {
  border-top: 3px solid #bbb;
}
ul { display: inline-block; text-align: left; list-style-type: none; font-size: 14px;}
button.addButton{
  margin-right: 4px;
  margin-bottom: 2px;
}

button{
  margin-left: 4px;
  margin-right: 4px;
  margin-bottom: 4px;
}

</style>
  