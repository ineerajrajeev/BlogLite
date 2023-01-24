<template>
  <div v-if="apiStatus">
    <router-view />
  </div>
  <div v-else>
    <h1>API is not running</h1>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "App",
  data() {
    return {
      apiStatus: true,
    };
  },
  methods: {
    async checkApiStatus() {
      try {
        const response = await axios.get("http://127.0.0.1:5000/apiCheck");
        if (response.status !== 200) {
          this.apiStatus = false;
        }
      } catch (error) {
        console.error(error);
        this.apiStatus = false;
      }
    },
  },
  created() {
    this.checkApiStatus();
  },
};
</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
