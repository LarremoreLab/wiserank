<template>
  <div>
    <button @click="this.$emit('leaveSession',['',''],'',false)">Exit Session</button>
    <button @click="stage = 1" :disabled="stage === 1">Select Items</button>
    <button @click="stage = 2" :disabled="stage === 2">Compare Items</button>
    <button @click="stage = 3" :disabled="stage === 3">Visualize Ranking</button>
  </div>
  <div>
    <SelectItems v-if="stage == 1" :sessionID="sessionID"/>
    <CompareItems v-if="stage == 2" :sessionID="sessionID"/>
    <VisualizeRanking v-if="stage == 3" :sessionID="sessionID"/>
  </div>
</template>

<script>
import SelectItems from './SelectItems.vue'
import CompareItems from './CompareItems.vue'
import VisualizeRanking from './VisualizeRanking.vue'

// import axios from 'axios';

export default {
  components: {
    SelectItems,
    CompareItems,
    VisualizeRanking
  },
  props: ["hash", "sessionID"],
  emits: ["leaveSession"],
  data() {
    return {
    name: 'SingleSession',
    session: null,
    stage: 1
    };
  },
  mounted() {
  },
  methods: {
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
button{
  margin-left: 4px;
  margin-right: 4px;
  margin-bottom: 4px;
}
</style>
  