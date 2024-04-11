<template>
  <div>
    <p class="firstP">user: {{ email }}</p>
    <p class="secondP">session: {{ sessionName }}</p>
  </div>
  <div v-if="hash == ''">
    <UserLogin @userLoaded="displayUser"/>
  </div>
  <div v-else>
    <div v-if="activeSessionID == ''">
      <SessionDashboard :hash="hash" :sessions="sessions" @selectSession="updateSession"/>
    </div>
    <div v-else>
      <SingleSession :hash="hash" :sessionID="activeSessionID" @leaveSession="updateSession"/>
    </div>
  </div>  
</template>

<script>
import UserLogin from './components/UserLogin.vue'
import SessionDashboard from './components/SessionDashboard.vue'
import SingleSession from './components/SingleSession.vue'


export default {
  name: 'App',
  components: {
    UserLogin,
    SessionDashboard,
    SingleSession
  },
  data: () => ({
    hash: "", // "OZOQgECDtdmrclDVt7XSZw",
    email: "",
    sessions: [],
    activeSessionID: "",
    sessionName: ""
    // userData: {page: -2, hash: "", code: "", ranking: null, overallRanking: null},
  }),
  created (){
  },
  methods: {
    displayUser(user) {
      this.hash = user.hash
      this.sessions = user.sessions
      this.email = user.email
    },
    updateSession(s,i,t){
      this.activeSessionID = s[0]
      this.sessionName = s[0] === '' ? '' : i+1 + " ("+s[1]+")"
      if (t){
        this.sessions.push(s)
      }
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
  margin-bottom: 0px;
}
.secondP{
  margin-top: 0px;
}
</style>
