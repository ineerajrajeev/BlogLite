<!-- eslint-disable prettier/prettier -->
<template>
  <NavBar></NavBar>
  <section class="home-section">
    <section class="text-gray-600 body-font overflow-hidden">
      <div class="container px-5 py-24 mx-auto">
        <div
          class="flex flex-wrap w-full mb-20 flex-col items-center text-center"
        >
          <h1
            class="sm:text-3xl text-2xl font-medium title-font mb-2 text-gray-900"
          >
            Search
          </h1>
          <div class="lg:w-1/2 w-full leading-relaxed text-gray-500">
            <div class="relative flex w-full flex-wrap items-stretch mb-3">
              <span
                class="z-10 h-full leading-snug font-normal absolute text-center text-gray-400 absolute bg-transparent rounded text-base items-center justify-center w-8 pl-3 py-3"
              >
                <i class="fas fa-search"></i>
              </span>
              <input
                type="text"
                placeholder="Find friends..."
                v-on:keyup="update_username($event)"
                class="px-3 py-3 placeholder-gray-400 text-gray-700 relative bg-white rounded text-sm shadow outline-none focus:outline-none focus:shadow-outline w-full pl-10"
              />
            </div>
          </div>
        </div>
        <div class="-my-8 divide-y-2 divide-gray-100" v-if="users.length > 0">
          <div
            class="py-8 flex flex-wrap md:flex-nowrap bg-gray-100 rounded-lg px-8"
            v-for="u in users"
            :key="u.id"
          >
            <div class="md:w-64 md:mb-0 mb-6 flex-shrink-0 flex flex-col">
              <span class="font-semibold title-font text-gray-700"
                >Profile Picture</span
              >
              <span class="mt-1 text-gray-500 text-sm">
                <div
                class="
                  w-20
                  h-20
                  rounded-full
                  inline-flex
                  items-center
                  justify-center
                  bg-gray-200
                  text-gray-400
                "
                style="border-radius: 50%"
              >
                <img :src="profile_pic(u.username)" />
              </div>
              </span>
              <p class="mt-1 text-gray-500 text-sm">@{{ u.username }}</p>
            </div>
            <div class="md:flex-grow">
              <h2 class="text-2xl font-medium text-gray-900 title-font mb-2">
                {{ u.name }} {{ u.surname }}
              </h2>
              <p class="leading-relaxed">
                <strong>Followers: </strong> {{ u.followers }} | <strong>Following: </strong> {{ u.following }}
              </p>
              <button class="button-33" role="button" @click.prevent = 'follow(u.username)'>Follow</button> .
              <button class="button-77" role="button" @click.prevent = 'unfollow(u.username)'>Unollow</button><br />
              <a class="text-indigo-500 inline-flex items-center mt-4"
              :href="'/user/'+u.username"
                >View Profile
                <svg
                  class="w-4 h-4 ml-2"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  stroke-width="2"
                  fill="none"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                >
                  <path d="M5 12h14"></path>
                  <path d="M12 5l7 7-7 7"></path>
                </svg>
              </a>
            </div>
            <br />
          </div>
        </div>
        <div class="flex flex-col items-center justify-center" v-else>
          <h1 class="text-2xl font-medium text-gray-900 title-font mb-2">
            No users found
          </h1>
        </div>
      </div>
    </section>
  </section>
</template>

<script>
import NavBar from "../components/NavBar.vue";

