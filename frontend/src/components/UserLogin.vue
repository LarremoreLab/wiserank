<template>
  <div>
    <input 
    v-model="email" 
    type="text" 
    placeholder="email or username"
    @keydown.enter="handleEnter">
    <button @click="loadUser">Create or Load Profile</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'UserLogin',
  components: {
  },
  data: () => ({
    email: "",
  }),
  mounted() {
    // this.loadUser()
  },
  methods: {
    loadUser() {
      axios.post(process.env.VUE_APP_API_URL+'/loaduser', {"email":this.email})
            .then(response => {
                this.$emit('userLoaded',response.data.user)
            })
            .catch(error => {
                console.error('Error:', error);
            });
    },
    handleEnter() {
      // Trigger the button click programmatically
      this.loadUser();
    },
  }
}
</script>

<style>
button{
  margin-left: 4px;
  margin-right: 4px;
}
</style>
