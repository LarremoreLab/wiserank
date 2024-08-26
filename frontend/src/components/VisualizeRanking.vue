<template>
  <div v-show="loaded">
    <div v-if="ranking.length !== 0">
      <div>
        <h4 :style="{marginBottom:'10px'}">Visualize Ranking:</h4>
      </div>
      <IndividualRanking :items="ranking" :comparisons="comparisons" @hovered="nodeHover"/>
    </div>
    <div v-else>
      <h4 :style="{marginBottom:'10px'}">Nothing to Rank!</h4>
    </div>
    <div>
      <ol>
        <li v-for="i in ranking" :key="i[0]"   :style="{fontWeight: i[2] === hoveredNode.name ? 'bold' : 'normal'}">
          {{ i[2] }}
        </li>
      </ol>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import IndividualRanking from './IndividualRanking.vue'


export default {
  components: {
    IndividualRanking
  },
  props: ["sessionID"],
  data() {
    return {
      ranking: [],
      loaded: false,
      comparisons: [],
      hoveredNode: {'name':''}
    };
  },
  mounted() {
    this.retrieve_individual_ranking()
  },
  methods: {
    retrieve_individual_ranking(){
      const payload = {"sessionID":this.sessionID}
      axios.post(process.env.VUE_APP_API_URL+"/rankindividual", payload)
        .then(response => {
            this.ranking = response.data.ranking;
            this.comparisons = response.data.comparisons
            this.loaded = true
        })
        .catch(error => {
            console.error('Error:', error);
        });
    },
    nodeHover(n){
      this.hoveredNode = n
    }
  }
};
</script>

<style scoped>
.hoveredNode{
  min-height: 30px;
  margin-bottom: 2px;
  margin-top: 2px;
  font-size: 16px;
}
ol { display: inline-block; text-align: left; font-size: 14px;}
</style>
    