export default {
  name: "SearchView",
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
        if (data.status != "success") {
          this.$router.push("/");
        }
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  },
  components: {
    NavBar,
  },
  data: function () {
    return {
      username: "",
      users: [],
    };
  },
  methods: {
    update_username(event) {
      this.username = event.target.value;
      this.search();
    },
    profile_pic(username) {
      return "http://127.0.0.1:5000/api/profile_pic/" + username;
    },
    follow(username) {
      fetch("http://127.0.0.1:5000/api/follow", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "x-access-token": localStorage.getItem("blog_lite_token"),
        },
        body: JSON.stringify({
          username: username,
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          alert(data.message);
        });
    },
    unfollow(username) {
      fetch("http://127.0.0.1:5000/api/unfollow", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "x-access-token": localStorage.getItem("blog_lite_token"),
        },
        body: JSON.stringify({
          username: username,
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          alert(data.message);
        });
    },
    search() {
      if (this.username.length > 0) {
        fetch("http://127.0.0.1:5000/api/search", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "x-access-token": localStorage.getItem("blog_lite_token"),
          },
          body: JSON.stringify({
            username: event.target.value,
          }),
        })
          .then((response) => response.json())
          .then((data) => {
            this.users = data.user;
          });
      } else {
        this.users = [];
      }
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
  left: 78px;
  width: calc(100% - 78px);
  transition: all 0.5s ease;
  z-index: 2;
}
.sidebar.open ~ .home-section {
  left: 250px;
  width: calc(100% - 250px);
}
.home-section .text {
  display: inline-block;
  color: #11101d;
  font-size: 25px;
  font-weight: 500;
  margin: 18px;
}
.button-33 {
  background-color: #c2fbd7;
  border-radius: 100px;
  box-shadow: rgba(44, 187, 99, 0.2) 0 -25px 18px -14px inset,
    rgba(44, 187, 99, 0.15) 0 1px 2px, rgba(44, 187, 99, 0.15) 0 2px 4px,
    rgba(44, 187, 99, 0.15) 0 4px 8px, rgba(44, 187, 99, 0.15) 0 8px 16px,
    rgba(44, 187, 99, 0.15) 0 16px 32px;
  color: green;
  cursor: pointer;
  display: inline-block;
  font-family: CerebriSans-Regular, -apple-system, system-ui, Roboto, sans-serif;
  padding: 7px 20px;
  text-align: center;
  text-decoration: none;
  transition: all 250ms;
  border: 0;
  font-size: 16px;
  user-select: none;
  -webkit-user-select: none;
  touch-action: manipulation;
}
.button-33:hover {
  box-shadow: rgba(44, 187, 99, 0.35) 0 -25px 18px -14px inset,
    rgba(44, 187, 99, 0.25) 0 1px 2px, rgba(44, 187, 99, 0.25) 0 2px 4px,
    rgba(44, 187, 99, 0.25) 0 4px 8px, rgba(44, 187, 99, 0.25) 0 8px 16px,
    rgba(44, 187, 99, 0.25) 0 16px 32px;
  transform: scale(1.05) rotate(-1deg);
}
.button-77 {
  background-color: #fbc2c2;
  border-radius: 100px;
  box-shadow: rgba(187, 44, 44, 0.2) 0 -25px 18px -14px inset,
    rgba(187, 44, 44, 0.15) 0 1px 2px, rgba(187, 44, 44, 0.15) 0 2px 4px,
    rgba(187, 44, 44, 0.15) 0 4px 8px, rgba(187, 44, 44, 0.15) 0 8px 16px,
    rgba(187, 44, 44, 0.15) 0 16px 32px;
  color: rgb(128, 0, 0);
  cursor: pointer;
  display: inline-block;
  font-family: CerebriSans-Regular, -apple-system, system-ui, Roboto, sans-serif;
  padding: 7px 20px;
  text-align: center;
  text-decoration: none;
  transition: all 250ms;
  border: 0;
  font-size: 16px;
  user-select: none;
  -webkit-user-select: none;
  touch-action: manipulation;
}
.button-77:hover {
  box-shadow: rgba(187, 44, 44, 0.35) 0 -25px 18px -14px inset,
    rgba(187, 44, 44, 0.25) 0 1px 2px, rgba(187, 44, 44, 0.25) 0 2px 4px,
    rgba(187, 44, 44, 0.25) 0 4px 8px, rgba(187, 44, 44, 0.25) 0 8px 16px,
    rgba(187, 44, 44, 0.25) 0 16px 32px;
  transform: scale(1.05) rotate(-1deg);
}
</style>
