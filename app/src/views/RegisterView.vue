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
          <h1>Create new account</h1>
          <form class="space-y-4 md:space-y-6">
            <div>
              <label for="username">Name</label>
              <input
                type="text"
                name="name"
                id="name"
                v-model="name"
                class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                placeholder="Name"
                required
              />
            </div>
            <div>
              <label for="username">Surname</label>
              <input
                type="text"
                name="surname"
                id="surname"
                v-model="surname"
                class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                placeholder="Surname"
                required
              />
            </div>
            <div>
              <label for="username">Username</label>
              <input
                type="text"
                name="username"
                id="username"
                v-model="username"
                class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                placeholder="Username"
                required
              />
            </div>
            <div>
              <label for="username">Email</label>
              <input
                type="text"
                name="email"
                id="email"
                v-model="email"
                class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                placeholder="Email"
                required
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
                required
              />
            </div>
            <div>
              <label
                for="password"
                class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
                >Confirm Password</label
              >
              <input
                type="password"
                name="password"
                id="password"
                placeholder="••••••••"
                v-model="confirm_password"
                class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                required
              />
            </div>
            <button type="submit" @click.prevent="user_register">
              Let's dive in
            </button>
            <p class="text-sm font-light text-gray-500 dark:text-gray-400">
              Already have an account ?
              <a
                href="/"
                class="font-medium text-primary-600 hover:underline dark:text-primary-500"
                >Sign in</a
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
  name: "RegisterView",
  data() {
    return {
      name: "",
      surname: "",
      username: "",
      password: "",
      confirm_password: "",
      email: "",
      message: "",
      message_type: "alert-warning",
    };
  },
  methods: {
    user_register() {
      if (this.match) {
        fetch("http://127.0.0.1:5000/api/register", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            name: this.name,
            surname: this.surname,
            username: this.username,
            password: this.password,
            email: this.email,
            bio: null,
            website: null,
          }),
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.status == "success") {
              window.location.href = "/";
            }
            alert(data.message);
          })
          .catch((error) => {
            console.error("Error:", error);
          });
      } else {
        this.message = "Password does not match";
      }
    },
  },
  computed: {
    match() {
      if (this.password == this.confirm_password && this.password != "") {
        return true;
      } else {
        return false;
      }
    },
    show_message() {
      return this.message != "";
    },
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
