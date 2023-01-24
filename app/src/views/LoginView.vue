<template>
  <section class="bg-gray-50 dark:bg-gray-900 home-section">
    <div
      class="flex flex-col items-center justify-center px-6 py-8 mx-auto md:h-screen lg:py-0"
    >
      <span
        class="flex items-center mb-6 text-2xl font-semibold text-gray-900 dark:text-white"
      >
        BlogLite
      </span>
      <div
        class="w-full bg-white rounded-lg shadow dark:border md:mt-0 sm:max-w-md xl:p-0 dark:bg-gray-800 dark:border-gray-700"
      >
        <div class="p-6 space-y-4 md:space-y-6 sm:p-8">
          <h1>Sign in to your account</h1>
          <form class="space-y-4 md:space-y-6">
            <div>
              <label
                for="username"
                class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
                >Username</label
              >
              <input
                type="text"
                name="username"
                id="username"
                v-model="username"
                class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                placeholder="Username"
                required=""
              />
            </div>
            <div>
              <label
                for="password"
                class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
                >Password</label
              >
              <input
                type="password"
                name="password"
                id="password"
                placeholder="••••••••"
                v-model="password"
                class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                required=""
              />
            </div>
            <button type="submit" @click.prevent="user_login">Sign in</button>
            <p class="text-sm font-light text-gray-500 dark:text-gray-400">
              Don’t have an account yet?
              <a
                href="/signup"
                class="font-medium text-primary-600 hover:underline dark:text-primary-500"
                >Sign up</a
              >
            </p>
          </form>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: "LoginView",
  data() {
    return {
      username: "",
      password: "",
      message: "",
      message_type: "alert-warning",
    };
  },
  methods: {
    user_login() {
      fetch("http://127.0.0.1:5000/api/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: this.username,
          password: this.password,
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.status == "success") {
            localStorage.setItem("blog_lite_token", data.token);
            this.$store.commit("setUser", data.user_data);
            this.message = "Welcome " + data.user_data.name;
            this.message_type = "alert-success";
            this.$router.push("/dashboard");
          } else {
            alert(data.message);
          }
        });
    },
  },
  computed: {
    show_message() {
      return this.message != "";
    },
  },
  beforeCreate: function () {
    const token = localStorage.getItem("blog_lite_token");
    // make an api call to check if the token is valid
    fetch("http://127.0.0.1:5000/api/verify_token", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "x-access-token": token,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status == "success") {
          this.$router.push("/dashboard");
        }
      });
  },
};
</script>

<style>
.home-section {
  position: relative;
  background: #e4e9f7;
  min-height: 100vh;
  top: 0;
  transition: all 0.5s ease;
  z-index: 2;
}
.home-section .text {
  display: inline-block;
  color: #11101d;
  font-size: 25px;
  font-weight: 500;
  margin: 18px;
}
</style>
