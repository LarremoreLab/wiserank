<template>
  <div v-show="loaded">
    <h1>Wise Rank</h1>
    <div v-if="email !== ''">
      <p v-if="sessionName !== ''" class="firstP">{{ email }} / {{ sessionName }}</p>
      <p v-else>{{ email }}</p>
    </div>
    <div v-if="hash == ''">
      <!-- toggle to make wise rank invite only (generate hashes for users) -->
      <UserLogin v-if="true" @userLoaded="displayUser"/> 
      <InviteOnly v-else />
    </div>
    <div v-else>
      <div v-if="activeSessionID == ''">
        <SessionDashboard :hash="hash" :sessions="sessions" @selectSession="updateSession"/>
      </div>
      <div v-else>
        <SingleSession :hash="hash" :sessionID="activeSessionID" @leaveSession="updateSession"/>
      </div>
    </div>  
  </div>
</template>

<script>
import axios from 'axios';

import UserLogin from './components/UserLogin.vue'
import InviteOnly from './components/InviteOnly.vue'
import SessionDashboard from './components/SessionDashboard.vue'
import SingleSession from './components/SingleSession.vue'


export default {
  name: 'App',
  components: {
    UserLogin,
    InviteOnly,
    SessionDashboard,
    SingleSession
  },
  data: () => ({
    hash: "", // "OZOQgECDtdmrclDVt7XSZw",
    email: "",
    sessions: [],
    activeSessionID: "",
    sessionName: "",
    loaded: false,
    // userData: {page: -2, hash: "", code: "", ranking: null, overallRanking: null},
  }),
  created (){
    const url = new URL(window.location)
    const p = url.searchParams.get('p')
    if (p){
      this.hash = p
      this.loadUser()
    } else {
      this.loaded = true
    }
  },
  methods: {
    displayUser(user) {
      this.hash = user.hash
      this.sessions = user.sessions
      this.email = user.email

      const url = new URL(window.location);
      url.searchParams.set('p', this.hash);
      history.pushState(null, '', url)
      this.loaded = true
    },
    updateSession(s,i,t){
      this.activeSessionID = s[0]
      this.sessionName = s[0] === '' ? '' : s[1] + " ("+(i+1)+")"
      if (t){
        this.sessions.push(s)
      }
    },
    loadUser() {
      axios.post(process.env.VUE_APP_API_URL+'/loaduser', {"email":this.email,"hash":this.hash})
            .then(response => {
                this.displayUser(response.data.user)
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }
  }
}

</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 20px;
}
.firstP{
  margin-top: 0px;
}
</style>
